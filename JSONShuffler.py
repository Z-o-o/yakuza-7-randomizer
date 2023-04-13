#!/usr/bin/env python3
import ijson
import re
import random
import sys

__author__ = "Zennith Boerger"
__version__ = "0.1.0"
__license__ = "MIT"

_ENEMYCOUNT = 18028

class Enemy:
    def __init__(self, base_id, name, stats):
        self.base_id = base_id
        self.name = name
        self.stats = stats

def get_id(enemy):
    if enemy.base_id == '':
        return -1
    return int(enemy.base_id)

def main():
    parser = ijson.parse(open(str(sys.argv[1]), r'r', encoding="utf8"))
    # there are 18027 npc's
    soldiers = []
    index_list = []
    current_enemy = Enemy("", "", {})
    old_progress = 0
    for prefix, event, value in parser:
        if event == 'end_map' and value == None:
            soldiers.append(current_enemy)
            current_enemy = Enemy("", "", {})
            
        if re.match(r'^[0-9]+$', prefix) and event == 'map_key':
            new_progress = int(re.search(r'\d+', prefix).group())/_ENEMYCOUNT
            if (new_progress - old_progress) >= 0.1:
                print(f'Processing Enemies: {("%.2f" % (new_progress*100))}%')
                old_progress = new_progress
            current_enemy.name = value
            current_enemy.base_id = re.search(r'\d+', prefix).group()

        if current_enemy.name != "" and "." in prefix:
            breakoff = 0
            while (prefix[breakoff-1] != "."):
                breakoff -= 1
            key = prefix[breakoff:]
            current_enemy.stats[key] = value
        # We need to store stats and names so we can create an Enemy object when its a valid enemy.
        # We need to keep track of the stats we get and the name, then add them into the list if they are valid
        # When we determine we are at a new enemy we need to redo the process
    print(f'Processing Enemies: 100%')
    print(f'Processing Enemies: Done!')
    valid_soldiers = []
    for s in soldiers:
        if s.base_id == "" or s.name == "" or s.stats == {}:
            continue
        if int(s.stats['hp']) > 0:
            valid_soldiers.append(s)
            index_list.append(s.base_id)
    # print(index_list)
    index_list.sort()
    random.shuffle(valid_soldiers)
    print(f'Enemies Shuffled!')

    print("Generating Statblocks!")
    enemy_blocks = {}
    old_progress = 0
    for i in range(len(index_list)):
        enemy_block = f'\t\"{index_list[i]}\": {"{"}\n'
        soldiers[soldiers.index(valid_soldiers[i])].base_id = index_list[i]
        enemy_block += f'\t\t\"{valid_soldiers[i].name}\": {"{"}\n\t\t\t'
        for stat in valid_soldiers[i].stats:
            value = valid_soldiers[i].stats[stat]
            if value == "reARMP_rowIndex":
                continue
            if stat == "reARMP_rowIndex":
                end_comma = ","
                if index_list[i] == '18027':
                    end_comma = ""
                enemy_block += f'\"{stat}\": {value}\n\t\t{"}"}\n\t{"}"}{end_comma}\n'
            elif stat == "reARMP_isValid":
                enemy_block += f'\"{stat}\": \"{value}\",\n\t\t\t'
            else:
                enemy_block += f'\"{stat}\": {value},\n\t\t\t'
        enemy_blocks[valid_soldiers[i].name] = enemy_block
    print("Statblocks Generated!")
    
    print("Generating shuffled JSON!")
    fr = open(str(sys.argv[1]), r'r', encoding="utf8")
    fw = open(r'RENAME_ME.json', r'w', encoding="utf8")
    line = ""
    while True:
        line = fr.readline()
        if "\"1\": {" in line:
            break
        fw.write(line)
    soldiers.sort(key=get_id)
    current_id = 0
    for s in soldiers:
        if s.base_id == "" or s.name == "" or s.stats == {}:
            continue
        if s.stats['hp'] == 0:
            enemy_block = f'\t\"{s.base_id}\": {"{"}\n'
            enemy_block += f'\t\t\"{s.name}\": {"{"}\n\t\t\t'
            for stat in s.stats:
                value = s.stats[stat]
                if value == "reARMP_rowIndex":
                    continue
                if stat == "reARMP_rowIndex":
                    enemy_block += f'\"{stat}\": {value}\n\t\t{"}"}\n\t{"}"},\n'
                elif stat == "reARMP_isValid":
                    enemy_block += f'\"{stat}\": \"{value}\",\n\t\t\t'
                else:
                    enemy_block += f'\"{stat}\": {value},\n\t\t\t'
            fw.write(enemy_block)
        else:
            fw.write(enemy_blocks[s.name])
        current_id += 1
    fw.write("}")
    fw.close()
    print("Shuffled JSON File Created!")

    print("Randomized!")


if __name__ == "__main__":
    main()