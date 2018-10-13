from itertools import chain
from nltk.corpus import wordnet


# Returns a list with simply False if no synonyms found.
# Returns a list with True in first index and wordlist in second index otherwise.

def getSyn(text):
    wordList = []
    synonyms = wordnet.synsets(text)
    lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
    for item in lemmas:
        string = item.lower()
        if ("_" not in string) and (string not in wordList):
            wordList.append(string)
    if len(wordList) == 0:
        return [False]
    else:
        return [True, wordList]
