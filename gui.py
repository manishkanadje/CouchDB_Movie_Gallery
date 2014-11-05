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


# Internal insertion frame variable
insertMaster = None
titleEntry = None
directorEntry = None
castEntry = None
budgetEntry = None


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

def callbackData():
    mg.setupDatabase()

def callbackDeleteMovie():
    text = e.get()
    result = mg.deleteMovie(text)
    displayPanel.delete(1.0, Tkinter.END)
    displayPanel.insert(Tkinter.INSERT, result)

def quitApplication():
    global master
    master.quit()

def insertMovie():
    global insertMaster
    insertMaster = Tkinter.Tk()

    # Label and entry for title
    titleLabel = createLabel("Title", insertMaster)
    titleLabel.grid(row = 0, column = 0)
    global titleEntry
    titleEntry = Entry(insertMaster, width = 20)
    titleEntry.grid(row = 0, column = 1)

    # Label and entry for director
    directorLabel = createLabel("Director", insertMaster)
    directorLabel.grid(row = 1, column = 0)
    global directorEntry
    directorEntry = Entry(insertMaster, width = 20)
    directorEntry.grid(row = 1, column = 1)

    # Label and entry for cast
    castLabel = createLabel("Cast", insertMaster)
    castLabel.grid(row = 2, column = 0)
    global castEntry
    castEntry = Entry(insertMaster, width = 50)
    castEntry.grid(row = 2, column = 1)

    # Label and entry for budget
    budgetLabel = createLabel("Budget", insertMaster)
    budgetLabel.grid(row = 3, column = 0)
    global budgetEntry
    budgetEntry = Entry(insertMaster, width = 20)
    budgetEntry.grid(row = 3, column = 1)

    # Add Button
    addButton = Button(insertMaster, text = "Add", width = 20, command = \
                       addEntry)
    addButton.grid(row = 4, column = 0)

def addEntry():
    movieDict = {}
    movieDict['title'] = titleEntry.get()
    movieDict['director'] = directorEntry.get()
    movieDict['budget'] = budgetEntry.get()
    castString = castEntry.get()
    castList = castString.split(",")
    movieDict['cast'] = castList
    idNo, revNo = mg.movieGallery.save(movieDict)
    result = titleEntry.get() + " movie was added with UUID " + str(idNo)
    displayPanel.delete(1.0, Tkinter.END)
    displayPanel.insert(INSERT, result)
    

# Creates new label with given text
def createLabel(inputText, canvas):
    labelfont = ('times', 14)
    labelWidget = Label(canvas, text = inputText)
    labelWidget.config(bg='white', fg='black')  
    labelWidget.config(font=labelfont)           
    labelWidget.config(height=3, width=20)
    return labelWidget

movie = Button(master, text="Search Movie", width=20, command=callbackMovieSearch)
movie.pack()

director = Button(master, text="Search Director", width=20, 
command=callbackDirectorSearch)
director.pack()

budget = Button(master, text="Search Budget", width=20, command=callbackBudgetSearch)
budget.pack()

database = Button(master, text = "Create Database", width = 20, command = \
                  callbackData)
database.pack()

delMovie = Button(master, text = "Delete a Movie", width = 20, command = \
                  callbackDeleteMovie)
delMovie.pack()

quitButton = Button(master, text = "Quit", width = 20, command = \
                    quitApplication)
quitButton.pack()

insertButton = Button(master, text = "Insert Movie", width = 20, command = \
                      insertMovie)
insertButton.pack()

mainloop()
#e = Entry(master, width=100)
#e.pack()

#text = e.get()


