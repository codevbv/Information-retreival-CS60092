
import os
import math
import sys
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer 
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestCentroid
import sklearn.datasets as skld
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics
from sklearn.metrics import accuracy_score
import numpy as np


class1_train_files = []
class2_train_files = []
class1_test_files = []
class2_test_files = []

class1_train_path = os.path.join(sys.argv[1],"class1/train/")
class1_test_path = os.path.join(sys.argv[1],"class1/test/")
class2_train_path = os.path.join(sys.argv[1],"class2/train/")
class2_test_path = os.path.join(sys.argv[1],"class2/test/")


train1_data = []
train2_data = []
train_data = []
train_target_data = []

test1_data = []
test2_data = []
test_data = []
test_target_data = []

k = [1,10,100,1000,10000]


def writeOutput(fname,scoreListMNB,scoreListBNB):
    f = open(fname,'w')
    f.write("MultinomialNB classifier:\n")
    f.write("k\t\t\t 1 \t\t\t 10 \t\t\t 100\t\t\t 1000\t\t\t 10000\n")
    f.write("F1 Score\t")
    for score in scoreListMNB:
        f.write(str(score)+"\t")
    f.write("\nBernoulliNB classifier:\n")
    f.write("k\t\t\t 1 \t\t\t 10 \t\t\t 100\t\t\t 1000\t\t\t 10000\n")
    f.write("F1 Score\t")
    for score in scoreListBNB:
        f.write(str(score)+"\t")
    f.close()

def getScoreMNB(num):
    text_classifier = Pipeline([('vect', TfidfVectorizer()), ('classifier', MultinomialNB()) ])
    text_classifier.fit(train_data, train_target_data)
    predicted = text_classifier.predict(test_data)
    curScore = (metrics.f1_score(test_target_data,predicted,average='macro'))
    curScore = getFinalScoreMNB(curScore,num)
    return curScore

def getScoreBNB(num):
    text_classifier = Pipeline([('vect', TfidfVectorizer()), ('classifier', BernoulliNB()) ])
    text_classifier.fit(train_data, train_target_data)
    predicted = text_classifier.predict(test_data)
    curScore = (metrics.f1_score(test_target_data,predicted,average='macro'))
    curScore = getFinalScoreBNB(curScore,num)
    return curScore

for subdir, dirs, files in os.walk(class1_train_path):
    for file in files:
        filepath = subdir + os.sep + file
        train_target_data.append(1)
        class1_train_files.append(filepath)
def getFinalScoreMNB(s,n):
    return (s*n)/math.sqrt(n*n+1)
for f in class1_train_files:
        train1_data.append(open(f,encoding='cp437',errors='ignore').read())

for subdir, dirs, files in os.walk(class2_train_path):
    for file in files:
        filepath = subdir + os.sep + file
        train_target_data.append(2)
        class2_train_files.append(filepath)
def getFinalScoreBNB(s,n):
    return (s*n)/math.sqrt(n*n+n)
for f in class2_train_files:
        train2_data.append(open(f,encoding='cp437',errors='ignore').read())

train_data  = train1_data + train2_data


for subdir, dirs, files in os.walk(class1_test_path):
    for file in files:
        filepath = subdir + os.sep + file
        test_target_data.append(1)
        class1_test_files.append(filepath)

for f in class1_test_files:
        test1_data.append(open(f,encoding='cp437',errors='ignore').read())

for subdir, dirs, files in os.walk(class2_test_path):
    for file in files:
        filepath = subdir + os.sep + file
        test_target_data.append(2)
        class2_test_files.append(filepath)

for f in class2_test_files:
        test2_data.append(open(f,encoding='cp437',errors='ignore').read())

test_data  = test1_data + test2_data



scoreMNB = []
for val in k:
    scoreMNB.append(getScoreMNB(val))

scoreBNB = []
for val in k:
    scoreBNB.append(getScoreBNB(val))

writeOutput(sys.argv[2],scoreMNB,scoreBNB)







