from flask import Flask, request, url_for, redirect, render_template
from TextAnalysis import TextAnalysis
from Synonym import Synonym
from subprocess import call

call(["python", "-m", "nltk.downloader", "wordnet","vader_lexicon"])

app = Flask(__name__)

regular_calc = ""

textA = TextAnalysis.blank()
textSyn = Synonym()
data = []

original_grad = 0
original_grad = 10
all_text = ""
words_all = []

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/review', methods=['GET', 'POST'])
def review():
    global word
    global words_all
    global tot

    grade = request.form['someid']
    print("id: "+grade)
    all_lines = all_text.splitlines()
    final = []
    if(int(grade)>original_grad):
        type_e = "harder"
        string_start = "<p>"

        for line in all_lines:
            print("FLAG")
            words = line.split(" ")
            print(words)
            for word in words:
                tot = []
                tot.append(word)
                print("_"*20)
                print(word)
                per_flag = False
                sec_flag = False
                if "." in word:
                    per_flag = True
                    word = word.split(".")[0]
                choices = textSyn.getChange(word, True)
                if(len(word)>3):
                    print("HERE")
                    if(len(choices)==0):
                        if per_flag:
                            string_start+= word+". "
                            sec_flag = True
                        else:
                            string_start+= word+" "
                    if(len(choices)>0):
                        string_start+=" <select class=\"someSel\" name=\""+word+"\">"
                        string_start+= "<option class=\"others\" value=\""+word+"\">"+word+"</option>"
                        for choice in choices:
                            string_start+= "<option class=\"others\" value=\""+choice[0]+"\">"+choice[0]+"</option>"
                        string_start+= "</select></span> "
                else:
                    if per_flag:
                        string_start += word + ". "
                        sec_flag = True
                    else:
                        string_start += word + " "
                if per_flag and not sec_flag:
                    string_start+=". "
                tot.append(word)
                words_all.append(tot)

            string_start+="<br>"
            words_all+=["!BREAK!"]
        string_start += "</p>"
        print(string_start)
    else:
        type_e = "easier"
        string_start = "<p>"

        for line in all_lines:
            print("FLAG")
            words = line.split(" ")
            print(words)
            for word in words:
                tot = []
                tot.append(word)
                print("_" * 20)
                print(word)
                per_flag = False
                sec_flag = False
                if "." in word:
                    per_flag = True
                    word = word.split(".")[0]
                choices = textSyn.getChange(word, False)
                if (len(word) > 3):
                    print("HERE")
                    if (len(choices) == 0):
                        if per_flag:
                            string_start += word + ". "
                            sec_flag = True
                        else:
                            string_start += word + " "
                    if (len(choices) > 0):
                        string_start += " <select class=\"someSel\" name=\"" + word + "\">"
                        string_start += "<option class=\"others\" value=\"" + word + "\">" + word + "</option>"
                        for choice in choices:
                            string_start += "<option class=\"others\" value=\"" + choice[0] + "\">" + choice[
                                0] + "</option>"
                        string_start += "</select></span> "
                else:
                    if per_flag:
                        string_start += word + ". "
                        sec_flag = True
                    else:
                        string_start += word + " "
                if per_flag and not sec_flag:
                    string_start += ". "
                tot.append(word)
                words_all.append(tot)

            string_start += "<br>"
            words_all += ["!BREAK!"]
        string_start += "</p>"
        print(string_start)

    Html_file = open("templates/generated_paragraph.html", "w")
    Html_file.write(string_start)
    Html_file.close()
    return render_template('review.html', type_a = type_e)


@app.route('/finish', methods=['GET', 'POST'])
def finish():
    edited=""
    for wordList in words_all:
        word = wordList[0]
        select = request.form.get(word)
        if(word!=""):
            if(wordList=="!BREAK!"):
                edited+="\n"
            else:
                print("*"*10)
                print(word)
                if(select == None):
                    edited+=word +" "
                else:
                    if("." in word):
                        edited += select+". "
                    else:
                        edited += select+" "
            print("=========")
            print(wordList)
            print (str(select))  # just to see what select is
    print(edited)
    return render_template('finish.html', fina=edited)

@app.route('/stats', methods=['POST'])
def stats():
    text = request.form['text']
    print(text)
    global all_text
    all_text=text
    data = textA.auto(text)
    print(data)
    text_sentiment = [data[0][0], data[0][1], data[0][2], data[0][3]]
    gen_text_info = [data[1][0], data[1][1],data[1][6], data[1][7]]
    con_gen_text = [data[1][2], data[1][3], data[1][4]]

    all_labels = ['fre_s', 'fre_g', 'fkg_s', 'fkg_g', 'gfi_s', 'gfi_g', 'si_s', 'si_g', ' ari_s', 'ari_g', 'cli_s', 'cli_g', 'lwi_s', 'lwi_g', 'dcr_s', 'dcr_g']
    all_datas = [data[2][0], data[3][0], data[4][0], data[5][0], data[6][0], data[7][0], data[8][0], data[9][0]]
    print("++++++: "+str(all_datas))
    print(gen_text_info)
    return render_template('stats.html', comp=data[0][0], neg=data[0][1], pos=data[0][2], neut=data[0][3], sent=data[1][0], sent_len=data[1][1], syll=data[1][2], word=data[1][3], char=data[1][4], char_nospc=data[1][5], avg_c=data[1][6], syll_per_word=data[1][7], fre_s=data[2][0], fre_g=data[2][1], fkg_s=data[3][0], fkg_g=data[3][1], gfi_s=data[4][0], gfi_g=data[4][1], si_s=data[5][0], si_g=data[5][1], ari_s=data[6][0], ari_g=data[6][1], cli_s=data[7][0], cli_g=data[7][1], lwi_s=data[8][0], lwi_g=data[8][1], dcr_s=data[9][0], dcr_g=data[9][1], dataA = text_sentiment, gen_text=gen_text_info, all_l=all_labels, all_d=all_datas, over=data[10][1], cont_gen=con_gen_text, avg_sl=data[1][1], avg_syll=data[1][7])


# TO GET SYNONYMS OF A WORD
# textSyn.getChange(word, True) - Returns 2d list of synonyms considered "harder"
# textSyn.getChange(word) - Returns 2d list of ALL found synonyms regardless of difficulty
# textSyn.getChange(word, False) - Returns 2d list of synonyms considered "easier"

if __name__ == '__main__':
    app.run()
