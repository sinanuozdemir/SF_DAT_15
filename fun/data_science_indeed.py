import requests
from BeautifulSoup import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer

texts = []
for i in range(0,1000,10): # cycle through 100 pages of indeed job resources
    soup = BeautifulSoup(requests.get('http://www.indeed.com/jobs?q=data+scientist&start='+str(i)).text)
    texts += [a.text for a in soup.findAll('span', {'class':'summary'})]
    

print len(texts), "job descriptions" # over 1,000 descriptions


texts[0]  # first job description

vect = CountVectorizer(ngram_range=(1,3), stop_words='english')
matrix = vect.fit_transform(texts)
len(vect.get_feature_names())


freqs = [(word, matrix.getcol(idx).sum()) for word, idx in vect.vocabulary_.items()]
#sort from largest to smallest
for phrase, times in sorted (freqs, key = lambda x: -x[1])[:25]:
    print phrase, times