from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from re import split as respl
from textstat.textstat import textstat
from math import ceil

class TextAnalysis:
    sid = SentimentIntensityAnalyzer()

    # Initialize an empty TextAnalysis object with no text entered.
    # Takes one optional input - the default display options.
    # If no optional input entered, default is display all.
    @classmethod
    def blank(cls):
        return cls("")
    
    def __init__(self, text):
        self.text = text
        self.splList = respl("\W+", text)
        self.data = []
        
    def setText(self, text):
        self.text = text
        self.splList = respl("\W+", text)
        self.data = []

    def autoGet(self, text):
        self.text = text
        self.splList = respl("\W+", text)
        self.data = []
        return self.updateData()
        
    def updateData(self):
        # Full list of polarity scores
        self.data.append(self.sid.polarity_scores(self.text)) #0
        # Compounded score (0.0 - 1.0)
        self.data.append(self.data[0]['compound']) #1
        # Negative connotation rating (0.0 - 1.0)
        self.data.append(self.data[0]['neg']) #2
        # Positive connotation rating (0.0 - 1.0)
        self.data.append(self.data[0]['pos']) #3
        # Neutral connotation rating (0.0 - 1.0)
        self.data.append(self.data[0]['neu']) #4
        # # of detected sentences
        self.data.append(textstat.sentence_count(self.text)) #5
        # # of unique words in sentence (ignores apostrophes and such)
        self.data.append(textstat.lexicon_count(self.text)) #6
        # # of syllables in text
        self.data.append(textstat.syllable_count(self.text)) #7
        # Flesch reading ease score (0 - 100, 0 being hard and 100 being easy)
        self.data.append(textstat.flesch_reading_ease(self.text)) #8

        self.data.append(self.freGrade(self.data[8])) #9
        # Grade of text using flesch kincaid grade
        self.data.append(textstat.flesch_kincaid_grade(self.text)) #10
        # Grade of text using FOG system
        self.data.append(textstat.gunning_fog(self.text)) #11
        # Grade of text using SMOG (basically, more complicated FOG)
        self.data.append(textstat.smog_index(self.text)) #12
        # Grade of text using automated readability index
        self.data.append(ceil(textstat.automated_readability_index(self.text))) #13

        self.data.append(self.ariGrade(self.data[13])) #14
        # Grade of text using Coleman-Liau index
        self.data.append(textstat.coleman_liau_index(self.text)) #15
        # Grade of text using Linsear write formula
        self.data.append(textstat.linsear_write_formula(self.text)) #16
        
        self.data.append(textstat.dale_chall_readability_score(self.text)) #17

        self.data.append(self.daleChallGrade(self.data[17])) #18
        
        self.data.append(textstat.text_standard(self.text)) #19
        self.data.append(len(self.splList))
##        self.polarity = self.sid.polarity_scores(self.text)
##        self.sentences = textstat.sentence_count(self.text)
##        self.unique_words = textstat.lexicon_count(self.text)
##        self.syllables = textstat.syllable_count(self.text)
##        self.fleschReadEase = textstat.flesch_reading_ease(self.text)
##        self.fKGrade = textstat.flesch_kincaid_grade(self.text)
##        self.fog = textstat.gunning_fog(self.text)
##        self.smog = textstat.smog_index(self.text)
##        self.autoReadIndex = textstat.automated_readability_index(self.text)
##        self.cLIndex = textstat.coleman_liau_index(self.text)
##        self.linsearWrite = textstat.linsear_write_formula(self.text)
##        self.daleChallRead = textstat.dale_chall_readability_score(self.text)
##        self.readConsensus = textstat.text_standard(self.text)
        return self.data

    def daleChallGrade(self, adjScore):
        if adjScore < 5:
            return "4th grade and below"
        elif adjScore < 6:
            return "5th and 6th grade"
        elif adjScore < 7:
            return "7th and 8th grade"
        elif adjScore < 8:
            return "9th and 10th grade"
        elif adjScore < 9:
            return "11th and 12th grade"
        elif adjScore < 10:
            return "College-level"
        else:
            return "College graduate"


    def ariGrade(self, score):
        if (score > 14):
            return "College graduate"
        return {
            1:"Kindergarten",
            2:"1st and 2nd grade",
            3:"3rd grade",
            4:"4th grade",
            5:"5th grade",
            6:"6th grade",
            7:"7th grade",
            8:"8th grade",
            9:"9th grade",
            10:"10th grade",
            11:"11th grade",
            12:"12th grade",
            13:"College-level",
            14:"College graduate"
        }[score]

    def freGrade(self, score):
        if score < 30:
            return "College graduate"
        elif score < 50:
            return "College-level"
        elif score < 60:
            return "10th to 12th grade"
        elif score < 70:
            return "8th and 9th grade"
        elif score < 80:
            return "7th grade"
        elif score < 90:
            return "6th grade"
        else:
            return "5th grade and below"

##    def setDisplay(self, enabled):
##        self.enabled = enabled
##
##    def getPolarity(self):
##        return self.polarity
##    
##    def getCompound(self):
##        return self.polarity['compound']
##
##    def getPos(self):
##        return self.polarity['pos']
##
##    def getNeut(self):
##        return self.polarity['neu']
##
##    def getNeg(self):
##        return self.polarity['neg']
##
##    def getSentences(self):
##        return self.sentences

    
