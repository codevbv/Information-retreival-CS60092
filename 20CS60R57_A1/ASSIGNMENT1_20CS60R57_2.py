import os
from bs4 import BeautifulSoup
import pickle
import re


my_files = []

for subdir, dirs, files in os.walk('ECT'):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".html"):
            my_files.append(filepath)

#PART 1 A
def get_date(line):
	months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
	tokens = line.split()
	my_date = []
	flag = 0
	for t in tokens:
		if t in months:
			flag = 1
			my_date.append(t)
			continue
		if flag==1:
			flag = 2
			t = re.findall('\d+', t)[0]
			my_date.append(int(t))
			continue
		if flag==2:
			flag==3
			my_date.append(int(t))
			return my_date

#PART 1 B
def get_participants(text):
	cp = "Company Participants"
	ccp = "Conference Call Participants"
	my_participants = []
	i = 0
	flag = 0
	last_index = -1
	while(i<len(text) and i < 30):
		if text[i].find(cp) != -1:
			i += 1
			while(len(text[i])<50 and text[i].find("-")!=-1 and len(text[i].split("-"))==2):
				my_participants.append(text[i].split(" - "))
				last_index = i
				i += 1
		if text[i].find(ccp) != -1:
			flag = 1
			i += 1
			while(len(text[i])<50 and text[i].find("-")!=-1 and len(text[i].split("-"))==2):
				my_participants.append(text[i].split(" - "))
				last_index = i
				i += 1
		i+=1
		if flag==1:
			return last_index, my_participants
	return last_index, my_participants

#PART 1 C
def get_speaker(text,last_index,my_participants):
	i = last_index+1
	qa = "Question-and-Answer Session"
	my_dict = {}

	while(i<len(text) and text[i].find(qa)==-1):
		if text[i].strip() in my_participants:
			curr_participant = text[i].strip()
			i += 1
			string = ""
			while(i<len(text) and (text[i].strip() not in my_participants) and text[i].find(qa)==-1):
				string = string+text[i]
				i += 1
			my_dict[curr_participant] = string
		else:
			i +=1

	return i,my_dict

#PART 1 D
def get_qa(text,my_participants,last_index):
	qa = "Question-and-Answer Session"
	i = last_index+1
	serial = 0
	my_dict = {}
	while(i<len(text)):
		speaker = None
		remark = ""
		for mp in my_participants:
			if text[i].find(mp) > -1 and len(text[i]) < len(mp)+10:
				speaker = mp
				break

		if speaker is not None:
			i += 1
			flag = True
			while(flag):
				for mp in my_participants:
					if i>=len(text) or (text[i].find(mp) > -1 and len(text[i]) < len(mp)+10):
						i -= 1
						flag = False
						break
				if flag==False:
					break
				remark += text[i]
				i += 1
		else:
			i+=1
			continue

		my_dict[serial] = {}
		my_dict[serial]["speaker"] = speaker
		my_dict[serial]["remark"] = remark
		serial +=1
		i += 1

	return my_dict

ECTNestedDict = {}

for f in my_files:
	text = ''.join(BeautifulSoup(open(f).read(), "html.parser").findAll(text=True))
	text = text.split('\n')
	date = get_date(text[0])
	last_index , participants = get_participants(text)
	my_participants = [ p[0] for p in participants ]
	last_index, speaker = get_speaker(text,last_index,my_participants)
	ques_ans_dict = get_qa(text,my_participants,last_index)
	f_new = f.replace("ECT\\","")
	ECTNestedDict[f_new] = {}
	ECTNestedDict[f_new]["Date"] = date
	ECTNestedDict[f_new]["Participants"] = my_participants
	ECTNestedDict[f_new]["Presentation"] = speaker
	ECTNestedDict[f_new]["Questionnaire"] = ques_ans_dict

#Output ECTNestedDict.pkl
with open("ECTNestedDict.pkl","wb") as out:
	pickle.dump(ECTNestedDict,out)


#PART 2
if not os.path.exists("ECTText"):
    os.makedirs("ECTText")

for f in my_files:
	a = open(f).read()
	text = ''.join(BeautifulSoup(a, "html.parser").findAll(text=True))
	new_name = f.split("-")[0]+".txt"
	with open(os.path.join("ECTText",new_name.replace("ECT/","")),"w") as out:
		out.write(text)




