import os
import time
import sys
from tkinter import *
from tkinter import Button, Tk, HORIZONTAL
from tkinter.ttk import Progressbar
from tkinter import messagebox
from tktooltip import ToolTip

__author__ = "Zennith Boerger"
__version__ = "0.1.2"
__license__ = "MIT"

scale_vagabonds_value = 1

def percentageCalculator(x, y):
    r = x/y*100
    return r

def processEntry(entries):
    infoDict = {}
    for entry in entries:       
        field = entry[0]
        text  = entry[1].get()
        infoDict[field] = text
        
    return infoDict
    
    
def randomize(progress, status):

    steps = ['Processing Enemies', 
             'Shuffling Enemies', 
             'Generating Statblocks', 
             'Reassigning Enemy IDs', 
             'Generating Randomized File', 
             'Generating RMM Compatible Directory']

    try:
        import Randomizer as ra
        ra.set_scale_vagabonds(scale_vagabonds_value)
        step = "{}...".format(steps[0])
        unit = percentageCalculator(0, len(steps))
        progress['value'] = unit
        percent['text'] = "{}%".format(int(unit))
        status['text'] = "{}".format(step)
        current_directory, parser = ra.open_data_file()

        soldiers, index_list = ra.parse_enemies(parser)

        valid_soldiers = ra.filter_soldiers(soldiers, index_list)
        step = "{}...".format(steps[1])
        unit = percentageCalculator(1, len(steps))
        progress['value'] = unit
        percent['text'] = "{}%".format(int(unit))
        status['text'] = "{}".format(step)

        valid_soldiers = ra.shuffle_enemies(index_list, valid_soldiers).copy()
        step = "{}...".format(steps[2])
        unit = percentageCalculator(2, len(steps))
        progress['value'] = unit
        percent['text'] = "{}%".format(int(unit))
        status['text'] = "{}".format(step)

        enemy_blocks = ra.generate_statblock(index_list, valid_soldiers)
        step = "{}...".format(steps[3])
        unit = percentageCalculator(2, len(steps))
        progress['value'] = unit
        percent['text'] = "{}%".format(int(unit))
        status['text'] = "{}".format(step)

        soldiers = ra.reassign_ids(soldiers, valid_soldiers).copy()

        step = "{}...".format(steps[4])
        unit = percentageCalculator(4, len(steps))
        progress['value'] = unit
        percent['text'] = "{}%".format(int(unit))
        status['text'] = "{}".format(step)
        ra.generate_json(soldiers, enemy_blocks)

        ra.repackage()
        step = "{}...".format(steps[5])
        unit = percentageCalculator(5, len(steps))
        progress['value'] = unit
        percent['text'] = "{}%".format(int(unit))
        status['text'] = "{}".format(step)

        ra.generate_RMM_directory(current_directory)
        unit = percentageCalculator(6, len(steps))
        progress['value'] = unit
        percent['text'] = "{}%".format(int(unit))
        status['text'] = "{}".format(step)

        root.update()
        messagebox.showinfo('Success!', "Randomized!")
        sys.exit()
    except Exception as e:
        messagebox.showinfo('Error!', "ERROR: {}".format(e) + "\nLet the Mod Creator know in the YMC or on the Mod Page.")

def set_value(field, value):
    field = value
    # wow what a complex method

root = Tk()
root.title("Randomizer v" + __version__)
root.geometry("600x320")

# root.iconbitmap('logo.ico')

row = Frame(root)
scale_vagabonds = IntVar(master=root, value=1)
ent = Checkbutton(root, text='Scale Vagabonds', variable=scale_vagabonds, onvalue=1, offvalue=0, command=(lambda s=scale_vagabonds: set_value(scale_vagabonds_value, s.get())))
row.pack(side=TOP, fill=X, padx=5, pady=5)
ent.pack(side=TOP, fill=X)
ToolTip(ent, msg="Scale Vagabonds to what level they spawn (no level 80 vagabonds giving you 30 levels at level 12).")

runButton = Button(root, text='Randomize!', command=(lambda : randomize(progress, status)))
percent = Label(root, text="", anchor=S) 
progress = Progressbar(root, length=500, mode='determinate')    
status = Label(root, text="", relief=SUNKEN, anchor=W, bd=2)


runButton.pack(pady=15)
percent.pack()
progress.pack()
status.pack(side=BOTTOM, fill=X)

root.mainloop()