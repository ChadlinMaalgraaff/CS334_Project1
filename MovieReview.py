import requests
import json

import nltk
from nltk.corpus import movie_reviews
import random

# importing libraries for web scraping
from bs4 import BeautifulSoup
import re

# Load and prepare the dataset
import nltk
from nltk.corpus import movie_reviews
import random
from nltk.tokenize import word_tokenize

# Vader Sentiment Intensity Analyser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ----------- datacamp -------------
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

# Define the feature extractor
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)[:2000]


def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features


def wordDictionary(document):
    #words = document.split()
    #dictionary = {}

    # for word in words:
    #    dictionary.update({word: True})

    # return dictionary
    token_set = document_features(document)
    return token_set


# Train Naive Bayes classifier
featuresets = [(document_features(d), c) for (d, c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)

# ----------- datacamp -------------


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def fullReview(reviewList):
    review = ''
    for p in reviewList:
        review = review + ' ' + p

    return review


def display(obj, num):
    # displfrom vaderSentiment.vaderSentiment import SentimentIntensityAnalyzerays the movie title, opening date, date updated, author of review, & full movie review

    url = obj['link']['url']
    pageError = False
    fullReview = ''
    sentimentVader = 'None'
    DataCampSentimentAnalysis = 'None'

    try:
        request = requests.get(url)
    except:
        print("An error occured.")
        pageError = True

    if (pageError != True):
        soup = BeautifulSoup(request.text, 'html.parser')
        review = soup.find_all('p', class_='css-exrw3m evys1bk0')
        for z in range(len(review)):
            fullReview += review[z].text

        VaderSentimentAnalysis = sentiment_analyzer_scores(fullReview)
        if (VaderSentimentAnalysis['compound'] >= 0.05):
            sentimentVader = 'positive'
        elif (VaderSentimentAnalysis['compound'] > -0.05 and VaderSentimentAnalysis['compound'] < 0.05):
            sentimentVader = 'neutral'
        elif (VaderSentimentAnalysis['compound'] < -0.05):
            sentimentVader = 'negative'

        DataCampSentimentAnalysis = classifier.classify(
            wordDictionary(fullReview))

    print(' ')
    print("{:s}\n{:s}\n".format('Movie number ' +
                                str(num), len('Movie number ' + str(num))*'-'))
    print('Movie Title: ' + str(obj['display_title']))
    print(' ')
    print('Opening Date: ' + str(obj['opening_date']))
    print(' ')
    print('Date Updated: ' + str(obj['date_updated']))
    print(' ')
    print('Author of review: ' + str(obj['byline']))
    print(' ')
    print('Review: \n' + fullReview)
    print(' ')
    print('Sentimental Analysis(Vader): ' + sentimentVader)
    print(' ')
    print('Sentimental Analysis(DataCamp): ' +
          DataCampSentimentAnalysis)
    print(' ')


def displayList(obj, length):
    for i in range(0, length):
        display(obj[i], i+1)


def sortReviews(obj, length):
    # sorts the list of reviews in order from most recent to least recent: DESCENDING ORDER
    for i in range(0, length - 1):
        for j in range(1, length):
            print('openingdate i: ' + str(obj[i]['opening_date']))
            print('openingdate i: ' + str(obj[i]['opening_date']))
            print(' ')
            if (obj[i]['opening_date'] != None and obj[j]['opening_date'] != None):
                if (obj[i]['opening_date'] > obj[j]['opening_date']):
                    temp = obj[i]
                    obj[i] = obj[j]
                    obj[j] = temp
                elif (obj[i]['opening_date'] == obj[j]['opening_date']):
                    if (obj[i]['date_updated'] > obj[j]['date_updated']):
                        temp = obj[i]
                        obj[i] = obj[j]
                        obj[j] = temp


def moveNoneToBottom(obj, length):
    # Moves all null values to the bottom of the list
    newList = []
    newLength = 0
    for i in range(0, length):
        if (obj[i]['opening_date'] == None):
            newList.insert(newLength, obj[i])
        else:
            newList.insert(0, obj[i])
        newLength = newLength + 1
    for j in range(0, newLength):
        obj[j] = newList[j]


def adjustNoneValues(objList):
    for obj in objList:
        if (obj['opening_date'] == None):
            obj['opening_date'] = '0000-00-00'


def printDates(obj, length):
    for i in range(0, length):
        print('Movie ' + str(obj[i]['display_title']) + ' ' + str(i) + ': ')
        if (obj[i]['opening_date'] != None and obj[i]['date_updated'] != None):
            print('Opening date: ' + obj[i]['opening_date'])
            print('Date updated: ' + obj[i]['date_updated'])
        elif (obj[i]['opening_date'] == None and obj[i]['date_updated'] != None):
            print('Opening date: ' + 'None')
            print('Date updated: ' + obj[i]['date_updated'])
        elif (obj[i]['opening_date'] != None and obj[i]['date_updated'] == None):
            print('Opening date: ' + obj[i]['opening_date'])
            print('Date updated: ' + 'None')
        elif (obj[i]['opening_date'] == None and obj[i]['date_updated'] == None):
            print('Opening date: ' + 'None')
            print('Date updated: ' + 'None')
        print(' ')

# Using Vader to do a sentimental analysis


def sentiment_analyzer_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(sentence)
    #print("{:-<40} {}".format(sentence, str(score)))
    return score


reviews = requests.get(
    "https://api.nytimes.com/svc/movies/v2/reviews/all.json?api-key=XJofZ2M4SMvMkP29EjpJx6afnLhkzdIh")

status_code = reviews.status_code
num_results = reviews.json()['num_results']
has_more = reviews.json()['has_more']
results = reviews.json()['results']
# moveNoneToBottom(results, num_results)  # Move null values to bottom first

adjustNoneValues(results)
# Copy the first 15 results from results to list
list = []
for i in range(0, 20):
    list.append(results[i])
# Sorts list in Descending order
list = sorted(list, key=lambda k: (
    k['opening_date'], k['date_updated']), reverse=True)

for item in list:
    print(' ')
    print(str(item['display_title']))
    print(str(item['opening_date']))
    print(str(item['date_updated']))
    print(' ')

displayList(list, 15)

#print(' ')
# print(str(test_set))

# train classifier
# make a function that takes each word in the doc, places it in a tuple ('word', True), and places it in a list. Do this for every word; basically creates a dictionary of words
# use function classifier.classify(dictionaryOfWords)

# print('Classifier: ' +
#      classifier.classify(wordDictionary("Good. Love the movie.")))

#printDates(results, 20)
