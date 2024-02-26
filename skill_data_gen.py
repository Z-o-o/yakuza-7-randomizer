import ijson
import json
import time

_SKILL_AMOUNT = 1750

class Skill:
    def __init__(self, id, name, stats):
        self.id = id
        self.name = name
        self.stats = stats
    def copy(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

start = time.time()

f = open(r'rpg_skill.bin.json', r'r', encoding="utf8")

skills = []
for skill_id in range(_SKILL_AMOUNT):
    if int((skill_id/_SKILL_AMOUNT) * 100) % 10 == 0:
        print(str((skill_id/_SKILL_AMOUNT) * 100) + "% Complete\n")
    f.seek(0)
    skill = Skill('', '', {})
    objects = ijson.items(f, str(skill_id))
    data = ""
    for stat in objects:
        skill.id = skill_id
        skill.name = list(stat.keys())[0]
        data = str(stat[list(stat.keys())[0]]).replace("'", "\"").replace("Decimal(\"", "").replace("\")", "").replace("True", "true").replace("False", "false").replace(", ", ",")
        data = data.replace('""We Are the Globe""', '"\\"We Are the Globe\\""').replace('""Scar Me""', '"\\"Scar Me\\""').replace('""Relax""', '"\\"Relax\\""').replace('""Your Wackiest Dreams""', '"\\"Your Wackiest Dreams\\""').replace('""Endless Desire""', '"\\"Endless Desire\\""').replace('""Those Who Protect""', '"\\"Those Who Protect\\""').replace('""Be My Shelter""', '"\\"Be My Shelter\\""')
        skill.stats = json.loads(data)
    skill = "Skill(\""+str(skill.id) + "\", \"" + str(skill.name) + "\", " + str(data) + ")"
    skills.append(skill)
f.close()

print("Done Parsing.")

file_write = open(r'skill_data.py', r'w', encoding="utf8")

file_write.write("class Skill:\n\tdef __init__(self, id, name, stats):\n\t\tself.id = id\n\t\tself.name = name\n\t\tself.stats = stats\n\tdef copy(self):\n\t\tobj = type(self).__new__(self.__class__)\n\t\tobj.__dict__.update(self.__dict__)\n\t\treturn obj\n\n")
file_write.write("skills0 = [\n\t")
skill_list = []
for i in range(_SKILL_AMOUNT):
    if i % 100 == 0:
        file_write.write(']\n\nskills' + str(i) + " = [\n\t")
        skill_list.append(i)
    file_write.write(str(skills[i]) + ",\n\t")
file_write.write(']\n')

file_write.write('skills = ')

for i in skill_list:
    file_write.write('skill' + str(i) + " + ")

file_write.close()

total_time = time.time() - start

print("Done after " + str(int(total_time / 60)) + "minutes")