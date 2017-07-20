from bs4 import BeautifulSoup # For HTML parsing
from urllib.request import urlopen
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
import re #regular expressions
from time import time #to see how long each step takes
from joblib import Parallel, delayed #to speed up / paralellize

def html_cleaner(site):
	"""
	Create function that takes a URL as input, extracts text,
	cleans it, outputs text as a list of words (no stopwords, no duplicates)
	"""
	try:
		html = urlopen(site).read()
	except:
		return  #use try-except in case website throws an error or doesn't connect

	soup = BeautifulSoup(html, 'html.parser') #extract html

	if len(soup) == 0: # In case the first parser doesn't work, try another one
		soup = BeautifulSoup(html, 'html5lib')

	#look for script and style tags/elements and remove this from soup object

	for sstags in soup(["script", "style"]):
		sstags.extract()

	#extract text, split into lines

	text = soup.get_text().splitlines()

	#split into individual lines, remove whitespace, join back together

	lines = (line.strip() for line in text)

	bits = (phrase.strip() for line in lines for phrase in line.split("  "))

	text = "".join(bit for bit in bits if bit)

	#use regular expressions to get rid of junk that is not a word
	text = re.sub("[^a-zA-Z+3]", " ", text) #include '+' for C++ and '3' for D3

	#space issues no longer a concern, comment this out
	#text = re.sub(r"([a-z+3])([A-Z+3])", r"\g<1> \g<2>", text)

	# lower case and split into words
	text = text.lower()

	ad_words = text.split()

	#define stopwords from NLTK
	#list comprehension to filter out stopwords like 'the' 'or' 'and'

	stop_words = set(stopwords.words("english"))
	ad_words = [w for w in ad_words if not w in stop_words]

	#use set() to eliminate duplicate elements

	ad_words = list(set(ad_words))

	return ad_words #return ad_words for a list of individual words in each ad or return text for job ad full text

	#unique words now ready for counting
