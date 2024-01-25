import os
import time
import sys
import re
import random
from tkinter import *
from tkinter import Button, Tk, HORIZONTAL
from tkinter.ttk import Progressbar
from tkinter import messagebox
from tktooltip import ToolTip

__author__ = "Zennith Boerger"
__version__ = "0.1.5"
__license__ = "MIT"

randomize_enemies_value = 1
randomize_skills_value = 1
scale_vagabonds_value = 1
seed_value = ''

def set_value(field, value):
    field = value
    # wow what a complex method

def percentageCalculator(x, y):
    r = x/y*100
    return r
    
def randomize(progress, status):

    current_directory = os.getcwd()
    randomize_enemies_value = bool(randomize_enemies.get())
    randomize_skills_value = bool(randomize_skills.get())

    if not randomize_skills_value and not randomize_enemies_value:
        messagebox.showinfo('Error', "You didn't select either randomization option.")
        return
    
    scale_vagabonds_value = bool(scale_vagabonds.get())
    seed_value = seed.get()
    boss_chance = int(boss_weight.get())
    if seed_value == '':
        seed_value = str(random.randrange(sys.maxsize))

    try:
        import EnemyRandomizer as ra
        import SkillRandomizer as sa

        if randomize_enemies_value:
            steps = ['Processing Enemies', 
                'Shuffling Enemies', 
                'Generating Statblocks', 
                'Reassigning Enemy IDs', 
                'Generating Randomized File', 
                'Generating RMM Compatible Directory']
            enemy_rando(progress, status, steps, current_directory, scale_vagabonds_value, seed_value, boss_chance, ra)
        if randomize_skills_value:
            steps = ['Processing Skills (this can take awhile)', 
                'Shuffling Skills', 
                'Generating Skills List', 
                'Generating Randomized File', 
                'Generating RMM Compatible Directory']
            skill_rando(progress, status, steps, current_directory, seed_value, sa)
            
        
        messagebox.showinfo('Success!', "Randomized!")
    except Exception as e:
        messagebox.showinfo('Error!', "ERROR: {}".format(e) + "\nLet the Mod Creator know in the YMC or on the Mod Page.")

def skill_rando(progress, status, steps, current_directory, seed_value, sa):
    increase_progress(progress, status, steps, 0)
    root.update()

    file = sa.open_data_file()
    skills = sa.parse_skills(file)
    increase_progress(progress, status, steps, 1)
    root.update()

    mp_cost, valid_skills, valid_skills_indexes = sa.shuffle_skills(skills, int(seed_value))
    increase_progress(progress, status, steps, 2)
    root.update()

    skills_list = sa.get_skills_list(skills, valid_skills, valid_skills_indexes, mp_cost, bool(empty_explain.get()))
    increase_progress(progress, status, steps, 3)
    root.update()

    sa.generate_JSON(skills_list)
    sa.repackage()
    increase_progress(progress, status, steps, 4)
    root.update()

    sa.generate_RMM(current_directory, int(seed_value))
    increase_progress(progress, status, steps, len(steps))
    root.update()

def enemy_rando(progress, status, steps, current_directory, scale_vagabonds_value, seed_value, boss_chance, ra):
    increase_progress(progress, status, steps, 0)
    root.update()

    parser = ra.open_data_file()
    soldiers, index_list = ra.parse_enemies(parser)
    valid_soldiers, soldier_data, bosses = ra.filter_soldiers(soldiers, index_list)
    increase_progress(progress, status, steps, 1)
    root.update()

    valid_soldiers, randomized = ra.shuffle_enemies(valid_soldiers, bosses, boss_chance, int(seed_value))
    increase_progress(progress, status, steps, 2)
    root.update()

    enemy_blocks = ra.generate_statblock(index_list, soldier_data, randomized, scale_vagabonds_value)
    increase_progress(progress, status, steps, 3)
    root.update()

    soldiers = ra.reassign_ids(soldiers, randomized).copy()
    increase_progress(progress, status, steps, 4)
    root.update()

    ra.generate_json(soldiers, enemy_blocks)
    ra.repackage()
    increase_progress(progress, status, steps, 5)
    root.update()

    ra.generate_RMM_directory(current_directory, int(seed_value))
    increase_progress(progress, status, steps, len(steps))
    root.update()

def increase_progress(progress, status, steps, index):
    if index < len(steps):
        step = "{}...".format(steps[index])
    else:
        step = 'Randomized!'
    unit = percentageCalculator(index, len(steps))
    progress['value'] = unit
    percent['text'] = "{}%".format(int(unit))
    status['text'] = "{}".format(step)


root = Tk()
root.title("Randomizer v" + __version__)
root.geometry("600x400")
root.minsize(600, 320)

row = Frame(root)
set_seed = Label(row, text="What do you want to randomize?:")
set_seed.pack(side=TOP)
randomize_enemies = IntVar(master=root, value=1)
ent = Checkbutton(root, text='Enemy', variable=randomize_enemies, onvalue=1, offvalue=0)
row.pack(side=TOP, fill=X, padx=5, pady=5)
ent.pack(side=TOP, fill=X)
randomize_skills = IntVar(master=root, value=1)
ent = Checkbutton(root, text='Skills', variable=randomize_skills, onvalue=1, offvalue=0)
row.pack(side=TOP, fill=X, padx=5, pady=5)
ent.pack(side=TOP, fill=X)

root.iconbitmap(os.path.join(sys._MEIPASS, 'logo.ico'))

row = Frame(root)
scale_vagabonds = IntVar(master=root, value=1)
ent = Checkbutton(root, text='Scale Vagabonds', variable=scale_vagabonds, onvalue=1, offvalue=0)
row.pack(side=TOP, fill=X, padx=5, pady=5)
ent.pack(side=TOP, fill=X)
ToolTip(ent, msg="Scale Vagabonds to what level they spawn (no level 80 vagabonds giving you 30 levels at level 12).")

empty_explain = IntVar(master=root, value=0)
ent = Checkbutton(root, text='Empty skill descriptions', variable=empty_explain, onvalue=1, offvalue=0)
row.pack(side=TOP, fill=X, padx=5, pady=5)
ent.pack(side=TOP, fill=X)
ToolTip(ent, msg="Make all skill descriptions empty (recommended for Skill Rando if you'd like more chaos).")

seed = StringVar(master=root, value='')
warning_text = StringVar(master=root, value='')
warning = Label(row, text=warning_text, fg='red')
warning['text'] = ""
warning.pack(side=TOP)

def verify_seed(var, index, mode):
    if re.match('^[0-9]*$', seed.get()):
        warning['text'] = ""
        warning.pack(side=TOP)
        set_value(seed_value, seed.get())
    else:
        warning['text'] ="Only Enter Numbers"
        warning.pack(side=TOP)
        seed.set(seed.get()[:-1])
        set_value(seed_value, seed.get()[:-1])

seed.trace_add('write', verify_seed)
set_seed = Label(row, text="Set Seed:")
ent = Entry(row, textvariable=seed)
set_seed.pack(side=TOP)
ent.pack(side=TOP)

boss_weight_text = Label(row, text="Percent chance for each enemy to be replaced by a boss (Recommend default 5-15%)")
boss_weight = Spinbox(row, from_ = 0.0, to = 100.00, format="%0.0f", wrap=True)
boss_weight_text.pack(side=TOP)
boss_weight.pack(side=TOP)

runButton = Button(root, text='Randomize!', command=(lambda : randomize(progress, status)))
percent = Label(root, text="", anchor=S) 
progress = Progressbar(root, length=500, mode='determinate')    
status = Label(root, text="", relief=SUNKEN, anchor=W, bd=2)


runButton.pack(pady=15)
percent.pack()
progress.pack()
status.pack(side=BOTTOM, fill=X)

root.mainloop()