# Created: Tue 04 Nov 2014 09:32:50 AM EST
# Modified: Sun 09 Nov 2014 09:35:42 AM EST
#
# Author:Manish Kanadje

import moviegallery as mg
import Tkinter
from Tkinter import *
import unicodedata as unicd


master = Tkinter.Tk()

labelfont = ('times', 20, 'bold')
labelWidget = Label(master, text = "Online Movie Gallery")
labelWidget.config(bg='white', fg='black')  
labelWidget.config(font=labelfont)           
labelWidget.config(height=1, width=20)
labelWidget.pack()


e = Entry(master, width = 80)

#e.grid(row = 0, column = 1)
#e.grid(row = 0, column = 1)
e.pack()
e.focus_set()


labelfont = ('times', 20, 'bold')
labelWidget = Label(master, text = "Query")
labelWidget.config(bg='white', fg='black')  
labelWidget.config(font=labelfont)           
labelWidget.config(height=1, width=20)
labelWidget.pack()


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
    text = e.get()

    headingLabel = createLabel("Insert or Update a Movie", insertMaster)
    headingLabel.config(font = ('times', 20, 'bold'))
    headingLabel.config(height = 3, width = 50)
    headingLabel.grid(row = 0, column = 1)
    # Label and entry for title
    titleLabel = createLabel("Title", insertMaster)
    titleLabel.grid(row = 1, column = 0)
    global titleEntry
    titleEntry = Entry(insertMaster, width = 20)
    titleEntry.grid(row = 1, column = 1)

    # Label and entry for director
    directorLabel = createLabel("Director", insertMaster)
    directorLabel.grid(row = 2, column = 0)
    global directorEntry
    directorEntry = Entry(insertMaster, width = 20)
    directorEntry.grid(row = 2, column = 1)

    # Label and entry for cast
    castLabel = createLabel("Cast", insertMaster)
    castLabel.grid(row = 3, column = 0)
    global castEntry
    castEntry = Entry(insertMaster, width = 50)
    castEntry.grid(row = 3, column = 1)

    # Label and entry for budget
    budgetLabel = createLabel("Budget", insertMaster)
    budgetLabel.grid(row = 4, column = 0)
    global budgetEntry
    budgetEntry = Entry(insertMaster, width = 20)
    budgetEntry.grid(row = 4, column = 1)


    if (text != ""):
        updateFields(text)
    # Add Button
    addButton = Button(insertMaster, text = "Add", width = 20, command = \
                       addEntry)
    addButton.grid(row = 5, column = 0)

    # Update button
    updateButton = Button(insertMaster, text = "Update", width = 20, command = \
                            updateEntry)
    updateButton.grid(row = 5, column = 1)


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


def updateFields(movieName):
    movie = mg.searchMovie(movieName)
    titleEntry.insert(0, movie['title'])
    directorEntry.insert(0, movie['director'])
    budgetEntry.insert(0, movie['budget'])
    castList = movie['cast']
    castString = ""
    for actor in castList:
        castString += unicd.normalize('NFKD', actor).encode('ascii', 'ignore')
        castString += ','
    castEntry.insert(0, castString)


    
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
    
def updateEntry():
    movie = mg.searchMovie(titleEntry.get())
    movie['director'] = directorEntry.get()
    movie['budget'] = int(budgetEntry.get())
    castString = castEntry.get()
    castList = castString.split(',')
    movie['cast'] = castList
    mg.movieGallery[movie['_id']] = movie
    callbackMovieSearch()


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

insertButton = Button(master, text = "Insert or Update Movie", width = 20, \
                        command = insertMovie)
insertButton.pack()

#updateButton = Button(master, text = "Update Movie", width = 20, command = \
#                      updateMovieEntry)
#updateButton.pack()

quitButton = Button(master, text = "Quit", width = 20, command = \
                    quitApplication)
quitButton.pack()

projectInfo = createLabel("This project manages a movie \n database using " \
                          "CouchDB \n \n Manish Kanadje \n Isankumar Fulia \n" \
                          + "Varun Basappa", master) 
projectInfo.config(height = 0, width = 25)
projectInfo.pack()

mainloop()


