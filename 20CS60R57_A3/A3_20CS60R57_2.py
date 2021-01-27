
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


class1_train_files = []
class2_train_files = []
class1_test_files = []
class2_test_files = []

class1_train_string_list_processed = []
class2_train_string_list_processed = []
class1_test_string_list_processed = []
class2_test_string_list_processed = []

final_train_class_list = []
final_test_class_list = []
final_train_string_list = []
final_test_string_list = []

numClass1Train = 0
numClass2Train = 0
numClass1Test = 0
numClass2Test = 0

class1_train_path = os.path.join(sys.argv[1],"class1/train/")
class1_test_path = os.path.join(sys.argv[1],"class1/test/")
class2_train_path = os.path.join(sys.argv[1],"class2/train/")
class2_test_path = os.path.join(sys.argv[1],"class2/test/")

def preprocess(text):

    punc = '''!()-[]{};:'"\,<>./?@#$%^=&*_~'''
    stop_words = set(stopwords.words('english')) 
    lemmatizer = WordNetLemmatizer() 
    
    lines = text.split("\n")
    my_lines = []
    for line in lines:
        for ch in line:  
            if ch in punc:  
                line = line.replace(ch," ")
        my_lines.append(line)
    
    filtered_sentence = ''
    for line in my_lines:
        word_tokens = word_tokenize(line)
        for w in word_tokens:
            if not w in stop_words:
                filtered_sentence = filtered_sentence+' '+ lemmatizer.lemmatize(w.lower())
    
    return filtered_sentence

def writeOutput(fname):
    data_classifier = Pipeline([('tfidf', TfidfVectorizer()),('clf', NearestCentroid())])
    data_classifier.fit(final_train_string_list,final_train_class_list)
    data_predicted = data_classifier.predict(final_test_string_list)
    f = open(fname,'w')
    f.write("Rocchio classifier macro F1 score for b = 0 \t")
    f.write(str(metrics.f1_score(final_test_class_list,data_predicted,average='macro'))+"\n")
    f.close()


for subdir, dirs, files in os.walk(class1_train_path):
    for file in files:
        filepath = subdir + os.sep + file
        final_train_class_list.append(1)
        class1_train_files.append(filepath)

for f in class1_train_files:
        class1_train_string_list_processed.append(preprocess(open(f,encoding='cp437',errors='ignore').read()))


for subdir, dirs, files in os.walk(class2_train_path):
    for file in files:
        filepath = subdir + os.sep + file
        final_train_class_list.append(2)
        class2_train_files.append(filepath)

for f in class2_train_files:
        class2_train_string_list_processed.append(preprocess(open(f,encoding='cp437',errors='ignore').read()))

final_train_string_list = class1_train_string_list_processed + class2_train_string_list_processed


for subdir, dirs, files in os.walk(class1_test_path):
    for file in files:
        filepath = subdir + os.sep + file
        final_test_class_list.append(1)
        class1_test_files.append(filepath)

for f in class1_test_files:
        class1_test_string_list_processed.append(preprocess(open(f,encoding='cp437',errors='ignore').read()))


for subdir, dirs, files in os.walk(class2_test_path):
    for file in files:
        filepath = subdir + os.sep + file
        final_test_class_list.append(2)
        class2_test_files.append(filepath)

for f in class2_test_files:
        class2_test_string_list_processed.append(preprocess(open(f,encoding='cp437',errors='ignore').read()))

final_test_string_list = class1_test_string_list_processed + class2_test_string_list_processed


writeOutput(sys.argv[2])


