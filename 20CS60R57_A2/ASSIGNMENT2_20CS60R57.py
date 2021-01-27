import pickle
import numpy
import os
import math
import sys
from bs4 import BeautifulSoup
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer 

my_html_files = []
my_files = []


for subdir, dirs, files in os.walk('Dataset'):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".html"):
            my_html_files.append(filepath)

if not os.path.exists("DatasetText"):
    os.makedirs("DatasetText")

for f in my_html_files:
	a = open(f,encoding='cp437',errors='ignore')  
	text = ''.join(BeautifulSoup(a, "html.parser").findAll(text=True))
	new_name = f.split(".")[0]+".txt"
	with open(os.path.join("DatasetText",new_name.replace("Dataset/","")),"w",encoding='cp437',errors='ignore') as out:
		out.write(text)

for subdir, dirs, files in os.walk('DatasetText'):
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
	# i = 0
	for line in lines:
		# print(line)
		# i +=1
		# if i > 3:
		# 	break
		for ch in line:  
			if ch in punc:  
				line = line.replace(ch,"")
		my_lines.append(line)
	
	my_lines_final = []
	for line in my_lines:
		filtered_sentence = []
		word_tokens = word_tokenize(line)
		for w in word_tokens:
			if not w in stop_words:
				filtered_sentence.append(lemmatizer.lemmatize(w.lower()))
		my_lines_final.append(filtered_sentence)
	
	return my_lines_final


def get_score():
	f = open('StaticQualityScore.pkl','rb')
	a  = pickle.load(f)
	f.close()
	'''
	print(a)
	'''
	return a

def update_inv_index(inv_index,file_name,term_freq):
	for token in term_freq.keys():
		# seeing token for first time
		val = math.log10(1+term_freq[token])
		if token not in inv_index.keys():
			inv_index[token] = []
			inv_index[token].append((file_name,val))
		# seen token before , but new document
		else:
			if file_name not in inv_index[token]:
				inv_index[token].append((file_name,val))
					

def get_term_freq(processed_lines):
	freq_count = {}
	for line in processed_lines:
		for term in line:
			freq_count[term] = freq_count.get(term,0)+1
	return freq_count

def get_inv_pos_index(my_files):

	# record id of each doc
	doc_idx = {} 
	# inverted index of step 1
	inv_index = {}

	for f in my_files:
		processed_lines = preprocess(open(f,encoding='cp437',errors='ignore').read())
		# for each doc , find freq of terms
		term_freq = get_term_freq(processed_lines)
		# print(term_freq)
		f = f.replace("DatasetText\\","")
		file_name = f.split(".")[0]
		doc_idx[file_name] = int(file_name)
		update_inv_index(inv_index,file_name,term_freq)
	
	# for t in inv_index.keys():
	# 	print(t," => ",inv_index[t])

	final_inv_idx = { ( k , math.log10(1000/len(v)) ) : sorted(v,key=lambda x : x[0]) for k,v in inv_index.items() }
	'''
	for t in final_inv_idx.keys():
		print(t," => ",final_inv_idx[t])

	print("------------------------------------------------------------------------------")
	'''
	return final_inv_idx , doc_idx

def get_champion_list_local(inv_index):
	champion_idx_local = { k : sorted(v,key=lambda x : x[1],reverse=True)[:50] for k,v in inv_index.items() }
	'''
	for t in champion_idx_local.keys():
		print(t," => ",champion_idx_local[t])
	print("------------------------------------------------------------------------------")
	'''
	return champion_idx_local

def get_champion_list_global(inv_index,scores,doc_idx):
	champion_idx_global = {}
	for term in inv_index.keys():
		idf = term[1]
		champion_idx_global[term] = []
		for docs_pair in inv_index[term]:
			score = idf*docs_pair[1]+scores[doc_idx[docs_pair[0]]]
			champion_idx_global[term].append((docs_pair[0],score))
		
		champion_idx_global[term] = sorted(champion_idx_global[term],key=lambda x : x[1] , reverse=True)
	'''
	for t in champion_idx_global.keys():
		print(t," => ",champion_idx_global[t])
	print("------------------------------------------------------------------------------")
	'''
	return champion_idx_global 



def dot(A,B): 
    return (sum(a*b for a,b in zip(A,B)))

def cosine_similarity(a,b):
	num = dot(a,b)
	den = (dot(a,a) **.5) * (dot(b,b) ** .5) 
	if den == 0 :
		return num 
	return dot(a,b) / ( (dot(a,a) **.5) * (dot(b,b) ** .5) )

def tf_idf_score(Q,d,num_terms):
	Q_vector = [0] * num_terms
	d_vector = [0] * num_terms
	for term in Q:
		if idf_scores.get(term,-1) != -1:
			pos = terms_order[term]
			Q_vector[pos] = idf_scores[term]
			for pair in inv_index[(term,idf_scores[term])]:
				if pair[0] == d:
					d_vector[pos] = pair[1] * idf_scores[term]
					break
	return cosine_similarity(Q_vector,d_vector)

def local_champion_score(Q,d,num_terms):
	Q_vector = [0] * num_terms
	d_vector = [0] * num_terms
	for term in Q:
		if idf_scores.get(term,-1) != -1:
			pos = terms_order[term]
			Q_vector[pos] = idf_scores[term]
			for pair in champion_idx_local[(term,idf_scores[term])]:
				if pair[0] == d:
					d_vector[pos] = pair[1] * idf_scores[term]
					break
	return cosine_similarity(Q_vector,d_vector)


def global_champion_score(Q,d,num_terms):
	Q_vector = [0] * num_terms
	d_vector = [0] * num_terms
	for term in Q:
		if idf_scores.get(term,-1) != -1:
			pos = terms_order[term]
			Q_vector[pos] = idf_scores[term]
			for pair in champion_idx_global[(term,idf_scores[term])]:
				if pair[0] == d:
					d_vector[pos] = pair[1] * idf_scores[term]
					break
	return cosine_similarity(Q_vector,d_vector)

def top_documents_1(processed_queries,num_terms):
	doc_list = list(doc_idx.keys())
	for q in processed_queries:
		scores = [0] * len(doc_idx.keys())
		for doc in doc_idx.keys():
			scores[doc_idx[doc]] = tf_idf_score(q,doc,num_terms)
		# print(scores)
		top_10_idx = sorted(range(len(scores)),reverse = True,key=lambda i: scores[i])[-10:]
		doc_name =  [doc_list[i] for i in top_10_idx]
		doc_score = [scores[i] for i in top_10_idx]
		return [(a,b) for a,b in zip(doc_name,doc_score)]

def top_documents_2(processed_queries,num_terms):
	doc_list = list(doc_idx.keys())
	for q in processed_queries:
		scores = [0] * len(doc_idx.keys())
		for doc in doc_idx.keys():
			scores[doc_idx[doc]] = local_champion_score(q,doc,num_terms)
		# print(scores)
		top_10_idx = sorted(range(len(scores)),reverse = True,key=lambda i: scores[i])[-10:]
		doc_name =  [doc_list[i] for i in top_10_idx]
		doc_score = [scores[i] for i in top_10_idx]
		return [(a,b) for a,b in zip(doc_name,doc_score)]

def top_documents_3(processed_queries,num_terms):
	doc_list = list(doc_idx.keys())
	for q in processed_queries:
		scores = [0] * len(doc_idx.keys())
		for doc in doc_idx.keys():
			scores[doc_idx[doc]] = global_champion_score(q,doc,num_terms)
		# print(scores)
		top_10_idx = sorted(range(len(scores)),reverse = True,key=lambda i: scores[i])[-10:]
		doc_name =  [doc_list[i] for i in top_10_idx]
		doc_score = [scores[i] for i in top_10_idx]
		return [(a,b) for a,b in zip(doc_name,doc_score)]

def task2(query_file_name,num_terms):
	processed_queries = preprocess(open(query_file_name).read())
	f = open('RESULTS2_20CS60R57.txt','w')
	for q in processed_queries:
		
		f.write(' '.join(q)+"\n")
		
		l1 = top_documents_1([q],num_terms)
		l1 = [ "<" + str(pair[0]) + "," + str(pair[1]) + ">" for pair in l1 ]
		f.write(','.join(l1)+"\n")
		
		l2 = top_documents_2([q],num_terms)
		l2 = [ "<" + str(pair[0]) + "," + str(pair[1]) + ">" for pair in l2]
		f.write(','.join(l2)+"\n")

		l3 = top_documents_3([q],num_terms)
		l3 = [ "<" + str(pair[0]) + "," + str(pair[1]) + ">" for pair in l3 ]
		f.write(','.join(l3)+"\n\n")

	f.close()

#Built inverted index
inv_index , doc_idx = get_inv_pos_index(my_files)
#Built Champion index local
champion_idx_local  = get_champion_list_local(inv_index)
#Retrieve the scores
scores = get_score()
#Built Champion index global
champion_idx_global  = get_champion_list_global(inv_index,scores,doc_idx)


terms_order = {}
idf_scores = {}

i = 0

for t in inv_index.keys():
	terms_order[t[0]] = i
	idf_scores[t[0]] = t[1]
	i += 1

num_terms = i
query_file_name = sys.argv[1]
task2(query_file_name,num_terms)