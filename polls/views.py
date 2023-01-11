from pprint import pprint

from django.http import HttpResponse
from django.template import loader
from TwitterSearch import *
from textblob import TextBlob


def index(request):
    try:
        tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
        tso.set_keywords(['covid usa'])  # let's define all words we would like to have a look for
        tso.set_language('en')  # we want to see German tweets only
        tso.set_include_entities(False)  # and don't give us all those entity information

        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key='kNUlFVnkKaDHL2LmbFCcL3vB9',
            consumer_secret='IRoCoL6qDxio3iirC63sPwswkh20cJXpzBCzsAJ3anzvUbkAHL',
            access_token='1492044764799115266-IYcwOMQ6Yd6TCuKSqwh0nfJyfTUtoS',
            access_token_secret='4scpXoux5uPhZwS6jlEt3kCb2ORtUB1Was13htrSCy7vy'
        )

        data = ts.search_tweets_iterable(tso)

        sentiments = {}

        for tweet in data:
            analysis = TextBlob(tweet['text'])
            if analysis.sentiment[0] > 0:
                sentiments.update({tweet['text']: "Positive"})
            elif analysis.sentiment[0] < 0:
                sentiments.update({tweet['text']: "Negative"})
            else:
                sentiments.update({tweet['text']: "Neutral"})

        template = loader.get_template('polls/index.html')
        context = {
            'sentiments': sentiments
        }

        return HttpResponse(template.render(context, request))

        # this is where the fun actually starts :)
        # for tweet in ts.search_tweets_iterable(tso):
        #     print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

    except TwitterSearchException as e:  # take care of all those ugly errors if there are some
        print(e)

