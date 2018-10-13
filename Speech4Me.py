from flask import Flask, request, url_for, redirect, render_template
from TextAnalysis import TextAnalysis
from Synonym import Synonym

app = Flask(__name__)

regular_calc = ""

textA = TextAnalysis.blank()
textSyn = Synonym()
data = []

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('seocnd.html')

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    print(text)
    data = textA.auto(text)
    print(data)
    return render_template('seocnd.html')

# TO GET SYNONYMS OF A WORD
# textSyn.getChange(word, True) - Returns 2d list of synonyms considered "harder"
# textSyn.getChange(word) - Returns 2d list of ALL found synonyms regardless of difficulty
# textSyn.getChange(word, False) - Returns 2d list of synonyms considered "easier"

if __name__ == '__main__':
    app.run()
