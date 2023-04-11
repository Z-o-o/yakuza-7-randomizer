#!/usr/bin/env python3
import ijson
import re

__author__ = "Zennith Boerger"
__version__ = "0.1.0"
__license__ = "MIT"

_ENEMYCOUNT = (18028 - 15184)
_ENEMYDISPLACEMENT = 15184

class Enemy:
    def __init__(self, name, stats):
        self.name = name
        self.stats = stats



def main():
    parser = ijson.parse(open(r'C:\Users\Zenni\Documents\GitHub\yakuza-7-randomizer\Test JSON\character_npc_soldier_personal_data.bin.json', r'r', encoding="utf8"))
    # there are 18027 npc's
    valid_soldiers = []
    index_list = []
    old_prefix = ""
    old_prefix_num = 0
    valid_enemy = False
    for prefix, event, value in parser:
        
        # We need to store stats and names so we can create an Enemy object when its a valid enemy.
        # We need to keep track of the stats we get and the name, then add them into the list if they are valid
        # When we determine we are at a new enemy we need to redo the process

        # Help notes: when transition from one enemy to the other you can take advatnage of this:
        #    prefix=98.BTL09_030_05, value=None
        #    prefix=98, value=None
        #    prefix=, value=99
        #    prefix=99, value=None
        #    prefix=99, value=BTL09_030_06
        #    prefix=99.BTL09_030_06, value=None
        print("prefix={}, value={}".format(prefix, value))
        
        """prefix_num = int(re.search(r'\d+', prefix).group())
        if old_prefix == "" or old_prefix_num != prefix_num:
            old_prefix = prefix
            if valid_enemy:
                valid_soldiers.append(Enemy(enemy_name, enemy_stats))
        
        if "hp" in prefix:
            if int(value) > 0:
                valid_enemy = True"""
    print(valid_soldiers)
    print(len(valid_soldiers))
    ## parse JSON file, obtain dictionary of all valid soldier npcs
    ## then shuffle order of dictionary and put the npcs back into the json file


if __name__ == "__main__":
    main()