from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
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

    # Initialize TextAnalysis with text input.
    def __init__(self, text):
        self.text = text
        self.splList = self.text.split()
        self.data = []

    # Set text in class to input.
    def setText(self, text):
        self.text = text
        self.splList = self.text.split()
        self.data = []

    # Update and set text to input, then return results.
    def auto(self, text):
        self.text = text
        self.splList = self.text.split()
        self.data = []
        return self.updateData()

    ########## METHOD: Update Data ##########
    # Updates, collects, and returns data.

    ##### INDEX 0 IN DATA: Text Sentiment #####
    # [INDEX 0] Compounded score (-1.0 - 1.0)            [INDEX 1] Negative connotation rating (0.0 - 1.0),
    # [INDEX 2] Positive connotation rating (0.0 - 1.0) [INDEX 3] Neutral connotation rating (0.0 - 1.0)
    ##### INDEX 1 IN DATA: Sentence Info #####
    # [INDEX 0] Sentence count          [INDEX 1] Unique wordcount
    # [INDEX 2] Syllable count          [INDEX 3] Overall word count
    # [INDEX 4] Character count
    ##### INDEX 2 IN DATA: Flesch Reading Ease #####
    # [INDEX 0] Pure score              [INDEX 1] Approximate grade
    # SCORE SCALE: 0 - 100
    ##### INDEX 3 IN DATA: Flesch-Kincaid Grade #####
    # [INDEX 0] Pure score              [INDEX 1] Approximate grade
    # SCORE SCALE: 0 - 18
    ##### INDEX 4 IN DATA: Gunning FOG Index #####
    # [INDEX 0] Pure Score              [INDEX 1] Approximate grade
    # SCORE SCALE: 0 - 18
    ##### INDEX 5 IN DATA: SMOG Index #####
    # [INDEX 0] Pure Score              [INDEX 1] Approximate grade
    # SCORE SCALE: 0 - 18
    ##### INDEX 6 IN DATA: Automated Readability Index #####
    # [INDEX 0] Pure Score              [INDEX 1] Approximate grade
    # SCORE SCALE: 0 - 14
    ##### INDEX 7 IN DATA: Coleman-Liau Index #####
    # [INDEX 0] Pure Score              [INDEX 1] Approximate grade
    # SCORE SCALE: 0 - 18
    ##### INDEX 8 IN DATA: Linsear Write Index #####
    # [INDEX 0] Pure Score              [INDEX 1] Approximate grade
    # SCORE SCALE: 0 - 18
    ##### INDEX 9 IN DATA: Dale-Chall Readability Score #####
    # [INDEX 0] Pure Score              [INDEX 1] Approximate grade
    # SCORE SCALE: 0 - 10
    ##### INDEX 10 IN DATA: Overall Score #####
    # Approximate grade (NOT A LIST)


    def updateData(self):

        # Full list of polarity scores
        self.polscore = self.sid.polarity_scores(self.text)

        ##### INDEX 0 IN DATA: Text Sentiment #####
        # [INDEX 0] Compounded score (0.0 - 1.0)            [INDEX 1] Negative connotation rating (0.0 - 1.0),
        # [INDEX 2] Positive connotation rating (0.0 - 1.0) [INDEX 3] Neutral connotation rating (0.0 - 1.0)
        self.data.append([self.polscore['compound'], self.polscore['neg'], self.polscore['pos'], self.polscore['neu']])

        ##### INDEX 1 IN DATA: Sentence Info #####
        # [INDEX 0] Sentence count          [INDEX 1] Average sentence length
        # [INDEX 2] Syllable count          [INDEX 3] Overall word count
        # [INDEX 4] Character count         [INDEX 5] Character count without spaces
        # [INDEX 6] Avg letters per word    [INDEX 7] Avg syllables per word
        self.data.append([textstat.sentence_count(self.text), textstat.avg_sentence_length(self.text),
                          textstat.syllable_count(self.text), len(self.splList), textstat.char_count(self.text, False),
                          textstat.char_count(self.text, True), textstat.avg_letter_per_word(self.text),
                          textstat.avg_syllables_per_word(self.text)])

        ##### INDEX 2 IN DATA: Flesch Reading Ease #####
        # [INDEX 0] Pure score              [INDEX 1] Approximate grade
        # SCORE SCALE: 0 - 100
        self.freStat = min(max(textstat.flesch_reading_ease(self.text), 0), 100)
        self.data.append([self.freStat, self.freGrade(self.freStat)])

        ##### INDEX 3 IN DATA: Flesch-Kincaid Grade #####
        # [INDEX 0] Pure score              [INDEX 1] Approximate grade
        # SCORE SCALE: 0 - 18
        self.fkgStat = self.adjustScore(textstat.flesch_kincaid_grade(self.text))
        self.data.append([self.fkgStat, self.grade(self.fkgStat)])

        ##### INDEX 4 IN DATA: Gunning FOG Index #####
        # [INDEX 0] Pure Score              [INDEX 1] Approximate grade
        # SCORE SCALE: 0 - 18
        self.fogStat = self.adjustScore(textstat.gunning_fog(self.text))
        self.data.append([self.fogStat, self.grade(self.fogStat)])

        ##### INDEX 5 IN DATA: SMOG Index #####
        # [INDEX 0] Pure Score              [INDEX 1] Approximate grade
        # SCORE SCALE: 0 - 18
        self.smogStat = self.adjustScore(textstat.smog_index(self.text))
        self.data.append([self.smogStat, self.grade(self.smogStat)])

        ##### INDEX 6 IN DATA: Automated Readability Index #####
        # [INDEX 0] Pure Score              [INDEX 1] Approximate grade
        # SCORE SCALE: 0 - 14
        self.ariStat = min(max(textstat.automated_readability_index(self.text), 0), 14)
        self.data.append([self.ariStat, self.ariGrade(ceil(self.ariStat))]) #13

        ##### INDEX 7 IN DATA: Coleman-Liau Index #####
        # [INDEX 0] Pure Score              [INDEX 1] Approximate grade
        # SCORE SCALE: 0 - 18
        self.cliStat = self.adjustScore(textstat.coleman_liau_index(self.text))
        self.data.append([self.cliStat, self.grade(self.cliStat)])

        ##### INDEX 8 IN DATA: Linsear Write Index #####
        # [INDEX 0] Pure Score              [INDEX 1] Approximate grade
        # SCORE SCALE: 0 - 18
        self.lwiStat = self.adjustScore(textstat.linsear_write_formula(self.text))
        self.data.append([self.lwiStat, self.grade(self.lwiStat)])

        ##### INDEX 9 IN DATA: Dale-Chall Readability Score #####
        # [INDEX 0] Pure Score              [INDEX 1] Approximate grade
        # SCORE SCALE: 0 - 10
        self.dcrStat = min(max(textstat.dale_chall_readability_score(self.text), 0), 10)
        self.data.append([self.dcrStat, self.grade(self.dcrStat)])

        ##### INDEX 10 IN DATA: Overall Score #####
        # [INDEX 0] Pure Score              [INDEX 1] Approximate grade
        # SCORE SCALE: 0 - 20
        self.txtStd = min(max(textstat.text_standard(self.text, True), 0), 20)
        self.txtInfo = textstat.text_standard(self.text)
        self.data.append([self.txtStd, self.txtGrade(self.txtStd, self.txtInfo)])

        return self.data

    # Adjust score to be between 0 and 18.
    def adjustScore(self, score):
        return min(max(score, 0), 18)

    def txtGrade(self, score, txt):
        if (score < 1):
            return "Kindergarten and 1st grade"
        elif (score < 12):
            return txt
        elif (score < 16):
            return "College-level"
        else:
            return "College graduate"
    # Approximate grade from score based on US grade system
    def grade(self, score):
        if (score > 17):
            return "College graduate"
        elif (score < 1):
            return "Kindergarten"
        gradeApprox = round(score)
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
            14:"College-level",
            15:"College-level",
            16:"College-level",
            17:"College graduate"
        }[gradeApprox]

    # Specific grade for Dale-Chall Readability Score
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

    # Specific grade for Automated Readability Index
    def ariGrade(self, score):
        if (score > 14):
            return "College graduate"
        elif (score < 1):
            return "Kindergarten"
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

    # Specific grade for Flesch Reading Ease
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

    
