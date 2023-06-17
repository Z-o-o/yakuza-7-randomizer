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
__version__ = "0.1.3"
__license__ = "MIT"

scale_vagabonds_value = 1
seed_value = ''

def set_value(field, value):
    field = value
    # wow what a complex method

def percentageCalculator(x, y):
    r = x/y*100
    return r
    
def randomize(progress, status):

    steps = ['Processing Enemies', 
             'Shuffling Enemies', 
             'Generating Statblocks', 
             'Reassigning Enemy IDs', 
             'Generating Randomized File', 
             'Generating RMM Compatible Directory']

    try:
        import Randomizer as ra
        scale_vagabonds_value = bool(scale_vagabonds.get())
        seed_value = seed.get()
        boss_chance = int(boss_weight.get())
        if seed_value == '':
            seed_value = str(random.randrange(sys.maxsize))
        increase_progress(progress, status, steps, 0)
        root.update()

        current_directory, parser = ra.open_data_file()
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
        
        messagebox.showinfo('Success!', "Randomized!")
    except Exception as e:
        messagebox.showinfo('Error!', "ERROR: {}".format(e) + "\nLet the Mod Creator know in the YMC or on the Mod Page.")

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
root.geometry("600x320")
root.minsize(600, 320)

root.iconbitmap(os.path.join(sys._MEIPASS, 'logo.ico'))

row = Frame(root)
scale_vagabonds = IntVar(master=root, value=1)
ent = Checkbutton(root, text='Scale Vagabonds', variable=scale_vagabonds, onvalue=1, offvalue=0)
row.pack(side=TOP, fill=X, padx=5, pady=5)
ent.pack(side=TOP, fill=X)
ToolTip(ent, msg="Scale Vagabonds to what level they spawn (no level 80 vagabonds giving you 30 levels at level 12).")

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