import os
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer 
import pickle

my_files = []

for subdir, dirs, files in os.walk('ECTTEXT'):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".txt"):
            my_files.append(filepath)


def preprocess(text):

	punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
	stop_words = set(stopwords.words('english')) 
	lemmatizer = WordNetLemmatizer() 
	
	lines = text.split("\n")
	my_lines = []

	for line in lines:

		for ch in line:  
			if ch in punc:  
				line = line.replace(ch,"")
		my_lines.append(line)
	
	my_lines_final = []
	pos = 1
	for line in my_lines:
		filtered_sentence = []
		word_tokens = word_tokenize(line)
		for w in word_tokens:
			if not w in stop_words:
				filtered_sentence.append((lemmatizer.lemmatize(w.lower()),pos))
			pos += 1
		my_lines_final.append(filtered_sentence)
	
	return my_lines_final

def update_inv_index(inv_index,file_name,processed_lines):
	for line in processed_lines:
		for tuples in line:
			token = tuples[0]
			pos = tuples[1]
			if token not in inv_index.keys():
				inv_index[token] = {}
				inv_index[token][file_name] = [pos]
			else:
				if file_name not in inv_index[token].keys():
					inv_index[token][file_name] = [pos]
				else:
					inv_index[token][file_name].append(pos)




inv_index = {}

for f in my_files:
	processed_lines = preprocess(open(f).read())
	f = f.replace("ECTTEXT/","")
	file_name = f.split(".")[0]
	update_inv_index(inv_index,file_name,processed_lines)

inv_index = dict(sorted(inv_index.items()))

for k in inv_index.keys():
	print("-----"+k+"---------")
	print(inv_index[k])

with open("inv_index.pkl","wb") as f:
	pickle.dump(inv_index,f)








