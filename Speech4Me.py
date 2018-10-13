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
    data = textA.auto(text)
    print(data)
    return render_template('seocnd.html')

if __name__ == '__main__':
    app.run()
