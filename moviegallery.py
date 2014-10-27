# Created: Sun 26 Oct 2014 07:51:32 AM EDT
# Modified: Sun 26 Oct 2014 03:12:45 PM EDT
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
movieGallery = couch.create('movie_gallery')


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

# Searches for movies created by same director using predefined view
def searchDirector(director_name):
    directorView = movieGallery.view("_design/movieDesign/_view/director_view")
    #pdb.set_trace()
    counter = len(directorView[director_name].rows)
    for i in range(counter):
        doc_id = directorView[director_name].rows[i].value
        print movieGallery[doc_id]


# Inserts a movie entry in the database
def insert(input):
    flag = True
    try:
        test = json.loads(input)
    except ValueError, e:
        flag = False
    if (flag == True):
        doc_id, doc_rev = movieGallery.save(input)
        print "UUID of new record is :", doc_id
    else:
        print "Invalid input format. Input must be a JSON file."

def inputOptions(input_id, query):
    if (input_id == 1):
        searchMovie(query)
    elif (input_id == 2):
        searchDirector(query)



def movieGalleryApp():
    connectMovie()
    #pdb.set_trace()
    setupDatabase()
    print "Action Index:",
    input_id = input()
    print "Input query:"
    query = raw_input()
    while (query != "0"):
        inputOptions(input_id, query)
        print "Action Index:",
        input_id = input()
        print "Input query:"
        query = raw_input()
    #del movieGallery['movie_gallery']

movieGalleryApp()





    
