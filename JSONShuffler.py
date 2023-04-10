#!/usr/bin/env python3
import json

__author__ = "Zennith Boerger"
__version__ = "0.1.0"
__license__ = "MIT"


def main():
    json_file = open("character_npc_soldier_personal_data.bin.json", "r")
    ## parse JSON file, obtain dictionary of all valid soldier npcs
    ## then shuffle order of dictionary and put the npcs back into the json file
    y = json.loads(json_file.read())
    print(y)


if __name__ == "__main__":
    main()