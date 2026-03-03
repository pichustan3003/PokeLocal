from gen1infodicts import *
from allinfodicts import *

class gen1Pokemon:
    def __init__(self,
                 speciesId : int,
                 curHP : int, level,
                 condition : int,
                 type1 : int,
                 type2 : int,
                 heldItem : int,
                 move1 : int,
                 move2: int,
                 move3 : int,
                 move4 : int,
                 otid : int,
                 exp : int,
                 hpEv : int,
                 atkEv : int,
                 defEv : int,
                 spdEv : int,
                 spcEv : int,
                 hpIv : int,
                 atkIv : int,
                 defIv : int,
                 spdIv : int,
                 spcIv : int,
                 move1pp : int,
                 move2pp : int,
                 move3pp : int,
                 move4pp : int,
                 move1ppups : int,
                 move2ppups : int,
                 move3ppups : int,
                 move4ppups : int,) -> None:

        self.speciesId : int = speciesId
        self.speciesstr : str = speciesMap[self.speciesId]
        self.currentHP : int = curHP
        self.level : int = level
        self.condition : int = condition
        self.conditionstr : str = statusmap[self.condition]

        self.type1 : int = type1
        self.type2 : int = type2
        self.type1str : str = typemap[self.type1]
        self.type2str : str = typemap[self.type2]

        self.heldItem : int = heldItem

        self.move1 : int = move1
        self.move1str : str = movemap[self.move1] if self.move1 != 0 else None
        self.move2: int = move2
        self.move2str: str = movemap[self.move2] if self.move2 != 0 else None
        self.move3: int = move3
        self.move3str: str = movemap[self.move3] if self.move3 != 0 else None
        self.move4: int = move4
        self.move4str: str = movemap[self.move4] if self.move4 != 0 else None

        self.OT : int = otid
        self.exp : int = exp

        self.hpEv : int = hpEv
        self.atkEv : int = atkEv
        self.defEv : int = defEv
        self.spdEv : int = spdEv
        self.spcEv : int = spcEv

        self.hpIv: int = hpIv
        self.atkIv: int = atkIv
        self.defIv: int = defIv
        self.spdIv: int = spdIv
        self.spcIv: int = spcIv

        self.move1pp : int = move1pp
        self.move2pp : int = move2pp
        self.move3pp : int = move3pp
        self.move4pp : int = move4pp

        self.move1ppups : int = move1ppups
        self.move2ppups : int = move2ppups
        self.move3ppups : int = move3ppups
        self.move4ppups : int = move4ppups

    def __str__(self):

        return (f"Species:{self.speciesstr} ({self.speciesId})\n"
                f"HP:{self.currentHP}\nLevel:{self.level}\n"
                f"Condition:{self.conditionstr}\n"
                f"Type1:{self.type1str} ({self.type1})\n"
                f"Type2:{self.type2str} ({self.type2})\n"
                f"HeldItem:{self.heldItem}\n"
                f"Move1:{self.move1str} ({self.move1})\n"
                f"Move2:{self.move2str} ({self.move2})\n"
                f"Move3:{self.move3str} ({self.move3})\n"
                f"Move4:{self.move4str} ({self.move4})\n"
                f"OT:{self.OT}\n"
                f"Exp:{self.exp}\n"
                f"HP EV:{self.hpEv}\n"
                f"Attack EV:{self.atkEv}\n"
                f"Defense EV:{self.defEv}\n"
                f"Speed EV:{self.spdEv}\n"
                f"Special EV:{self.spcEv}\n"
                f"HP IV:{self.hpIv}\n"
                f"Attack IV:{self.atkIv}\n"
                f"Defense IV:{self.defIv}\n"
                f"Speed IV:{self.spdIv}\n"
                f"Speed IV:{self.spcIv}\n"
                f"Move 1 PP:{self.move1pp} ({self.move1ppups} PP UPs used)\n"
                f"Move 2 PP:{self.move2pp} ({self.move2ppups} PP UPs used)\n"
                f"Move 3 PP:{self.move3pp} ({self.move3ppups} PP UPs used)\n"
                f"Move 4 PP:{self.move4pp} ({self.move4ppups} PP UPs used)\n")


class offsets:
    def __init__(self):
        self.name =  0x598 + 8192
        self.TID = 0x2605
        self.money = 0x25F3
        self.boxdata = 0x4000

offsets : offsets = offsets()

def readName(save : bytes) -> str:

    namebytes : bytes = save[offsets.name : offsets.name+11]
    name : str = ""

    for byte in namebytes:
        if byte == 0x50:
            break
        name += charmap[byte]

    return name

def readTID(save : bytes) -> int:

    TIDBytes : bytes = save[offsets.TID : offsets.TID+2]
    TID : int = int.from_bytes(TIDBytes, byteorder='big')
    return TID

def readTrainerBalance(save : bytes) -> str:

    moneyBytes : bytes = save[offsets.money : offsets.money+3]
    money = hex(int.from_bytes(moneyBytes, byteorder='big'))
    return money[2:]

def readMon(save : bytes, box : int, position : int) -> gen1Pokemon | None:

    address = offsets.boxdata + (box * 1122) + 22 + (33 * position)

    speclst = offsets.boxdata + (box * 1122) + 1 + position
    print(address)
    if save[speclst] == 255:
        return None

    pokemonBytes = save[address : address + 33]
    speciesID = pokemonBytes[0]
    curHP = int.from_bytes(pokemonBytes[1:3], byteorder='big')
    level = pokemonBytes[3]
    condition = pokemonBytes[4]
    type1 = pokemonBytes[5]
    type2 = pokemonBytes[6]
    heldItem = pokemonBytes[7]
    move1 = pokemonBytes[8]
    move2 = pokemonBytes[9]
    move3 = pokemonBytes[10]
    move4 = pokemonBytes[11]
    otid = int.from_bytes(pokemonBytes[12:14], "big")
    exp = int.from_bytes(pokemonBytes[14:17], "big")
    hpEv = int.from_bytes(pokemonBytes[17:19], "big")
    atkEv = int.from_bytes(pokemonBytes[19:21], "big")
    defEv = int.from_bytes(pokemonBytes[21:23], "big")
    spdEv = int.from_bytes(pokemonBytes[23:25], "big")
    spcEv = int.from_bytes(pokemonBytes[25:27], "big")

    AtkDefEncoded = bin(pokemonBytes[27])[2:].zfill(8)
    SpdSpcEncoded = bin(pokemonBytes[28])[2:].zfill(8)

    atkIvbin = AtkDefEncoded[:4]
    defIvbin = AtkDefEncoded[4:]
    spdIvbin = SpdSpcEncoded[:4]
    spcIvbin = SpdSpcEncoded[4:]

    hpIvbin = atkIvbin[-1] + defIvbin[-1] + spdIvbin[-1] + spcIvbin[-1]

    atkIv = int(atkIvbin, 2)
    defIv = int(defIvbin, 2)
    spdIv = int(spdIvbin, 2)
    spcIv = int(spcIvbin, 2)
    hpIv = int(hpIvbin, 2)

    move1ppEncoded = bin(pokemonBytes[29])[2:].zfill(8)
    move2ppEncoded = bin(pokemonBytes[30])[2:].zfill(8)
    move3ppEncoded = bin(pokemonBytes[31])[2:].zfill(8)
    move4ppEncoded = bin(pokemonBytes[32])[2:].zfill(8)

    move1pp = int(move1ppEncoded[2:], 2)
    move2pp = int(move2ppEncoded[2:], 2)
    move3pp = int(move3ppEncoded[2:], 2)
    move4pp = int(move4ppEncoded[2:], 2)

    move1ppups = int(move1ppEncoded[:2], 2)
    move2ppups = int(move2ppEncoded[:2], 2)
    move3ppups = int(move3ppEncoded[:2], 2)
    move4ppups = int(move4ppEncoded[:2], 2)


    return gen1Pokemon(speciesID, curHP, level, condition, type1, type2, heldItem, move1, move2, move3, move4, otid, exp, hpEv, atkEv, defEv, spdEv, spcEv, hpIv, atkIv, defIv, spdIv, spcIv, move1pp, move2pp, move3pp, move4pp, move1ppups, move2ppups, move3ppups, move4ppups)

with open("../Examples/POKEMON RED-0.sav", "rb") as f:

    file = f.read()
    print(readName(file))
    print(readTID(file))
    print(readTrainerBalance(file))
    print(readMon(file, 4, 17))