from gramformer import Gramformer
import torch
from nltk import tokenize
from flask import Flask,render_template,request

app = Flask(__name__)
@app.route('/')
def home():
    print("Grammer check")
    return("Hello")

def set_seed(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

set_seed(1212)

@app.route('/grammer',methods=["POST"])
def gram():
    txt = ""
    c = " "
    tl = []
    cl = []
    req_Json = request.json
    txt = req_Json['text']

    print("Incorrect " , txt)
    gf = Gramformer(models = 1, use_gpu=False) # 1=corrector, 2=detector

    tl = tokenize.sent_tokenize(txt)
    print(tl)

    for i in tl:
            corrected_sentences = gf.correct(i, max_candidates=1)
            print("[Input] ", i)
            for corrected_sentence in corrected_sentences:
                print("[Correction] ",corrected_sentence)
                corrected_sentence = str(corrected_sentence)
                cl.append(corrected_sentence)
                print("-" *100)
    for i in cl:
          c = c + i
    #corrected_sentences = gf.correct(txt, max_candidates=1)
    #c = str(corrected_sentences)
    print("Corrected" , c)
    return(c)

@app.route('/grammerhtml',methods=["GET", "POST"])
def gramhtml():
  c = " "
  cl = []
  txthtml = ""
  tlhtml = []

  if request.method == "POST" :
    #txt = ""
    #req_Json = request.json
    #txt = req_Json['text']

    txthtml = request.form.get('txt')
    tlhtml = tokenize.sent_tokenize(txthtml)
    print(tlhtml)

    print("Incorrect Text : " , txthtml)
    gf = Gramformer(models = 1, use_gpu=False) # 1=corrector, 2=detector
    for i in tlhtml:
            corrected_sentences = gf.correct(i, max_candidates=1)
            print("[Input] ", i)
            for corrected_sentence in corrected_sentences:
                print("[Correction] ",corrected_sentence)
                corrected_sentence = str(corrected_sentence)
                cl.append(corrected_sentence)
                print("-" *100)
    for i in cl:
          c = c + i
    #print(c)
    #corrected_sentences = gf.correct(txthtml, max_candidates=1)
    #c = str(corrected_sentences)
    print("Corrected Text : " , c)
  return render_template('index.html', correct = c)