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
                '15620', # Ch.13 Sawashiro
                '15640', # Normal Kiryu
                '15647', # Ryo Aoki
                '15210', # Clara-chan fight
                '17621', '17829', # Right Arm of Cleaning Robots
                '17622', '17830', # Left Arm of Cleaning Robots 
                '17828', '15216', # Cleaning Robots
                '17990', # True Final Millenium Tower Amon
                '17991', # Summoned Majima
                '17992', # Summoned Saejima
                '17993', # Summoned Kiryu
                '16532', '16522' # Placeholder party members
                ]

# Enemy class for storing enemies throughout the file
class Enemy:
    def __init__(self, base_id, scale_id, name, stats, scaled_stats):
        self.base_id = base_id
        self.scale_id = scale_id
        self.name = name
        self.stats = stats
        self.scaled_stats = scaled_stats
    #def __copy__(self):
        #return Enemy(self.base_id, self.scale_id, self.name, self.stats, self.scaled_stats)
    def __copy__(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

# Sorting function based on base_id
def get_id(enemy):
    if enemy.base_id == '':
        return -1
    return int(enemy.base_id)

# This function utilizes a naive method of scaling enemies by simply
# copying the stats from the original enemy to the enemy replacing it.
# there is additional logic for dealing with Invested Vagabonds but for the most part
# this is how the scaling works
def scale_enemy(soldier, soldier_data, scale_enemy_id, scale_vagabonds):
    stat_names = ['mission', 'group', 'npc_list', 'encounter_kind', 'hp', 'enemy_level', 'exp_point', 'money_point', 'money_drop_ratio', 'job_exp_point', 'attack', 'defence', 'dodge', 'accuracy', 'mp', 'sp_attack', 'base_wait']
    invested_vagabonds = ['17203', '17989', '17205', '17204', '15701', '15971']
    soldier.scale_id = scale_enemy_id
    soldier.scaled_stats = soldier.stats.copy()
    same_level_enemies = []
    
    original_stats = {}
    for s in soldier_data:
        if s.base_id == scale_enemy_id:
            original_stats = s.stats
            break
    
    scaled_level = int(original_stats['enemy_level'])
    for s in soldier_data:
        if (scaled_level - 1) <= int(s.stats['enemy_level']) <= (scaled_level + 2):
            same_level_enemies.append(int(s.base_id)) 

    vagabond_scaled = (invested_vagabonds.count(soldier.base_id)) != 0
    enemy_scaled = (invested_vagabonds.count(scale_enemy_id)) != 0
    if vagabond_scaled:
        soldier.scaled_stats['attack'] = original_stats['attack']
        soldier.scaled_stats['sp_attack'] = original_stats['sp_attack']
        if scale_vagabonds:
            soldier.scaled_stats['enemy_level'] = original_stats['enemy_level']
            soldier.scaled_stats['exp_point'] = int(original_stats['exp_point'] * random.randint(10, 30))
            soldier.scaled_stats['job_exp_point'] = int(soldier.scaled_stats['exp_point'] * 0.9)
            soldier.scaled_stats['money_point'] = int(soldier.scaled_stats['exp_point'] / random.randint(20, 140))
        return soldier
    
    if enemy_scaled:
        if original_stats['enemy_level'] == 30:
            soldier.scaled_stats = scale_enemy_vagabond(soldier, 200, 400, random.randint(180, 450), 500, 1000, 162).copy()
        if original_stats['enemy_level'] == 34:
            soldier.scaled_stats = scale_enemy_vagabond(soldier, 320, 1744, 400, 800, 1300, 360).copy()
        if original_stats['enemy_level'] == 35:
            soldier.scaled_stats = scale_enemy_vagabond(soldier, 389, 666, 400, 1100, 1500, 360).copy()
        if original_stats['enemy_level'] == 41:
            soldier.scaled_stats = scale_enemy_vagabond(soldier, 798, 798, 7500, 0, 30000, 6750).copy()
        if original_stats['enemy_level'] == 50:
            soldier.scaled_stats = scale_enemy_vagabond(soldier, 984, 984, 2574, 3000, 4800, 2317).copy()
        if original_stats['enemy_level'] == 80:
            soldier.scaled_stats = scale_enemy_vagabond(soldier, 1350, 1350, 12540, 8700, 10500, 11286).copy()

    for stat in stat_names:
        if enemy_scaled and ['hp', 'exp_point', 'money_point', 'money_drop_ratio', 'job_exp_point'].count(stat) != 0:
            continue
        if soldier.scaled_stats['call_enemy_id'] != 0:
            soldier.scaled_stats['call_enemy_id'] = random.choice(same_level_enemies)
        soldier.scaled_stats[stat] = original_stats[stat]
    return soldier

# This is the method used to scale enemies that replace Vagabonds so that they don't give the same amount of XP
def scale_enemy_vagabond(soldier, hp_lower, hp_higher, exp, money_lower, money_higher, job_exp):
    soldier.scaled_stats['hp'] = int(random.randint(hp_lower, hp_higher))
    soldier.scaled_stats['exp_point'] = exp
    soldier.scaled_stats['money_point'] = int(random.randint(money_lower, money_higher))
    soldier.scaled_stats['money_drop_ratio'] = 1000
    soldier.scaled_stats['job_exp_point'] = job_exp
    return soldier.scaled_stats

# This is just using out current_directory we stored at the way beginning of the program's execution to store our newly
# packaged .bin file into an RMM compatible package. Nothing too crazy here
def generate_RMM_directory(current_directory, seed):
    seeded_name = f'Randomizer seed - {seed}/'
    current_directory = os.path.join(current_directory, seeded_name)
    os.makedirs(current_directory)
    languages = [r'de', r'en', r'es', r'fr', r'it', r'ja', r'ko', r'pt', r'ru', r'zh', r'zhs']
    for language in languages:
        rmm_directory = current_directory
        directories = [f'db.yazawa.{language}/', f'{language}/']
        for directory in directories:
            rmm_directory = os.path.join(rmm_directory, directory)
            os.makedirs(rmm_directory)
        shutil.copy(os.path.join(sys._MEIPASS, r"rpg_enemy_arts_data.bin"), os.path.join(rmm_directory, r"rpg_enemy_arts_data.bin"))
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
            file_write.write(enemy_blocks[s.name + str(s.base_id)])

    file_write.write("}")
    file_write.close()

# We reassign enemy IDs here to ensure that they are placed into the file at the enemy that they replaced.
# Although it may be possible to bypass this by using scale_id when generating the new JSON file, it currently 
# works fine, so we don't need to fix it.
def reassign_ids(soldiers, randomized):
    for soldier in randomized:
        soldiers[soldiers.index(soldier)].base_id = soldier.scale_id
    return soldiers

# We generate the statblocks for each scaled enemy here. Although a lot of hard-coding is involved to match formatting, 
# it makes the file look good. The scale_id and scaled_stats parameters for the Enemy object are used here, and the code 
# is easily readable despite containing many if and for statements. Look for the function explanation of scale_enemy for 
# more information.
def generate_statblock(index_list, soldier_data, randomized, scale_vagabonds):
    enemy_blocks = {}
    index_list.sort()
    for i in range(len(index_list)):
        enemy = randomized[i]
        enemy_block = f'  \"{index_list[i]}\": {"{"}\n'
        enemy = scale_enemy(enemy, soldier_data, index_list[i], scale_vagabonds)
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
        enemy_blocks[enemy.name + str(enemy.scale_id)] = enemy_block
    return enemy_blocks

def shuffle_enemies(valid_soldiers, bosses, boss_weight, seed_value=None):
    random.seed(seed_value)
    randomized = valid_soldiers.copy()
    ushio_index = 0
    ushio = Enemy('', '', '', {}, {})
    for enemy in randomized:
        if enemy.base_id == '15220':
            ushio_index = randomized.index(enemy)
            ushio = enemy.__copy__()
            break
    bosses_copy = bosses.copy()
    for enemy in randomized:
        if random.randint(1, 100) <= boss_weight:
            if len(bosses_copy) == 0:
                bosses_copy = bosses.copy()
            boss = random.choice(bosses_copy)
            bosses_copy.remove(boss)
            for b in bosses_copy:
                if b.stats['name'] == boss.stats['name']:
                    bosses_copy.remove(b)
            randomized[randomized.index(enemy)].name = boss.name
            randomized[randomized.index(enemy)].stats = boss.stats.copy()
    random.shuffle(randomized)
    if int(randomized[ushio_index].stats['life_gauge_type']) == 3:
        randomized[ushio_index].base_id = ushio.base_id
        randomized[ushio_index].scale_id = ushio.scale_id
        randomized[ushio_index].name = ushio.name
        randomized[ushio_index].stats = ushio.stats
        randomized[ushio_index].scaled_stats = ushio.scaled_stats

    return valid_soldiers, randomized.copy()

# Now we process soldiers to filter out all test/invalid enemies (enemies who have 0 hp in the files)
# We also keep track of what indexes are "valid" indexes for future processing as well
def filter_soldiers(soldiers, index_list):
    soldier_data = []
    valid_soldiers = []
    bosses = []
    bosses_list = ['15603', '15604', '15640', '15210']
    for s in soldiers:
        # there are a lot of blank soldiers, either due to a processing error I make or just how ijson parses the file
        # but either way we don't want them so we skip them
        if s.base_id == "" or s.name == "" or s.stats == {}:
            continue
        # check to see if the enemy is test/invalid/ignored
        if bosses_list.count(s.base_id) != 0:
            bosses.append(s)
        if int(s.stats['hp']) > 0 and _IGNORED_IDS.count(s.base_id) == 0:
            soldier_data.append(s.__copy__())
            valid_soldiers.append(s)
            index_list.append(s.base_id)
            if int(s.stats['life_gauge_type']) == 3:
                bosses.append(s)
    return valid_soldiers, soldier_data, bosses

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
