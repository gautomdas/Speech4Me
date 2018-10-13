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
    return render_template('second.html')

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    print(text)
    data = textA.auto(text)
    print(data)
    return render_template('second.html', comp=data[0][0], neg=data[0][1], pos=data[0][2], neut=data[0][3], sent=data[1][0], uniq=data[1][1], syll=data[1][2], word=data[1][3], char=data[1][4], fre_s=data[2][0], fre_g=data[2][1], fkg_s=data[3][0], fkg_g=data[3][1], gfi_s=data[4][0], gfi_g=data[4][1], si_s=data[5][0], si_g=data[5][1],  ari_s=data[6][0], ari_g=data[6][1], cli_s=data[7][0], cli_g=data[7][1], lwi_s=data[8][0], lwi_g=data[8][1], dcr_s=data[9][0], dcr_g=data[9][1])

# TO GET SYNONYMS OF A WORD
# textSyn.getChange(word, True) - Returns 2d list of synonyms considered "harder"
# textSyn.getChange(word) - Returns 2d list of ALL found synonyms regardless of difficulty
# textSyn.getChange(word, False) - Returns 2d list of synonyms considered "easier"

if __name__ == '__main__':
    app.run()
