from flask import Flask, request, url_for, redirect, render_template
import TextAnalysis

app = Flask(__name__)

regular_calc = ""

textA = TextAnalysis.TextAnalysis.blank()
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
    data = textA.autoGet(text)
    print(data)
    return render_template('seocnd.html', originalText=text, fullPolarity=data[0], posnegPolarity=data[1], negPolarity=data[2],
                           posPolarity=data[3], neutPolarity=data[4], numSentence=data[5], numUniqueWords=data[6], numSyllable=data[7],
                           fleschScore=data[8], fleschGrade=data[9], fleshKincaidGrade=data[10], gunningFog=data[11], smogIndex=data[12],
                           autoReadIndex=data[13], autoReadGrade=data[14], colemanLiau=data[15])

if __name__ == '__main__':
    app.run()
