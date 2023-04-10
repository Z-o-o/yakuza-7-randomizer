#!/usr/bin/env python3
import ijson

__author__ = "Zennith Boerger"
__version__ = "0.1.0"
__license__ = "MIT"

_ENEMYCOUNT = (18028 - 15184)
_ENEMYDISPLACEMENT = 15184

def main():
    f = open(r'C:\Users\Zenni\Documents\GitHub\yakuza-7-randomizer\Test JSON\character_npc_soldier_personal_data.bin.json', r'r')
    # there are 18027 npc's
    for i in range(_ENEMYCOUNT):
        index = i + _ENEMYDISPLACEMENT
        soldier = ijson.items(f, '{}.item'.format(index))
        print(soldier)
    ## parse JSON file, obtain dictionary of all valid soldier npcs
    ## then shuffle order of dictionary and put the npcs back into the json file


if __name__ == "__main__":
    main()