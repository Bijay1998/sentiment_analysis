from django.shortcuts import render
from django.http import HttpResponse
from numpy import character, var
from . import articleSentiment
from . import sentimentVader
from . import tweepy_sentiment
import mysql.connector as sql
from django.contrib import messages
from .forms import Sentiment_Imported_Tweet_analyse_form
from . import twitterSentimentAnalysis
from .twitterSentimentAnalysis import SentimentAnalysis
from .tweepy_sentiment import Import_tweet_sentiment
from .sentiment_analysis_code import sentiment_analysis_code

fn = ''
ln=''
em=''
reg=''
sub=''




def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def sLive(request):
    user_sentiment = str(request.GET.get('sentence'))
    obj= sentimentVader.sentimentVader(user_sentiment)
    prediction = obj.predict()  
    #only show result after the user has entered a sentence
    # also print the sentence and fade it after a few seconds

    if user_sentiment != '':
        return render(request, 'sLive.html', {'prediction': prediction, 'user_sentiment': user_sentiment})
    else:
        return render(request, 'sLive.html', {'prediction': 'Waiting.....'}) 
    


    
def sentiment_import_result_hashtag(request):
    return render(request, 'sentiment_import_result_hashtag.html')    

#function for importing and analyzing the tweets from twitter.
def sTwitter(request):  

    # if request.method == 'POST':
    #     form = Sentiment_Imported_Tweet_analyse_form(request.POST)
    #     tweet_text = Import_tweet_sentiment()
    #     analyse = sentiment_analysis_code()

    #     if form.is_valid():
    #         handle = form.cleaned_data['sentiment_imported_tweet']

    #         if handle[0]=='#':
    #             list_of_tweets = tweet_text.get_hashtag(handle)
    #             list_of_tweets_and_sentiments = []
    #             for i in list_of_tweets:
    #                 list_of_tweets_and_sentiments.append((i,analyse.get_tweet_sentiment(i)))
    #             args = {'list_of_tweets_and_sentiments':list_of_tweets_and_sentiments, 'handle':handle}
    #             return render(request, 'twitter_result_hashtag.html', args)

    #         list_of_tweets = tweet_text.get_tweets(handle)
    #         list_of_tweets_and_sentiments = []
    #         if handle[0]!='@':
    #             handle = str('@'+handle)
    #         for i in list_of_tweets:
    #             list_of_tweets_and_sentiments.append((i,analyse.get_tweet_sentiment(i)))
    #         args = {'list_of_tweets_and_sentiments':list_of_tweets_and_sentiments, 'handle':handle}
    #         return render(request, 'twitter_result.html', args)

    # else:
    #     form = Sentiment_Imported_Tweet_analyse_form()
    #     return render(request, 'sTwitter.html')


    if request.method == 'POST':
        form = Sentiment_Imported_Tweet_analyse_form(request.POST)
        #import the tweet

        tweet_text = Import_tweet_sentiment()
        #analyse = SentimentAnalysis()
        analyse = sentiment_analysis_code()

        if form.is_valid():
            handle = form.cleaned_data['sentiment_imported_tweet']

            if handle[0]=='#':
                list_of_tweets = tweet_text.get_hashtag(handle)
                list_of_tweets_and_sentiments = []
                for i in list_of_tweets:
                    #list_of_tweets_and_sentiments.append((i,analyse.predict_sentiment(i)))
                    list_of_tweets_and_sentiments.append((i,analyse.get_tweet_sentiment(i)))
                args = {'list_of_tweets_and_sentiments': list_of_tweets_and_sentiments, 'handle': handle}
                return render(request, 'twitter_result_hashtag.html', args)
               

               
            list_of_tweets = tweet_text.get_tweets(handle)
            list_of_tweets_and_sentiments = []
            if handle[0]!='@':
                handle = str('@'+handle)
            for i in list_of_tweets:
                #list_of_tweets_and_sentiments.append((i,analyse.predict_sentiment(i)))
                list_of_tweets_and_sentiments.append((i,analyse.get_tweet_sentiment(i)))
            args = {'list_of_tweets_and_sentiments':list_of_tweets_and_sentiments, 'handle':handle}            
            return render(request, 'twitter_result_hashtag.html', args)

    else:
        form = Sentiment_Imported_Tweet_analyse_form()   

        return render(request, 'sTwitter.html')




def sentimentUrl(request):
    return render(request, 'sentimentUrl.html')

def nav(request):
    return render(request, 'nav.html')

# def vaderResult(request):
#     user_sentiment = str(request.GET.get('sentence'))
#     obj= sentimentVader.sentimentVader(user_sentiment)
#     prediction = obj.predict()    
#     return render(request, 'vaderResult.html', {'prediction': prediction})

def urlResult(request):
    user_url = str(request.GET.get('url'))
    #handling the error if the url is not valid
    try:
        objArticle = articleSentiment.articleSentiment(user_url)
        prediction1 = objArticle.predict()
        summary = objArticle.generateSummary()
        return render(request, 'urlResult.html', {'prediction1': prediction1, 'summary': summary})
    except:
       #display error message as a visible message
        a= messages.error(request, 'Invalid URL')        
        
        return render(request, 'sentimentUrl.html' , {'a': a})


def twitter_result(request):
    return render(request, 'twitter_result.html')
    
        

        

    
    

def contact(request):
    global fn, ln, em, reg, sub
    if request.method == 'POST':
        m = sql.connect(host='localhost', user='root', password='root', database='users')
        cursor= m.cursor()
        d = request.POST
        for key, value in d.items():
            if key == 'firstname':
                fn = value
            if key == 'lastname':
                ln = value
            if key == 'email':
                #validating the email
                if '@' in value and '.' in value:
                    em = value
                else:
                    messages.error(request, 'Invalid Email')
                    return render(request, 'contact.html')
            
            if key == 'region':
                reg = value
            if key == 'subject':
                sub = value
        c = "INSERT INTO users(firstname, lastname, region, subject, email) VALUES('"+fn+"', '"+ln+"', '"+reg+"', '"+sub+"', '"+em+"')"
        cursor.execute(c)
        m.commit()
        messages.success(request, 'Feedback/message submitted successfully')
        cursor.close()
    return render(request, 'contact.html')
def feature(request):
    return render(request, 'feature.html')

def message(request):
    return render(request, 'message.html')

def twitter_result_hashtag(request):
    return render(request, 'twitter_result_hashtag.html')
    