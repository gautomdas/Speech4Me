from itertools import chain
from nltk.corpus import wordnet
import math


# Returns a list with simply False if no synonyms found.
# Returns a list with True in first index and wordlist in second index otherwise.

class Synonym:
    def __init__(self):
        self.wordDist = self.readFile()

    # Gets synonyms from wordnet.
    def getSyn(self, text):
        wordList = []
        synonyms = wordnet.synsets(text)
        lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
        for item in lemmas:
            string = item.lower()
            if ("_" not in string) and (string not in wordList) and (string != text.lower()):
                wordList.append(string)
        return wordList

    # Gets frequency of synonyms found in wordnet.
    def getFreqSyn(self, word):
        self.inputFreq = self.getWord(word)
        syns = self.getSyn(word)
        result = []
        if syns:
            for item in syns:
                result.append([item, round(self.getWord(item), 3)])
            return result
        else:
            return False

    ##### MAIN METHOD #####
    # [ARG 1] Word to check for
    # [ARG 2] True: Check for harder words, False: Check for easier words, None: Return all
    # [RETURN] 2D Array. Each index in main array will "belong" to a synonym.
    #           Each index contains the string in [INDEX 0] and the frequency score
    #           in [INDEX 1]. Higher frequencies mean harder words.

    def getChange(self, word, harder=None):
        freqSyn = self.getFreqSyn(word)
        freqSyn.sort(key=lambda x : x[1])
        finalAns = []
        if harder is None:
            return freqSyn
        if harder:
            for item in freqSyn:
                if item[1] > self.inputFreq:
                    finalAns.append(item)
        else:
            for item in freqSyn:
                if item[1] <= self.inputFreq:
                    finalAns.append(item)
        finalAns.sort(key=lambda x : x[1])
        return finalAns

    ##### READ FILE METHOD #####
    # Reads a file and returns a dictionary with words and frequency number.
    # Frequency number is the negative log of the number of occurrences divided by total words in set.
    # frequency = -log10(words_wanted/total_words)
    def readFile(self, filename="en_full.txt"):
        wordFreq = dict()
        with open(filename, 'r') as file:
            lines = file.readlines()
            ##### FOR VARIABLE-SIZED CORPUS BASE #####
            # self.totalSize = sum([int(item) for item in file.read().split() if item.isdigit()])

            # Only one specific (not-actually-a) corpus used, so total words in "corpus" known
            self.totalSize = 534751778

        for line in lines:
            info = line.split()
            wordFreq[info[0]] = -math.log10(int(info[1]) / self.totalSize)
        return wordFreq

    # Finds frequency of a word.
    # If word not in dataset, use the highest "frequency number" possible rounded up.
    # Remember, frequency number is -log10(words_wanted/total_words)
    def getWord(self, word):
        if word in self.wordDist:
            return self.wordDist[word]
        else:
            return -math.log10(1 / self.totalSize)
