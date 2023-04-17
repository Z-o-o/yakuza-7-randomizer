#!/usr/bin/env python3
import ijson
import re
import random
import sys
import msvcrt as m
import reARMP as rearmp
import os

__author__ = "Zennith Boerger"
__version__ = "0.1.0"
__license__ = "MIT"

# Total enemy count including invalid/test enemies
_ENEMYCOUNT = 18028
# IDs to ignore so that no shenanigans happen like Mr Masochist replacing a boss
"""
Current list of unrandomized enemies (in-order):
    1. Mr. Masochist
    2. Masato Arakawa
    3. Ishioda Wrecking Ball
    4. Normal Majima
    5. Normal Saejima
    6. Normal Kiryu
    7 + 8. Right and Left Arm Enemies of the cleaning bot
"""
_IGNORED_IDS = ['15363', '17186', '15435', '15603', '15604', '15640', '15668', '15483']

class Enemy:
    def __init__(self, base_id, scale_id, name, stats, scaled_stats):
        self.base_id = base_id
        self.scale_id = scale_id
        self.name = name
        self.stats = stats
        self.scaled_stats = scaled_stats

def get_id(enemy):
    if enemy.base_id == '':
        return -1
    return int(enemy.base_id)

def wait():
    m.getch()

def scale_enemy(soldier, valid_soldiers, scale_enemy_id):
    stat_names = ['mission', 'group', 'npc_list', 'encounter_kind', 'hp', 'enemy_level', 'exp_point', 'money_point', 'money_drop_ratio', 'job_exp_point', 'attack', 'defence', 'dodge', 'accuracy', 'mp', 'sp_attack', 'base_wait']
    invested_vagabonds = ['17203', '17989', '17205', '17204', '15701']
    soldier.scale_id = scale_enemy_id
    soldier.scaled_stats = soldier.stats.copy()
    if invested_vagabonds.count(soldier.base_id) != 0 or invested_vagabonds.count(scale_enemy_id) != 0:
        return soldier
    
    original_stats = {}
    for s in valid_soldiers:
        if s.base_id == scale_enemy_id:
            original_stats = s.stats
            break

    for stat in stat_names:
        soldier.scaled_stats[stat] = original_stats[stat]
    return soldier


def main():
    rearmp.file_path = sys.argv[1]
    # rearmp.exportFile()
    parser = ijson.parse(open(str(rearmp.file_path + '.json'), r'r', encoding="utf8"))
    # there are 18027 npc's
    soldiers = []
    index_list = []
    current_enemy = Enemy("", "", "", {}, {})
    old_progress = 0
    print(f'Processing Enemies: 0%')
    for prefix, event, value in parser:
        if event == 'end_map' and value == None:
            soldiers.append(current_enemy)
            current_enemy = Enemy("", "", "", {}, {})
            
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
    print(f'Processing Enemies: Done!\n')
    valid_soldiers = []
    for s in soldiers:
        if s.base_id == "" or s.name == "" or s.stats == {}:
            continue
        if int(s.stats['hp']) > 0 and _IGNORED_IDS.count(s.base_id) == 0:
            valid_soldiers.append(s)
            index_list.append(s.base_id)

    index_list.sort()
    random.shuffle(valid_soldiers)
    print(f'Enemies Shuffled!\n')

    print("Generating Statblocks!")
    enemy_blocks = {}
    for i in range(len(index_list)):
        enemy = valid_soldiers[i]
        enemy_block = f'  \"{index_list[i]}\": {"{"}\n'
        enemy = scale_enemy(enemy, valid_soldiers, index_list[i])
        enemy_block += f'    \"{enemy.name}\": {"{"}\n      '
        for stat in enemy.scaled_stats:
            value = enemy.scaled_stats[stat]
            if value == "reARMP_rowIndex":
                continue
            if stat == "reARMP_rowIndex":
                end_comma = ","
                if index_list[i] == '18027':
                    end_comma = ""
                enemy_block += f'\"{stat}\": {value}\n    {"}"}\n  {"}"}{end_comma}\n'
            elif stat == "reARMP_isValid":
                enemy_block += f'\"{stat}\": \"{value}\",\n      '
            else:
                enemy_block += f'\"{stat}\": {value},\n      '
        enemy_blocks[enemy.name] = enemy_block
    print("Statblocks Generated!\n")

    for soldier in valid_soldiers:
        soldiers[soldiers.index(soldier)].base_id = soldier.scale_id
    
    print("Generating shuffled JSON!")
    file_read = open(str(rearmp.file_path + '.json'), r'r', encoding="utf8")
    file_write = open(r'character_npc_soldier_personal_data.json', r'w', encoding="utf8")
    line = ""
    while True:
        line = file_read.readline()
        if "\"1\": {" in line:
            break
        file_write.write(line)
    file_read.close()
    soldiers.sort(key=get_id)
    for s in soldiers:
        if s.base_id == "" or s.name == "" or s.stats == {}:
            continue
        if s.stats['hp'] == 0 or _IGNORED_IDS.count(s.base_id) != 0:
            enemy_block = f'  \"{s.base_id}\": {"{"}\n'
            enemy_block += f'    \"{s.name}\": {"{"}\n      '
            for stat in s.stats:
                value = s.stats[stat]
                if value == "reARMP_rowIndex":
                    continue
                if stat == "reARMP_rowIndex":
                    enemy_block += f'\"{stat}\": {value}\n    {"}"}\n  {"}"},\n'
                elif stat == "reARMP_isValid":
                    enemy_block += f'\"{stat}\": \"{value}\",\n      '
                else:
                    enemy_block += f'\"{stat}\": {value},\n      '
            file_write.write(enemy_block)
        else:
            file_write.write(enemy_blocks[s.name])

    file_write.write("}")
    file_write.close()
    print("Shuffled JSON File Created!\n")

    print("Regenerating Bin File")
    rearmp.file_path = 'character_npc_soldier_personal_data.json'
    rearmp.rebuildFile()
    print(".bin File Generated\n")

    print("Randomized! Press any key to close this window.")
    wait()


if __name__ == "__main__":
    main()