#!/usr/bin/env python3
import ijson

__author__ = "Zennith Boerger"
__version__ = "0.1.0"
__license__ = "MIT"

_ENEMYCOUNT = 18027

def main():
    f = open(r'C:\Users\Zenni\Documents\GitHub\yakuza-7-randomizer\Test JSON\character_npc_soldier_personal_data.bin.json', r'r')
    # there are 18027 npc's
    for i in len(range(30)):
        print(ijson.items(f, '${i}'))
    ## parse JSON file, obtain dictionary of all valid soldier npcs
    ## then shuffle order of dictionary and put the npcs back into the json file


if __name__ == "__main__":
    main()