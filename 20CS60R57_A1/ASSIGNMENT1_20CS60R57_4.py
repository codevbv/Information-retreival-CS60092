import pickle
import sys

inv_index = None

with open("inv_index.pkl","rb") as f:
	inv_index = pickle.load(f)

# for k in inv_index.keys():
# 	print("-----"+k+"---------")
# 	print(inv_index[k])

def get_queries():
	queries = []
	query_file = sys.argv[1]
	f = open(query_file)
	for line in f:
		line = line.replace("\n","").lower()
		queries.append(line)
	return queries

def make_new_index(inv_index):
	outer_index_pre = {}
	outer_index_suf = {}
	for token in inv_index.keys():
		for i in range(1,len(token)):
			if token[:i] in outer_index_pre.keys():
				outer_index_pre[token[:i]].append(token)
			else:
				outer_index_pre[token[:i]] = []
				outer_index_pre[token[:i]].append(token)

			if token[i:] in outer_index_suf.keys():
				outer_index_suf[token[i:]].append(token)
			else:
				outer_index_suf[token[i:]] = []
				outer_index_suf[token[i:]].append(token)
		
		if token in outer_index_pre.keys():
			outer_index_pre[token].append(token)
		else:
			outer_index_pre[token] = []
			outer_index_pre[token].append(token)

		if token in outer_index_suf.keys():
			outer_index_suf[token].append(token)
		else:
			outer_index_suf[token] = []
			outer_index_suf[token].append(token)

	return outer_index_pre , outer_index_suf

def process_query(query):

	if query[0] == '*':
		
		query = query[1:]
		if query in outer_index_suf.keys():
			for term in outer_index_suf[query]:
				result = []
				docs = inv_index[term]
				for doc in docs.keys():
					for pos in docs[doc]:
						result.append((doc,pos))
				my_print(term,result)

		return 

	if query[len(query)-1] == '*':
		
		query = query[:-1]
		if query in outer_index_pre.keys():
			for term in outer_index_pre[query]:
				result = []
				docs = inv_index[term]
				for doc in docs.keys():
					for pos in docs[doc]:
						result.append((doc,pos))
				my_print(term,result)
		return

	if query.find('*') > -1:

		idx = query.find('*')
		pre = query[:idx]
		suf = query[idx+1:]

		terms_suf = []
		if suf in outer_index_suf.keys():
			for term in outer_index_suf[suf]:
				terms_suf.append(term)

		terms_pre = []
		if pre in outer_index_pre.keys():
			for term in outer_index_pre[pre]:
				terms_pre.append(term)

		common = set(terms_pre).intersection(terms_suf)
		common = list(common)
		
		for term in common:
			result = []
			docs = inv_index[term]
			for doc in docs.keys():
				for pos in docs[doc]:
					result.append((doc,pos))
			my_print(term,result)


		return



def my_print(term,res):
	string = term+":"
	for r in res:
		string += "<"+str(r[0])+","+str(r[1])+">,"
	f = open("RESULTS1_20CS60R57.txt", "a")
	f.write(string+'\n')
	f.close()

print(get_queries())

queries = get_queries()

outer_index_pre , outer_index_suf = make_new_index(inv_index)

for q in queries:
	process_query(q)




