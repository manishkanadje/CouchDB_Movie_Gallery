# Created: Tue 04 Nov 2014 09:32:50 AM EST
# Modified: Tue 04 Nov 2014 11:16:05 AM EST
#
# Author:Manish Kanadje

import moviegallery as mg
import Tkinter
from Tkinter import *

master = Tkinter.Tk()

e = Entry(master)
e.pack()

e.focus_set()


# Creates a text field for displaying on-screen text
displayPanel = Text(master)
displayPanel.pack()

def callbackMovieSearch():
    text = e.get()
    result = mg.searchMovie(text)
    displayPanel.delete(1.0, Tkinter.END)
    displayPanel.insert(INSERT, result)

def callbackDirectorSearch():
    text = e.get()
    resultList = mg.searchDirector(text)
    displayPanel.delete(1.0, Tkinter.END)
    ansString = text + " has directed following movies"
    displayPanel.insert(Tkinter.END, ansString)
    displayPanel.insert(Tkinter.END, "\n")
    for result in resultList:
        displayPanel.insert(Tkinter.END, result)
        displayPanel.insert(Tkinter.END, "\n")

def callbackBudgetSearch():
    text = e.get()
    result = mg.searchMovie(text)
    displayPanel.delete(1.0, Tkinter.END)
    displayPanel.insert(INSERT, result)


movie = Button(master, text="Search Movie", width=10, command=callbackMovieSearch)
movie.pack()

director = Button(master, text="Search Director", width=10, 
command=callbackDirectorSearch)
director.pack()

budget = Button(master, text="Search Budget", width=10, command=callbackBudgetSearch)
budget.pack()


mainloop()
e = Entry(master, width=50)
e.pack()

text = e.get()


