 #making sentiment analysis model using LSTM trained model
import pickle
import re
import os
import itertools
import numpy as np
import nltk
from nltk.stem.wordnet import WordNetLemmatizer 


# Importing Keras library
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

#making class for sentiment analysis for twitter
class SentimentAnalysis:
    lem = WordNetLemmatizer()

    ModelPath = os.path.join(os.path.dirname(__file__), r"D:/UG/sentiment_analysis/sentiment_analysis/SentimentalAnalysis_LSTM.h5")
    # Loading the model
    model = load_model(ModelPath)
    #load tokenizer
    tokenizer = os.path.join(os.path.dirname(__file__), r"D:/UG/sentiment_analysis/sentiment_analysis/tokenizer.pickle")
    data = open(tokenizer, 'rb')
    tokenizer = pickle.load(data)

    # Cleaning the text
    def clean_text(self, text):
        txt = str(text)
        txt = re.sub(r'[^a-zA-Z\s]', '', txt)
        txt = txt.lower()
         
         #checking if the text lengt
        if len(txt) ==0:
            return "no text"
        else:
            txt = txt.split()
            index = 0
            for j in range(len(txt)):
                if txt[j][0] == '@':
                    index = j
            txt = np.delete(txt, index)
            if len(txt) == 0:
                return 'no text'
            else:
                words = txt[0]
                for k in range(len(txt)-1):
                    words+= " " + txt[k+1]
                txt = words
                txt = re.sub(r'[^\w]', ' ', txt)
                if len(txt) == 0:
                    return 'no text'
                else:
                    txt = ''.join(''.join(s)[:2] for _, s in itertools.groupby(txt))
                    txt = txt.replace("'", "")
                    txt = nltk.tokenize.word_tokenize(txt)
                    #data.content[i] = [w for w in data.content[i] if not w in stopset]
                    for j in range(len(txt)):
                        txt[j] = self.lem.lemmatize(txt[j], "v")
                    if len(txt) == 0:
                        return 'no text'
                    else:
                        return txt

        



        
  #function to get tweets
    def predict_sentiment(self, tweet):
        #cleaning the text
        tweet = self.clean_text(tweet)
        #tokenizing the text
        tweet = self.tokenizer.texts_to_sequences(tweet)
        #padding the text
        tweet = pad_sequences(tweet,maxlen=500)
        #predicting the sentiment
        prediction = self.model.predict(tweet)
        #returning the sentiment
        prediction = prediction[0][1]

        if prediction >= 0.7:
            return "Positive"	
        else:
            return "Negative"


    
       

        


    




# Defining the function to make the sentiment analysis
# def predict_sentiment(self, review):
#     ModelPath = os.path.join(os.path.dirname(__file__), r"D:/UG/sentiment_analysis/sentiment_analysis/SentimentalAnalysis_LSTM.h5")
#     # Loading the model
#     model = load_model(ModelPath)
#     #load tokenizer
#     tokenizer = os.path.join(os.path.dirname(__file__), r"D:/UG/sentiment_analysis/sentiment_analysis/tokenizer.pickle")
#     data = open(tokenizer, 'rb')
#     tokenizer = pickle.load(data)
#     # Cleaning the text
#     regex = re.compile(r'[^a-zA-Z\s]')
#     review = ''.join(review)
#     review = regex.sub('', review)
    
#     preprocess = tokenizer.texts_to_sequences([review])
#     preprocess=pad_sequences(preprocess,maxlen=500)
#     prediction = model.predict(preprocess)
#     prediction=prediction[0][1]
    
#     if prediction >= 0.5:
#         print('positive')
#     else:
#         print('negative')





#predict_sentiment('game is good')