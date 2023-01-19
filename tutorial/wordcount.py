import email
import json
from multiprocessing.util import debug
import re
from collections import Counter
from nltk.corpus import stopwords
import nltk
from math import log10, floor
from matplotlib import pyplot as plt
import numpy as np


def round_to_1(x):
   return round(x, -int(floor(log10(abs(x)))))

nltk.download('stopwords')

#add panda and numpy matplot

words = ""

myjsonfile=open('ksushow.json')
jsondata=myjsonfile.read()

obj = json.loads(jsondata)

#print(str(obj['pages']))
res = []
eres = []
totalNumresult = 0
page_counter = 0
for pages in obj['pages']:
    page_counter += 1
    pageBodyString = (str(pages['body']))
    pageEmailString = (str(pages['email']))
    res += re.findall(r'[a-zA-Z]{1,15}', pageBodyString) 
    eres += re.findall(r'\w+@kennesaw.edu', pageEmailString)

    totalNumresult += len(re.findall(r'[a-zA-Z]{1,15}', pageBodyString))

    

    #words = words + pageBodyString
    #print(str(pages['body']))

#print(words)
Avg_PageResult = totalNumresult/page_counter


stopwords = set(stopwords.words('english'))


d = {}
e = {}
fd= {}
Counter(res).most_common()

Counter(eres).most_common()

wlst = [x.lower() for x in res]


for word in eres:
    word.lower()

for word in wlst:
    d[word] = d.get(word, 0 ) + 1

for word in eres:
    e[word] = e.get(word, 0 ) + 1

for word in wlst:
    if word in stopwords:
        continue
    else:
        fd[word] = fd.get(word, 0 ) + 1

totalStopNumResult = len(fd)
totalEmailNumResult = len(e)

word_freq = []
fWord_freq = []
email_freq = []
for key, value in d.items():
    word_freq.append((value, key))

for key, value in fd.items():
    fWord_freq.append((value, key))

for key, value in e.items():
    email_freq.append((value, key))


word_freq.sort(reverse=True)
fWord_freq.sort(reverse=True)
email_freq.sort(reverse=True)
print("Word Frequency")
print("{:<8} {:<15} {:<10} {:<10}".format("rank", "term", "freq", "perc."))

word_occ = []
stopword_occ = []
for words in range(0,1000):
    word_occ.append(word_freq[words][0])
    stopword_occ.append(fWord_freq[words] [0])

for words in range(0,30):
    print("{:<8} {:<15} {:<10} {:<10}".format(words + 1, word_freq[words][1], word_freq[words][0], round_to_1((word_freq[words][0])/totalNumresult)))     #f'{words + 1} | {word_freq[words][1]} | {round_to_1((word_freq[words][0])/totalNumresult)}')



print("Word Frequency (Without Stopwords): ")
print("{:<8} {:<15} {:<10} {:<10}".format("rank", "term", "freq", "perc."))
for words in range(0,30):
    print("{:<8} {:<15} {:<10} {:<10}".format(words + 1, fWord_freq[words][1], fWord_freq[words][0], round_to_1((fWord_freq[words][0])/totalStopNumResult)))     


print("Email Frequency: ")
print('doc_len: ' + f'{totalEmailNumResult}')
print('emails:')
topTen = 0
for emails in range(0,10):
    topTen += email_freq[emails][0]
    print('         ' + f'{email_freq[emails]}')
email_perc = round_to_1((topTen)/totalEmailNumResult)
print('perc: ' + f'{email_perc}')



fig = plt.figure()

plt.plot(range(0,1000), word_occ)
plt.xlabel("Word rank")
plt.ylabel("word frequency")
fig.savefig('word_Distribution.png')
plt.loglog(range(0,1000), word_occ)
fig.savefig('log_log_plot.png')

plt.plot(range(0,1000), stopword_occ)
plt.xlabel("Word rank")
plt.ylabel("word frequency (without stopwords)")
fig.savefig('stopword_Distribution.png')
plt.loglog(range(0,1000), stopword_occ)
fig.savefig('stop_log_log_plot.png')

#print(word_freq)
#print(email_freq)
#print(d)
#print(e)

#Need to remove all : www, common phrases, jpg, https, 

#res = re.findall(r'\w+', words) 



# printing result 
#print ("\nThe words of string are")
#for i in res:
    #print(i)
