from flask import Flask, request, url_for, redirect, render_template, session
from TextAnalysis import TextAnalysis
from Synonym import Synonym
from subprocess import call
# from webui import WebUI
from os.path import dirname, abspath, join


app = Flask(__name__)
# ui = WebUI(app, debug=True)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
regular_calc = ""

textA = TextAnalysis.blank()
textSyn = Synonym()
data = []

original_grad = 0
original_grad = 10

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/stats', methods=['POST'])
def stats():
    text = request.form['text']
    if text is '':
        return ('', 204)
    print(text)
    session["all_text"]=text
    data = textA.auto(text)
    print(data)
    text_sentiment = [data[0][0], data[0][1], data[0][2], data[0][3]]
    gen_text_info = [data[1][0], data[1][1],data[1][6], data[1][7]]
    con_gen_text = [data[1][2], data[1][3], data[1][4]]

    all_labels = ['fre_s', 'fre_g', 'fkg_s', 'fkg_g', 'gfi_s', 'gfi_g', 'si_s', 'si_g', ' ari_s', 'ari_g', 'cli_s', 'cli_g', 'lwi_s', 'lwi_g', 'dcr_s', 'dcr_g']
    all_datas = [data[2][2], data[3][2], data[4][2], data[5][2], data[6][2], data[7][2], data[8][2], data[9][2], data[10][2]]
    print("++++++: "+str(all_datas))
    print(gen_text_info)
    return render_template('stats.html', comp=data[0][0], neg=data[0][1],pos=data[0][2], neut=data[0][3],
                           sent=data[1][0], sent_len=data[1][1], syll=data[1][2], word=data[1][3], char=data[1][4],
                           char_nospc=data[1][5], avg_c=data[1][6], syll_per_word=data[1][7], fre_s=data[2][0],
                           fre_g=data[2][1], fkg_s=data[3][0], fkg_g=data[3][1], gfi_s=data[4][0],
                           gfi_g=data[4][1], si_s=data[5][0], si_g=data[5][1], ari_s=data[6][0], ari_g=data[6][1],
                           cli_s=data[7][0], cli_g=data[7][1], lwi_s=data[8][0], lwi_g=data[8][1],
                           dcr_s=data[9][0], dcr_g=data[9][1], dataA = text_sentiment, gen_text=gen_text_info,
                           all_l=all_labels, all_d=all_datas, over=data[10][1], overG=data[10][0],
                           cont_gen=con_gen_text, avg_sl=data[1][1], avg_syll=data[1][7],
                           fre_gph=data[2][2], fkg_gph=data[3][2], gfi_gph=data[4][2], si_gph=data[5][2],
                           ari_gph=data[6][2], cli_gph=data[7][2], lwi_gph=data[8][2], dcr_gph=data[9][2],
                           overGph=data[10][2])



@app.route('/review', methods=['GET', 'POST'])
def review():
    tot = []
    session["words_all"] = []
    session["string_start"] = "<p>"
    grade = request.form['someid']
    if not(grade.isdigit()):
         return ('', 204)
    print("id: "+grade)
    all_lines = session["all_text"].splitlines()
    final = []
    if(int(grade)>original_grad):
        type_e = "harder"

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
                            session["string_start"]+= word+". "
                            sec_flag = True
                        else:
                            session["string_start"]+= word+" "
                    if(len(choices)>0):
                        session["string_start"]+=" <select class=\"someSel\" name=\""+word+"\">"
                        session["string_start"]+= "<option class=\"others\" value=\""+word+"\">"+word+"</option>"
                        for choice in choices:
                            session["string_start"]+= "<option class=\"others\" value=\""+choice[0]+"\">"+choice[0]+"</option>"
                        session["string_start"]+= "</select></span> "
                else:
                    if per_flag:
                        session["string_start"] += word + ". "
                        sec_flag = True
                    else:
                        session["string_start"] += word + " "
                if per_flag and not sec_flag:
                    session["string_start"]+=". "
                tot.append(word)
                session["words_all"].append(tot)

            session["string_start"]+="<br>"
            session["words_all"]+=["!BREAK!"]
        session["string_start"] += "</p>"
        print(session["string_start"])
    else:
        type_e = "easier"
        session["string_start"] = "<p>"

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
                            session["string_start"] += word + ". "
                            sec_flag = True
                        else:
                            session["string_start"] += word + " "
                    if (len(choices) > 0):
                        session["string_start"] += " <select class=\"someSel\" name=\"" + word + "\">"
                        session["string_start"] += "<option class=\"others\" value=\"" + word + "\">" + word + "</option>"
                        for choice in choices:
                            session["string_start"] += "<option class=\"others\" value=\"" + choice[0] + "\">" + choice[
                                0] + "</option>"
                        session["string_start"] += "</select></span> "
                else:
                    if per_flag:
                        session["string_start"] += word + ". "
                        sec_flag = True
                    else:
                        session["string_start"] += word + " "
                if per_flag and not sec_flag:
                    session["string_start"] += ". "
                tot.append(word)
                session["words_all"].append(tot)

            session["string_start"] += "<br>"
            session["words_all"] += ["!BREAK!"]
        session["string_start"] += "</p>"
        print(session["string_start"])


    return render_template('review.html', type_a = type_e, all_dat=session["string_start"])


@app.route('/finish', methods=['GET', 'POST'])
def finish():
    edited=""
    for wordList in session["words_all"]:
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
    return render_template('finish.html', final=edited)


# TO GET SYNONYMS OF A WORD
# textSyn.getChange(word, True) - Returns 2d list of synonyms considered "harder"
# textSyn.getChange(word) - Returns 2d list of ALL found synonyms regardless of difficulty
# textSyn.getChange(word, False) - Returns 2d list of synonyms considered "easier"

if __name__ == '__main__':
    context = ('fullchain.pem', 'privkey.pem')
    app.run(host='0.0.0.0', port = 443, ssl_context=context, threaded=True)