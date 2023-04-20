#!/usr/bin/env python3
import ijson
import re
import random
import sys
import msvcrt as m
import os

__author__ = "Zennith Boerger"
__version__ = "0.1.1"
__license__ = "MIT"

# Total enemy count including invalid/test enemies
_ENEMYCOUNT = 18028
# IDs to ignore so that no shenanigans happen like Mr Masochist replacing a boss
_IGNORED_IDS = ['15363', # Mr. Masochist 
                '17186', # Masato Arakawa
                '15435', # Ishioda Wrecking Ball
                '15603', # Normal Majima
                '15604', # Normal Saejima
                '15640', # Normal Kiryu
                '15668', '17621', '17829', # Right Arm of Cleaning Robots
                '15483', '17622', '17830', # Left Arm of Cleaning Robots 
                '17828', '15216', '15648' ] # Cleaning Robots

# Enemy class for storing enemies throughout the file
class Enemy:
    def __init__(self, base_id, scale_id, name, stats, scaled_stats):
        self.base_id = base_id
        self.scale_id = scale_id
        self.name = name
        self.stats = stats
        self.scaled_stats = scaled_stats

# Sorting function based on base_id
def get_id(enemy):
    if enemy.base_id == '':
        return -1
    return int(enemy.base_id)

# wait function to stop the program until keypress
def wait():
    m.getch()

# This function utilizes a naive method of scaling enemies by simply
# copying the stats from the original enemy to the enemy replacing it.
def scale_enemy(soldier, valid_soldiers, scale_enemy_id):
    stat_names = ['mission', 'group', 'npc_list', 'encounter_kind', 'hp', 'enemy_level', 'exp_point', 'money_point', 'money_drop_ratio', 'job_exp_point', 'attack', 'defence', 'dodge', 'accuracy', 'mp', 'sp_attack', 'base_wait']
    invested_vagabonds = ['17203', '17989', '17205', '17204', '15701']
    soldier.scale_id = scale_enemy_id
    soldier.scaled_stats = soldier.stats.copy()
    
    original_stats = {}
    for s in valid_soldiers:
        if s.base_id == scale_enemy_id:
            original_stats = s.stats
            break

    if invested_vagabonds.count(soldier.base_id) != 0 or invested_vagabonds.count(scale_enemy_id) != 0:
        soldier.scaled_stats['attack'] = original_stats['attack']
        soldier.scaled_stats['sp_attack'] = original_stats['sp_attack']
        return soldier

    for stat in stat_names:
        soldier.scaled_stats[stat] = original_stats[stat]
    return soldier


def main():
    # We need to store our current location to generate the RMM folder structure where the .exe
    # was run from, since the .exe uses the root's temp folder for processing.
    current_directory = os.getcwd()
    os.chdir(sys._MEIPASS)
    parser = ijson.parse(open(r'character_npc_soldier_personal_data.bin.json', r'r', encoding="utf8"))
    # We process the JSON file to retrieve the base_id, name, and stats of the current enemy, such as True 
    # Final Millenium Tower Amon (base_id = '17790', name = 'yazawa_sfm_boss_amon', stats = Lots of stuff). 
    # While doing so, we keep the user updated on progress to ensure everything is working correctly.
    soldiers = []
    index_list = []
    current_enemy = Enemy("", "", "", {}, {})
    old_progress = 0
    print(f'Processing Enemies: 0.00%')
    for prefix, event, value in parser:
        if event == 'end_map' and value == None:
            soldiers.append(current_enemy)
            current_enemy = Enemy("", "", "", {}, {})
            
        if re.match(r'^[0-9]+$', prefix) and event == 'map_key':
            new_progress = int(re.search(r'\d+', prefix).group())/_ENEMYCOUNT
            if (new_progress - old_progress) >= 0.05:
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

    print(f'Processing Enemies: 100%')
    print(f'Processing Enemies: Done!\n')

    # Now we process soldiers to filter out all test/invalid enemies (enemies who have 0 hp in the files)
    # We also keep track of what indexes are "valid" indexes for future processing as well
    valid_soldiers = []
    for s in soldiers:
        # there are a lot of blank soldiers, either due to a processing error I make or just how ijson parses the file
        # but either way we don't want them so we skip them
        if s.base_id == "" or s.name == "" or s.stats == {}:
            continue
        # check to see if the enemy is test/invalid/ignored
        if int(s.stats['hp']) > 0 and _IGNORED_IDS.count(s.base_id) == 0:
            valid_soldiers.append(s)
            index_list.append(s.base_id)

    index_list.sort()
    random.shuffle(valid_soldiers)
    print(f'Enemies Shuffled!\n')

    print("Generating Statblocks...")
    # We generate the statblocks for each scaled enemy here. Although a lot of hard-coding is involved to match formatting, 
    # it makes the file look good. The scale_id and scaled_stats parameters for the Enemy object are used here, and the code 
    # is easily readable despite containing many if and for statements. Look for the function explanation of scale_enemy for 
    # more information.
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

    # We reassign enemy IDs here to ensure that they are placed into the file at the enemy that they replaced.
    # Although it may be possible to bypass this by using scale_id when generating the new JSON file, it currently 
    # works fine, so we don't need to fix it.
    print("Reassigning enemy IDs...")
    for soldier in valid_soldiers:
        soldiers[soldiers.index(soldier)].base_id = soldier.scale_id
    print("ID's Reassigned\n")
    
    # Here is where we generate a brand new JSON for our randomizes enemies
    print("Generating shuffled JSON...")
    file_read = open(r'character_npc_soldier_personal_data.bin.json', r'r', encoding="utf8")
    file_write = open(r'character_npc_soldier_personal_data.json', r'w', encoding="utf8")
    # Create and open our files
    line = ""
    while True:
        line = file_read.readline()
        if "\"1\": {" in line:
            break
        file_write.write(line)
    file_read.close()
    # Read up to the "1" enemy entry since then we can utilize soldiers
    soldiers.sort(key=get_id)
    for s in soldiers:
        # same reasoning for this check as when generating valid_soldiers
        if s.base_id == "" or s.name == "" or s.stats == {}:
            continue
        # Check if enemy is invalid/test/ignored
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

    print("Generating Randomized Bin File...")
    # Here, it appears that the Python files automatically run when imported, but this code does not execute 
    # reARMP until after the randomized JSON is generated, so it works fine. However, IDEs may complain that 
    # reARMP is not utilized. The source code has been edited for this project's purposes, but it could be 
    # improved later to be more efficient.
    import reARMP
    print(".bin File Generated!\n")

    # This is just using out current_directory we stored at the way beginning of the program's execution to store our newly
    # packaged .bin file into an RMM compatible package. Nothing too crazy here
    print("Generating RMM Compatible Directory...")
    directories = ['Randomizer/', 'db.yazawa.en/', 'en/']
    for directory in directories:
        current_directory = os.path.join(current_directory, directory)
        os.makedirs(current_directory)
    os.rename(os.path.join(sys._MEIPASS, r"character_npc_soldier_personal_data.bin"), os.path.join(current_directory, r"character_npc_soldier_personal_data.bin"))
    print("RMM Compatible Directory Generated!\n")

    print("Randomized! Press any key to close this window.")
    wait()


if __name__ == "__main__":
    main()