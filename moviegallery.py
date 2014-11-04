# Created: Sun 26 Oct 2014 07:51:32 AM EDT
# Modified: Tue 04 Nov 2014 03:49:23 PM EST
#
# Creates a CouchDB doucment. Put it into the database. Add movies from the 
# The Movie Database. Create a view.
# Author : Manish Kanadje

import pdb
import couchdb
import tmdb3
from tmdb3 import *
import unicodedata as unicd
import json

designDocID = "_design/movieDesign"
couch = couchdb.Server('http://127.0.0.1:5984')
couch.config()["query_server_config"]["reduce_limit"] = "false"
#movieGallery = couch.create('movie_gallery')
movieGallery = couch['movie_gallery']


# Creates a dictionary from data fetched from The Movie Database
def createDict(movie_id):
    movie = tmdb3.Movie(movie_id)
    movieDict = {}
    movieDict['title'] = unicd.normalize('NFKD', movie.title).encode('ascii', \
                                'ignore')
    movieDict['budget'] = movie.budget
    genres = [unicd.normalize('NFKD', genre.name).encode('ascii', 'ignore') \
                    for genre in movie.genres]
    movieDict['genres'] = genres
    movieCast = [unicd.normalize('NFKD', person.name).encode('ascii', \
                    'ignore') for person in movie.cast]
    movieDict['cast'] = movieCast
    movieDict['director'] = movie.crew[0].name
    return movieDict

# Name of directors whose total budget is higher than given value
def budgetDirectors(director):
    map_fun = '''function(doc) { emit(doc.director, doc.budget);}'''
    reduce_fun = '''function(key, value, reduce) { return sum(value);}'''
    tempView = movieGallery.query(map_fun, reduce_fun)
    result = tempView[director].rows[0].value
    print "Total budget of director ", director, " is ", result
    return ("Total budget of director ", director, " is ", result)
    

# Creates an initial CouchDB design document. Contains basic map function.
def createDesign():
    viewMap = {}
    designView = {}
    # Predefined view for search based on name
    view_1_name = "title_view"
    view_1_fields = {}
    view_1_fields["map"] = "function (doc) {emit (doc.title, doc._id);}"
    designView[view_1_name] = view_1_fields
    # Predefined view for finding movies of single director
    view_2_name = "director_view"
    view_2_fields = {}
    view_2_fields["map"] = "function (doc) {emit (doc.director, doc.title)}"
    view_2_fields["reduce"] = "function (key, value, reducer) { return value;}"
    designView[view_2_name] = view_2_fields
    # Assign views to _view in the design document
    viewMap["views"] = designView
    return viewMap

# Creates a connection with The Movie Database
def connectMovie():
    # set API key
    tmdb3.set_key('aeef209bc3d0782fbb28db3e310e8303')   
    # cache for maintaining fetch limit
    tmdb3.set_cache(filename = 'tmdb3.cache')
    # set locale information
    tmdb3.set_locale()

# Creates database. Inserts design document. Creates a new CouchDB movie 
# database with 100 movies
def setupDatabase():
    designDoc = createDesign()
    movieGallery[designDocID] = designDoc
    id = 500
    while (id < 610):
        if (idExists(id) == True):
            newMovie = createDict(id)
            movieGallery.save(newMovie)
        id += 1
        #print newMovie

# Validates that the given id is present in The Movie Database
def idExists(input_id):
    temp = tmdb3.Movie(input_id)
    try:
        tempName = temp.title
    except:
        return False
    return True


# Searches for movie by name using the predefined index
def searchMovie(movie_name):
    titleView = movieGallery.view("_design/movieDesign/_view/title_view")
    #pdb.set_trace()
    counter = len(titleView[movie_name].rows)
    for i in range(counter):
        doc_id = titleView[movie_name].rows[i].value
        print movieGallery[doc_id]
        print printMoviedetails(movieGallery[doc_id])
        return movieGallery[doc_id]

# Prints movie details in readable format
def printMoviedetails(movie):
    fields = movie.keys()
    #pdb.set_trace()
    answerString = ""
    for key in fields:
        temp = movie[key]
        newKey =  unicd.normalize('NFKD', key).encode('ascii','ignore')
        if (not(isinstance(temp, int) or isinstance(temp, list))):
            newTemp = unicd.normalize('NFKD', temp).encode('ascii','ignore')
        else:
            newTemp = str(temp)
        if (newKey == 'cast' or newKey == 'genres'):
            answerString += newKey + " : " + getListDetails(temp)
        else:
            answerString += newKey+ " : " + newTemp + "\n"
    #pdb.set_trace()
    return answerString

# Returns a string containing all the cast
def getListDetails(inputList):
    answer = ""
    for entry in inputList:
        answer += unicd.normalize('NFKD', entry).encode('ascii', 'ignore')
        answer += "\n"
    return answer


# Searches for movies created by same director using predefined view
def searchDirector(director_name):
    directorView = movieGallery.view("_design/movieDesign/_view/director_view")
    #pdb.set_trace()
    counter = len(directorView[director_name].rows)
    for i in range(counter):
        doc_list = directorView[director_name].rows[i].value
        for name in doc_list:
            print(unicd.normalize("NFKD", name).encode('ascii', 'ignore'))

# Inserts a movie entry in the database
def insert(input):
    #pdb.set_trace()
    flag = True
    try:
        temp = json.loads(input)
    except ValueError, e:
        flag = False
    if (flag == True):
        doc_id, doc_rev = movieGallery.save(temp)
        print "UUID of new movie is :", doc_id
    else:
        print "Invalid input format. Input must be a JSON file."

def delete(movie_name):
    titleView = movieGallery.view("_design/movieDesign/_view/title_view")
    counter = len(titleView[movie_name].rows)
    for i in range(counter):
        #pdb.set_trace()
        doc_id = titleView[movie_name].rows[i].value
        doc = movieGallery[doc_id]
        movieGallery.delete(doc)
        print "Deleted the movie with title :", movie_name

# Searches for movies created by same director using predefined view
def searchDirector(director_name):
    directorView = movieGallery.view("_design/movieDesign/_view/director_view")
    #pdb.set_trace()
    counter = len(directorView[director_name].rows)
    for i in range(counter):
        doc_list = directorView[director_name].rows[i].value
        print director_name, " has directed following movies"
        answerList = []
        for name in doc_list:
            tempAns = unicd.normalize('NFKD', name).encode('ascii', 'ignore')
            answerList.append(tempAns)
            print tempAns
        return answerList

def inputOptions(input_id):
    if (input_id == 1):
        print "---------------------------------------------------"
        print "Movie Name : ",
        query = raw_input()
        searchMovie(query)
        print "---------------------------------------------------"
    elif (input_id == 2):
        print "---------------------------------------------------"
        print "Director Name :",
        query = raw_input()
        searchDirector(query)
        print "---------------------------------------------------"
    elif (input_id == 3):
        print "---------------------------------------------------"
        print 'JSON string containg new movie i.e. {"title":"foo"} :',
        query = raw_input()
        insert(query)
        print "---------------------------------------------------"
    elif (input_id == 4):
        print "---------------------------------------------------"
        print "Name of the movie to be deleted :",
        query = raw_input()
        delete(query)
        print "---------------------------------------------------"
    elif (input_id == 5):
        print "---------------------------------------------------"
        print "Name of the director whose budget need to be found :",
        query = raw_input()
        budgetDirectors(query)
        print "---------------------------------------------------"

def printActionSequence():
    print "---------------------------------------------------"
    print "Action Sequence Indices: "
    print "Search Movie by Name 1"
    print "List all movies of a director 2"
    print "Insert a new movie in database 3"
    print "Delete a movie fromt database 4"
    print "Total budget of a director 5"
    print "---------------------------------------------------"
        
def movieGalleryApp():
    connectMovie()
    #pdb.set_trace()
    #setupDatabase()
    printActionSequence()
    print "Action Index:",
    input_id = input()
    '''
    while (input_id != 0):
        inputOptions(input_id)
        print "Action Index:",
        input_id = input()
    '''
    #del couch['movie_gallery']

movieGalleryApp()

