try:
	import tkinter as tk
	from tkinter import *
except ImportError:
	import Tkinter as tk
	from Tkinter import *

import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import json
import pickle
from keras.models import load_model
model = load_model('chatbot_model.h5')
import random
import numpy as np

intents = json.loads(open('covid19_dataset.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
 	ints = predict_class(msg, model)
 	res = getResponse(ints, intents)
 	return res
	
def send():
# 	msg = entrybox.get("1.0",'end-1c').strip()
	msg = entrybox.get().strip()		
	entrybox.delete(0, tk.END)

	if msg != '':
		chatlog.config(state=tk.NORMAL)
		chatlog.insert(tk.END, "You: " + msg + '\n\n')
		chatlog.config(foreground="#442265", font=("Verdana", 12 ))
		
		res = chatbot_response(msg)
		chatlog.insert(tk.END, "Bot: " + res + '\n\n')
		
		chatlog.config(state=tk.DISABLED)
		chatlog.yview(tk.END)	

master = tk.Tk()
master.title("COVID-19 - ChatBot 1.0")
tk.Label(master, text="COVID-19").grid(row=0, columnspan=2)
tk.Label(master, text="Type your questions here:").grid(row=3, columnspan=2)

chatlog = tk.Text(master, height=20, width=40, bg="lightgray")
chatlog.config(state="disabled")
scrollbar = tk.Scrollbar(master, command=chatlog.yview)
chatlog['yscrollcommand'] = scrollbar.set
chatlog.grid(row=1, columnspan=2)

entrybox = tk.Entry(master, width=20)
entrybox.bind("<Return>", send)
entrybox.grid(row=4, column=0, padx=5, pady=5)
									
tk.Button(master, text='Send', command=send).grid(row=4, 
                                                               column=1, 
                                                               sticky=tk.W, 
                                                               pady=4)

master.mainloop()