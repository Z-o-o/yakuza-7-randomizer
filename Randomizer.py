#!/usr/bin/env python3
import ijson
import re
import random
import sys
import msvcrt as m
import os
import shutil

__author__ = "Zennith Boerger"
__version__ = "0.1.3"
__license__ = "MIT"

# Total enemy count including invalid/test enemies (not currently utilized)
_ENEMYCOUNT = 18028
# IDs to ignore so that no shenanigans happen like Mr Masochist replacing a boss
_IGNORED_IDS = ['15363', # Mr. Masochist 
                '17186', # Masato Arakawa
                '15435', # Ishioda Wrecking Ball
                '15603', # Normal Majima
                '15604', # Normal Saejima
                '15640', # Normal Kiryu
                '17621', '17829', # Right Arm of Cleaning Robots
                '17622', '17830', # Left Arm of Cleaning Robots 
                '17828', '15216', # Cleaning Robots
                '17990' # True Final Millenium Tower Amon
                ]

scale_vagabonds = True

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

def set_scale_vagabonds(new_value):
    scale_vagabonds = new_value

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

    vagabond_scaled = (invested_vagabonds.count(soldier.base_id)) != 0
    enemy_scaled = (invested_vagabonds.count(scale_enemy_id)) != 0
    if vagabond_scaled:
        soldier.scaled_stats['attack'] = original_stats['attack']
        soldier.scaled_stats['sp_attack'] = original_stats['sp_attack']
        if scale_vagabonds:
            soldier.scaled_stats['enemy_level'] = original_stats['enemy_level']
            soldier.scaled_stats['exp_point'] = int(original_stats['exp_point'] * 10)
            soldier.scaled_stats['job_exp_point'] = int(soldier.scaled_stats['exp_point'] * 0.9)
            soldier.scaled_stats['money_point'] = int(soldier.scaled_stats['exp_point'] / random.randint(20, 140))
        return soldier

    for stat in stat_names:
        if enemy_scaled and ['hp', 'exp_point', 'money_point', 'money_drop_ratio', 'job_exp_point'].count(stat) != 0:
            continue
        soldier.scaled_stats[stat] = original_stats[stat]
    return soldier

# This is just using out current_directory we stored at the way beginning of the program's execution to store our newly
# packaged .bin file into an RMM compatible package. Nothing too crazy here
def generate_RMM_directory(current_directory):
    current_directory = os.path.join(current_directory, 'Randomizer/')
    os.makedirs(current_directory)
    languages = [r'de', r'en', r'es', r'fr', r'it', r'ja', r'ko', r'pt', r'ru', r'zh', r'zhs']
    for language in languages:
        rmm_directory = current_directory
        directories = [f'db.yazawa.{language}/', f'{language}/']
        for directory in directories:
            rmm_directory = os.path.join(rmm_directory, directory)
            os.makedirs(rmm_directory)
        shutil.copy(os.path.join(sys._MEIPASS, r"character_npc_soldier_personal_data.bin"), os.path.join(rmm_directory, r"character_npc_soldier_personal_data.bin"))

def repackage():
    import reARMP
    reARMP.rebuildFile()

# Here is where we generate a brand new JSON for our randomizes enemies
def generate_json(soldiers, enemy_blocks):
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

# We reassign enemy IDs here to ensure that they are placed into the file at the enemy that they replaced.
# Although it may be possible to bypass this by using scale_id when generating the new JSON file, it currently 
# works fine, so we don't need to fix it.
def reassign_ids(soldiers, valid_soldiers):
    for soldier in valid_soldiers:
        soldiers[soldiers.index(soldier)].base_id = soldier.scale_id
    return soldiers

# We generate the statblocks for each scaled enemy here. Although a lot of hard-coding is involved to match formatting, 
# it makes the file look good. The scale_id and scaled_stats parameters for the Enemy object are used here, and the code 
# is easily readable despite containing many if and for statements. Look for the function explanation of scale_enemy for 
# more information.
def generate_statblock(index_list, valid_soldiers):
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
    return enemy_blocks

def shuffle_enemies(index_list, valid_soldiers):
    index_list.sort()
    random.shuffle(valid_soldiers)
    return valid_soldiers

# Now we process soldiers to filter out all test/invalid enemies (enemies who have 0 hp in the files)
# We also keep track of what indexes are "valid" indexes for future processing as well
def filter_soldiers(soldiers, index_list):
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
    return valid_soldiers

# We process the JSON file to retrieve the base_id, name, and stats of the current enemy, such as True 
# Final Millenium Tower Amon (base_id = '17790', name = 'yazawa_sfm_boss_amon', stats = Lots of stuff).
def parse_enemies(parser):
    soldiers = []
    index_list = []
    current_enemy = Enemy("", "", "", {}, {})
    for prefix, event, value in parser:
        if event == 'end_map' and value == None:
            soldiers.append(current_enemy)
            current_enemy = Enemy("", "", "", {}, {})
            
        if re.match(r'^[0-9]+$', prefix) and event == 'map_key':
            current_enemy.name = value
            current_enemy.base_id = re.search(r'\d+', prefix).group()

        if current_enemy.name != "" and "." in prefix:
            breakoff = 0
            while (prefix[breakoff-1] != "."):
                breakoff -= 1
            key = prefix[breakoff:]
            current_enemy.stats[key] = value
    return soldiers,index_list

# We need to store our current location to generate the RMM folder structure where the .exe
# was run from, since the .exe uses the root's temp folder for processing.
def open_data_file():
    current_directory = os.getcwd()
    os.chdir(sys._MEIPASS)
    parser = ijson.parse(open(r'character_npc_soldier_personal_data.bin.json', r'r', encoding="utf8"))
    return current_directory,parser
