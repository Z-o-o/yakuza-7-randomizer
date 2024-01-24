#!/usr/bin/env python3
import ijson
import json
import re
import random
import sys
import msvcrt as m
import os
import shutil
import time

_SKILL_AMOUNT = 1750
_IGNORED_IDS = [243, # Tenacious Fist,
                1140, # Guard Order
                757, # Unleash Hell
                763, # Blasphemous Ritual
                853, # Foreman Demolish skill
                852, # Honey Hunt
                851, # Freelancer Treasure Hunt
                1175, # Summon Bandmate
                1503, 131, 508, 717, 722, 757, 760, 762, 800, 804, 1170, 1175, 1316, 1156, # Call Backup
                1255, 1254, 1253, 1252, 1251, 1250 # All Tag Team moves except Essence of Mayham
                ]

class Skill:
    def __init__(self, id, name, stats, new_stats):
        self.id = id
        self.name = name
        self.stats = stats
        self.new_stats = new_stats
    def copy(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

# We need to store our current location to generate the RMM folder structure where the .exe
# was run from, since the .exe uses the root's temp folder for processing.
def open_data_file():
    os.chdir(sys._MEIPASS)
    file = open(r'rpg_skill.bin.json', r'r', encoding="utf8")
    return file


def parse_skills(f):
    skills = []
    for skill_id in range(_SKILL_AMOUNT):
        # if ((skill_id/_SKILL_AMOUNT) * 100) % 10 == 0:
        #     print(str((skill_id/_SKILL_AMOUNT) * 100) + "% Complete")
        f.seek(0)
        skill = Skill('', '', {}, {})
        objects = ijson.items(f, str(skill_id))
        for stat in objects:
            skill.id = skill_id
            skill.name = list(stat.keys())[0]
            data = str(stat[list(stat.keys())[0]]).replace("'", "\"").replace("Decimal(\"", "").replace("\")", "").replace("True", "true").replace("False", "false").replace(", ", ",")
            data = data.replace('""We Are the Globe""', '"\\"We Are the Globe\\""').replace('""Scar Me""', '"\\"Scar Me\\""').replace('""Relax""', '"\\"Relax\\""').replace('""Your Wackiest Dreams""', '"\\"Your Wackiest Dreams\\""').replace('""Endless Desire""', '"\\"Endless Desire\\""').replace('""Those Who Protect""', '"\\"Those Who Protect\\""').replace('""Be My Shelter""', '"\\"Be My Shelter\\""')
            skill.stats = json.loads(data)
            skill.new_stats = skill.stats.copy()
        skills.append(skill)
    f.close()
    return skills

def shuffle_skills(skills, seed_value=None):
    random.seed(seed_value)
    mp_cost_og = []
    for skill in skills:
        mp_cost_og.append(skill.stats['need_heat'])


    valid_skills = []
    valid_skills_indexes = []
    for skill in skills:
        if skill.stats['reARMP_isValid'] == '1' and 'name' in skill.stats and skill.stats['category'] != 11 and skill.stats['use_cond'] != 30 and _IGNORED_IDS.count(skill.id) == 0:
            valid_skills.append(skill.copy())
            valid_skills_indexes.append(skill.id)
        
    random.shuffle(valid_skills)
    return mp_cost_og,valid_skills,valid_skills_indexes

def get_skills_list(skills, valid_skills, valid_skills_indexes, mp_cost_og, empty_explain=False):
    skills_list = []

    for i in range(_SKILL_AMOUNT):
        if valid_skills_indexes.count(i) != 0:
            next_skill = valid_skills.pop()
            skills_list.append(next_skill)
        else:
            skills_list.append(skills[i])
        
    for i in range(len(skills_list)):
        if mp_cost_og[i] == 0:
            skills_list[i].stats['need_heat'] = 0
        if mp_cost_og[i] > 0 and skills_list[i].stats['need_heat'] == 0:
            skills_list[i].stats['need_heat'] = random.randrange(5, 70)

    if empty_explain:
        for skill in skills_list:
            skill.stats['explain'] = ''

    return skills_list

def generate_JSON(skills_list):
    file_read = open(r'rpg_skill.bin.json', r'r', encoding="utf8")
    file_write = open(r'rpg_skill.json', r'w', encoding="utf8")

    line = ""
    while True:
        line = file_read.readline()
        if "\"0\": {" in line:
            break
        file_write.write(line)
    file_read.close()
    for i in range(_SKILL_AMOUNT):
        end_comma = ",\n"
        if i == _SKILL_AMOUNT - 1:
             end_comma = "\n"
        data = str(skills_list[i].stats).replace("'", "\"").replace("Decimal(\"", "").replace("\")", "").replace("True", "true").replace("False", "false")#.replace(", ", ",")
        data = data.replace('""We Are the Globe""', '"\\"We Are the Globe\\""').replace('""Scar Me""', '"\\"Scar Me\\""').replace('""Relax""', '"\\"Relax\\""').replace('""Your Wackiest Dreams""', '"\\"Your Wackiest Dreams\\""').replace('""Endless Desire""', '"\\"Endless Desire\\""').replace('""Those Who Protect""', '"\\"Those Who Protect\\""').replace('""Be My Shelter""', '"\\"Be My Shelter\\""')
        data = data.replace('true Grit', 'True Grit')
        data = '"' + str(skills_list[i].name) + "\": {\n      " + data[1:]
        data = data[:-1] + "\n    }\n  }"
        data = data.replace(',"', ',\n      "')
        file_write.write("  \"" + str(i) + "\": {\n    " + data + end_comma)
    file_write.write("}")
    file_write.close()

def repackage():
    import SkillreARMP
    SkillreARMP.rebuildFile()

def generate_RMM(current_directory, seed):
    seeded_name = f'Skill Randomizer seed - {seed}/'
    seeded_name = os.path.join(seeded_name, 'db.yazawa.en/')
    seeded_name = os.path.join(seeded_name, 'en/')
    current_directory = os.path.join(current_directory, seeded_name)
    os.makedirs(current_directory)
    shutil.copy(os.path.join(sys._MEIPASS, r"rpg_skill.bin"), os.path.join(current_directory, r"rpg_skill.bin"))
    # os.remove(r'rpg_skill.json')

# seed = random.randrange(sys.maxsize)
# random.seed(seed)

# current_directory, file = open_data_file()
# skills = parse_skills(file)
# mp_cost, valid_skills, valid_skills_indexes = shuffle_skills(skills, seed)
# skills_list = get_skills_list(skills, valid_skills, valid_skills_indexes, mp_cost)
# generate_JSON(skills_list)
# repackage()
# generate_RMM(current_directory, seed)