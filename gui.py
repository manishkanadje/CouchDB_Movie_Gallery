# Created: Tue 04 Nov 2014 09:32:50 AM EST
# Modified: Tue 04 Nov 2014 12:03:22 PM EST
#
# Author:Manish Kanadje

import moviegallery as mg
import Tkinter
from Tkinter import *

master = Tkinter.Tk()
e = Entry(master, width = 80)
#Label(master, text = "Query").grid(row = 0)
e.pack()
#e.grid(row = 0, column = 1)
e.focus_set()


# Creates a text field for displaying on-screen text
displayPanel = Text(master, width = 50, bd = 10, bg = "beige")
displayPanel.pack(side = LEFT)

def callbackMovieSearch():
    text = e.get()
    result = mg.searchMovie(text)
    result = mg.printMoviedetails(result)
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
    result = mg.budgetDirectors(text)
    displayPanel.delete(1.0, Tkinter.END)
    displayPanel.insert(INSERT, result)


movie = Button(master, text="Search Movie", width=20, command=callbackMovieSearch)
movie.pack()

director = Button(master, text="Search Director", width=20, 
command=callbackDirectorSearch)
director.pack()

budget = Button(master, text="Search Budget", width=20, command=callbackBudgetSearch)
budget.pack()


mainloop()
#e = Entry(master, width=100)
#e.pack()

#text = e.get()


