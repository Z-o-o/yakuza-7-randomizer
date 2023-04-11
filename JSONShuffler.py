#!/usr/bin/env python3
import ijson
import re

__author__ = "Zennith Boerger"
__version__ = "0.1.0"
__license__ = "MIT"

_ENEMYCOUNT = 18028
_ENEMYDISPLACEMENT = 15184

class Enemy:
    def __init__(self, base_id, name, stats):
        self.base_id = base_id
        self.name = name
        self.stats = stats



def main():
    parser = ijson.parse(open(r'C:\Users\Zenni\Documents\GitHub\yakuza-7-randomizer\Test JSON\character_npc_soldier_personal_data.bin.json', r'r', encoding="utf8"))
    # there are 18027 npc's
    soldiers = []
    index_list = []
    current_enemey = Enemy("", "", {})
    old_progress = 0
    for prefix, event, value in parser:
        if event == 'end_map' and value == None:
            index_list.append(prefix)
            soldiers.append(current_enemey)
            current_enemey = Enemy("", "", {})
            
        if re.match(r'^[0-9]+$', prefix) and event == 'map_key':
            new_progress = int(re.search(r'\d+', prefix).group())/_ENEMYCOUNT
            if (new_progress - old_progress) >= 0.011:
                print(f'Progress {new_progress}')
                old_progress = new_progress
            current_enemey.name = value
            current_enemey.base_id = re.search(r'\d+', prefix).group()

        if current_enemey.name != "" and "." in prefix:
            breakoff = 0
            while (prefix[breakoff-1] != "."):
                breakoff -= 1
            key = prefix[breakoff:]
            current_enemey.stats[key] = value
        # We need to store stats and names so we can create an Enemy object when its a valid enemy.
        # We need to keep track of the stats we get and the name, then add them into the list if they are valid
        # When we determine we are at a new enemy we need to redo the process
    valid_soldiers = []
    for s in soldiers:
        if s.base_id == "" or s.name == "" or s.stats == {}:
            continue
        if s.stats['hp'] > 0:
            valid_soldiers.append(Enemy(s.base_id, s.name, s.stats))
    for s in valid_soldiers:
        print("base_id = {}, name = {}, hp = {}".format(s.base_id, s.name, s.stats['hp']))
    print(len(valid_soldiers))
    ## parse JSON file, obtain dictionary of all valid soldier npcs
    ## then shuffle order of dictionary and put the npcs back into the json file


if __name__ == "__main__":
    main()