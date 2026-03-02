using System.Collections.Generic;
using System.Buffers.Binary;
using static PokeplaygroundTestDomain.PokemonGen1;
using PokeplaygroundTestDomain;

var gen1CharMap = new Dictionary<byte, string>()
{
    { 0x4F, " " },
    { 0x50, "\0" }, // terminator
    { 0x51, "*" },
    { 0x52, "A1" },
    { 0x53, "A2" },
    { 0x54, "POKé" },
    { 0x55, "+" },
    { 0x57, "#" },
    { 0x58, "$" },
    { 0x75, "…" },
    { 0x7F, " " },
    { 0x80, "A" },
    { 0x81, "B" },
    { 0x82, "C" },
    { 0x83, "D" },
    { 0x84, "E" },
    { 0x85, "F" },
    { 0x86, "G" },
    { 0x87, "H" },
    { 0x88, "I" },
    { 0x89, "J" },
    { 0x8A, "K" },
    { 0x8B, "L" },
    { 0x8C, "M" },
    { 0x8D, "N" },
    { 0x8E, "O" },
    { 0x8F, "P" },
    { 0x90, "Q" },
    { 0x91, "R" },
    { 0x92, "S" },
    { 0x93, "T" },
    { 0x94, "U" },
    { 0x95, "V" },
    { 0x96, "W" },
    { 0x97, "X" },
    { 0x98, "Y" },
    { 0x99, "Z" },
    { 0x9A, "(" },
    { 0x9B, ")" },
    { 0x9C, ":" },
    { 0x9D, ";" },
    { 0x9E, "[" },
    { 0x9F, "]" },
    { 0xA0, "a" },
    { 0xA1, "b" },
    { 0xA2, "c" },
    { 0xA3, "d" },
    { 0xA4, "e" },
    { 0xA5, "f" },
    { 0xA6, "g" },
    { 0xA7, "h" },
    { 0xA8, "i" },
    { 0xA9, "j" },
    { 0xAA, "k" },
    { 0xAB, "l" },
    { 0xAC, "m" },
    { 0xAD, "n" },
    { 0xAE, "o" },
    { 0xAF, "p" },
    { 0xB0, "q" },
    { 0xB1, "r" },
    { 0xB2, "s" },
    { 0xB3, "t" },
    { 0xB4, "u" },
    { 0xB5, "v" },
    { 0xB6, "w" },
    { 0xB7, "x" },
    { 0xB8, "y" },
    { 0xB9, "z" },
    { 0xBA, "é" },
    { 0xBB, "'d" },
    { 0xBC, "'l" },
    { 0xBD, "'s" },
    { 0xBE, "'t" },
    { 0xBF, "'v" },
    { 0xE0, "'" },
    { 0xE1, "PK" },
    { 0xE2, "MN" },
    { 0xE3, "-" },
    { 0xE4, "'r" },
    { 0xE5, "'m" },
    { 0xE6, "?" },
    { 0xE7, "!" },
    { 0xE8, "." },
    { 0xED, "?" },
    { 0xEE, "?" },
    { 0xEF, "?" },
    { 0xF0, "¥" },
    { 0xF1, "×" },
    { 0xF3, "/" },
    { 0xF4, "," },
    { 0xF5, "?" },
    { 0xF6, "0" },
    { 0xF7, "1" },
    { 0xF8, "2" },
    { 0xF9, "3" },
    { 0xFA, "4" },
    { 0xFB, "5" },
    { 0xFC, "6" },
    { 0xFD, "7" },
    { 0xFE, "8" },
    { 0xFF, "9" }
};

Dictionary<string, int> offsets = new Dictionary<string, int>()
{
    {"name", 0x598 + 8192},
    {"TID", 0x2605},
    {"money", 0x25F3},
    {"boxdata", 0x4000},
};

static byte[] Slice(byte[] data, int offset, int length)
{
    byte[] result = new byte[length];
    Array.Copy(data, offset, result, 0, length);
    return result;
}

static uint readUint24(byte[] data, int offset)
{
    byte b0 = data[offset];     // low byte
    byte b1 = data[offset + 1];   // middle byte
    byte b2 = data[offset + 2];   // high byte
    uint value = (uint)((b0 << 16) | (b1 << 8) | b2);
    return value;
}

Console.WriteLine("Enter the path to the save file:");
string fpath = Console.ReadLine();

byte[] save = File.ReadAllBytes(fpath);


// general data dump

// Name
byte[] plrname = Slice(save, offsets["name"], 11);
string name = string.Concat(plrname
    .TakeWhile(b => b != 0x50)
    .Select(b => gen1CharMap[b]));

Console.WriteLine(name);

// Trainer ID

Console.WriteLine(BinaryPrimitives.ReadUInt16BigEndian(save.AsSpan(offsets["TID"])));

// balance
int money = int.Parse(readUint24(save, offsets["money"]).ToString("X6"));
Console.WriteLine(money);

// comand line box reader
string cmd = "";
int curbox = 0;
while (cmd != "exit")
{
    Console.WriteLine($"box {curbox}:");
    cmd = Console.ReadLine();
    if (cmd.StartsWith("switch"))
    {
        curbox = int.Parse(cmd.Split(' ')[1]);
        if (curbox > 11)
        {
            Console.WriteLine("Box out of range");
            curbox = 11;
        }
        else if (curbox < 0)
        {
            Console.WriteLine("Box out of range");
            curbox = 0;
        }
    }
    else if (cmd.StartsWith("read"))
    {
        int toread = int.Parse(cmd.Split(' ')[1]);

        int address = offsets["boxdata"] + (curbox*1122) + 22 + (33*toread);

        PokemonGen1 pokemon = new PokemonGen1(save[address..(address + 33)]);
        Console.WriteLine("reading start as " + address);
        Console.WriteLine($"Species ID: {pokemon.SpeciesID}");
    }
}