import nltk
import string

#
# Input a text string, output a list of words from the text
#
def text2words(text):
    words = nltk.word_tokenize(text)
    words = [w.lower() for w in words if w not in string.punctuation]
    return [w for w in words if w not in nltk.corpus.stopwords.words('english')]