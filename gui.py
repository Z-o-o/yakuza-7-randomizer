import os
import time
import sys
from tkinter import *
from tkinter import Button, Tk, HORIZONTAL
from tkinter.ttk import Progressbar
from tkinter import messagebox

__author__ = "Zennith Boerger"
__version__ = "0.1.2"
__license__ = "MIT"

def percentageCalculator(x, y, case=1):
    """Calculate percentages
       Case1: What is x% of y?
       Case2: x is what percent of y?
       Case3: What is the percentage increase/decrease from x to y?
    """
    if case == 1:
        #Case1: What is x% of y?
        r = x/100*y
        return r
    elif case == 2:
        #Case2: x is what percent of y?
        r = x/y*100
        return r
    elif case == 3:
        #Case3: What is the percentage increase/decrease from x to y?
        r = (y-x)/x*100
        return r
    else:
        raise Exception("Only case 1,2 and 3 are available!")


def makeChecks(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        ent = Checkbutton(root, text=field, variable=scale_vagabonds, onvalue=1, offvalue=0, command=(lambda s=scale_vagabonds: print('Scale Vagabonds?: ' + str(s.get()))))
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        ent.pack(side=TOP, fill=X)
        entries.append((field, ent))
    return entries


def processEntry(entries):
    infoDict = {}
    for entry in entries:       
        field = entry[0]
        text  = entry[1].get()
        infoDict[field] = text
        
    return infoDict
    
    
def randomize(progress, status, responses):

    steps = ['Processing Enemies', 
             'Shuffling Enemies', 
             'Generating Statblocks', 
             'Reassigning Enemy IDs', 
             'Generating Randomized File', 
             'Generating RMM Compatible Directory']

    try:
        p = 0
        for i in steps:
            p += 1
            # Case2: x is what percent of y?
            unit = percentageCalculator(p, len(steps), case=2)


            step = "{}...".format(i)
            progress['value'] = unit
            percent['text'] = "{}%".format(int(unit))
            status['text'] = "{}".format(step)

            root.update()

        messagebox.showinfo('Success!', "Randomized!")
        sys.exit()


    except Exception as e:
        messagebox.showinfo('Error!', "ERROR: {}".format(e) + "\nLet the Mod Creator know in the YMC or on the Mod Page.")
        sys.exit()

    log.close()






root = Tk()
root.title("Randomizer v" + __version__)
root.geometry("600x320")

root.iconbitmap(os.path.join(os.getcwd(), 'logo.ico'))

fields = 'Randomize Vagabonds?',

scale_vagabonds = IntVar(master=root, value=1)

ents = makeChecks(root, fields)

runButton = Button(root, text='Randomize!', command=(lambda responses=ents: randomize(progress, status, responses)))
percent = Label(root, text="", anchor=S) 
progress = Progressbar(root, length=500, mode='determinate')    
status = Label(root, text="", relief=SUNKEN, anchor=W, bd=2)


runButton.pack(pady=15)
percent.pack()
progress.pack()
status.pack(side=BOTTOM, fill=X)

root.mainloop()