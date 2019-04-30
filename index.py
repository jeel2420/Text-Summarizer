from flask import Flask,render_template,request
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from flask import url_for
from nltk.probability import FreqDist
from heapq import nlargest

from collections import defaultdict

def summarize(text,n):
    sents = sent_tokenize(text)
    
    assert n <= len(sents)       # fucntion fails if article contains 2 function and you have to make summary of 3 sentence.
    
    word_sent = word_tokenize(text.lower())
    _stopwords = set(stopwords.words('english') + list(punctuation))
    
    word_sent = [word for word in word_sent if word not in _stopwords]

    freq = FreqDist(word_sent)
    
    ranking = defaultdict(int)
    
    for i,sent in enumerate(sents):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i] += freq[w]
                
    sents_idx = nlargest(n, ranking, key=ranking.get)
    
    return [sents[j] for j in sorted(sents_idx)]

app = Flask(__name__)

@app.route("/")
def home():
	return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    text1 = request.form['text']
    text2 = summarize(text1,5)
    return render_template('home.html', text1=text1, text2=text2)

@app.route('/hiw')
def hiw():
	return render_template('hiw.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route("/login")
def login():
	return render_template('login.html')

if __name__ == '__main__':
	app.run(debug=True)