#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import pandas as pd
import os
import shutil
from tkinter import filedialog as tkFileDialog

verblist = []
verblist_buffer = []
dataFilepath = "./data/Farkenheitz_verb_en.csv"

version = "0.1.0"

def clearlabels():
    output_label_verb["text"] = ""
    output_label_pronounce["text"] = ""
    output_label_typeA["text"] = ""
    output_label_typeB["text"] = ""
    output_label_typeC["text"] = ""
    output_label_typeD["text"] = ""
    output_label_meanings["text"] = ""

def search():
    verblist.clear()
    verblist_buffer.clear()
    word = search_inputbox.get()
    lb.delete(0, tk.END)
    clearlabels()
    if len(word) > 0:
        verb_Dataframe = pd.read_csv(filepath_or_buffer = dataFilepath)
        search_output_df = verb_Dataframe.query('verb.str.contains(@word,case=False)|meanings.str.contains(@word,case=False)',engine='python')
        search_output_list = search_output_df.values.tolist()
        verbnum = len(search_output_list)
        if verbnum == 0:
            output_label_verb["text"] = "No results"
        else:
            output_label_verb["text"] = "Enter a serch word"
            for verbs in range(verbnum):
                lb.insert(tk.END, str("  "+search_output_list[verbs][1]))
                verblist_buffer.append(search_output_list[verbs])
    else:
        output_label_verb["text"] = "No results"

def replaceDatabase():
    replaceFiledir=tkFileDialog.askopenfilename()
    if os.path.exists(dataFilepath) == False:
        os.mkdir("./data")
    shutil.copyfile(replaceFiledir,dataFilepath)

def exportDatabase():
    exportFiledir=tkFileDialog.askdirectory()
    shutil.copy(dataFilepath,exportFiledir)

def listClick():
    verbselect = 0
    for i in lb.curselection():
        verbselect = i

    output_label_verb["text"] = str(verblist_buffer[verbselect][1])
    output_label_pronounce["text"] = str(verblist_buffer[verbselect][2])
    output_label_typeA["text"] = str("▸"+verblist_buffer[verbselect][3])
    output_label_typeB["text"] = str("▸"+verblist_buffer[verbselect][4])
    output_label_typeC["text"] = str("▸"+verblist_buffer[verbselect][5])
    # output_label_typeD["text"] = str("▸"+verblist_buffer[verbselect][6])
    output_label_meanings["text"] = str("意味 : "+verblist_buffer[verbselect][7])

root = tk.Tk()
root.minsize(width=600,height=400)
root.resizable(0,0)
root.title("Farkenheitzef Eihensùr")

# making manubar
menubar = tk.Menu(root)
root.configure(menu = menubar)
# filemenu type
filemenu = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "General", menu = filemenu)
# indexes
filemenu.add_command(label = "Add words (Not implemented)")
filemenu.add_command(label = "Add word database (Not implemented)")
filemenu.add_command(label = "Replace word database (CAUTION!)", command = replaceDatabase)
filemenu.add_command(label = "Export word database", command = exportDatabase)
# index separator
filemenu.add_separator()
filemenu.add_command(label = "Exit", command = lambda: root.destroy())

frame = tk.Frame(root, borderwidth=0, bg='white')
frame.pack()

frame_search = tk.Frame(
    frame, width=600, height=90,
    borderwidth=1, relief='flat', bg="#bbbbbb")

search_button = tk.Button(root, text = "  Bufwalt  ", command = search)
search_button.place(x=470,y=32.5)

search_inputbox = tk.Entry(width = 40)
search_inputbox.place(x=70,y=30)

frame_search.grid(row = 1,column = 0, columnspan = 3, sticky = tk.W + tk.E)

scroll=tk.Scrollbar(frame, orient=tk.VERTICAL)

list_value=tk.StringVar()
list_value.set(verblist)
lb= tk.Listbox(frame, listvariable=list_value, width=20,height=20,borderwidth=0,selectmode="single", yscrollcommand=scroll.set, bg="#dddddd")
lb.bind('<<ListboxSelect>>', lambda e: listClick())
lb.grid(row = 2, column = 0)

scroll["command"]=lb.yview
scroll.grid(row = 2,column = 1, sticky = tk.N + tk.S)

frame2 = tk.Frame(
    frame, width=400, height=330,
    borderwidth=0, relief='solid')
frame2.grid(row = 2, column = 2)

output_label_verb = tk.Label(frame2, text="No results", font = ("", "20", "bold"), anchor=tk.E)
output_label_verb.place(x=10, y=10)

output_label_pronounce = tk.Label(frame2, anchor=tk.E)
output_label_pronounce.place(x=10, y=40)

output_label_typeA = tk.Label(frame2, anchor=tk.E)
output_label_typeA.place(x=10, y=60)

output_label_typeB = tk.Label(frame2, anchor=tk.E)
output_label_typeB.place(x=90, y=60)

output_label_typeC = tk.Label(frame2, anchor=tk.E)
output_label_typeC.place(x=170, y=60)

output_label_typeD = tk.Label(frame2, anchor=tk.E)
output_label_typeD.place(x=250, y=60)

output_label_meanings = tk.Label(frame2, font=("", "15", ""), anchor=tk.E)
output_label_meanings.place(x=10, y=90)

root.mainloop()
