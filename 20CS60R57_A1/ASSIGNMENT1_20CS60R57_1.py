from bs4 import BeautifulSoup, SoupStrainer
import requests
import os
import time
import random

headers = { 'accept':'*/*',
'accept-encoding':'gzip, deflate, br',
'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7,la;q=0.6',
'cache-control':'no-cache',
'dnt':'1',
'pragma':'no-cache',
'referer':'https',
'sec-fetch-mode':'no-cors',
'sec-fetch-site':'cross-site',
'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
 }

if not os.path.exists("ECT"):
    os.makedirs("ECT")

def update_URL(page_num):
	url = "https://seekingalpha.com/earnings/earnings-call-transcripts/"
	print(page_num)
	return url+page_num


def get_Links():
	countLinks = 0
	countPage = 1
	while(countLinks<=10000):
		t1 = random.uniform(5, 10) + random.uniform(1, 3)
		time.sleep(t1)
		new_URL = update_URL(str(countPage))
		print(new_URL)
		page = requests.get(new_URL,headers=headers)    
		data = page.text
		soup = BeautifulSoup(data,'html.parser')
		for link in soup.find_all('a',class_='dashboard-article-link'):
			t2 = random.uniform(5, 10) + random.uniform(1, 3)
			time.sleep(t2)
			text_URL = 'https://seekingalpha.com'+ (link.get('href'))
			#r = requests.get(text_URL, allow_redirects=True)
			r = requests.get(text_URL, headers = headers)
			file_name = str(countLinks)+link.get('href')+'.html'
			file_name = file_name.replace("/","-")
			print(file_name)
			path = 'ECT\\'+file_name
			open(path, 'wb').write(r.content)
			countLinks = countLinks + 1
		countPage = countPage +1		

get_Links()
