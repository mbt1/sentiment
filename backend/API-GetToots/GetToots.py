import logging
from . import ReadEnvironment
from . import SentimentAnalyzer
import azure.functions as func
from mastodon import Mastodon
import json
from datetime import datetime

def my_serializer(o):
    if isinstance(o, datetime):
        return o.isoformat()

def add_sentiments_to_statuses_inplace(statuses):
    raw_texts = [status['content'] for status in statuses]
    sentiment_analyzer = SentimentAnalyzer.SentimentAnalyzer()
    sentiments = sentiment_analyzer.analyze_sentiment(raw_texts=raw_texts)
    
    logging.critical(sentiments)
    for idx, status in enumerate(statuses):
        sentiment_result = sentiments[idx]
        status['sentiment'] = {
            'positive_score': sentiment_result[1].positive,
            'neutral_score': sentiment_result[1].neutral,
            'negative_score': sentiment_result[1].negative,
            'overall_sentiment': sentiment_result[0]
        }



def main(req: func.HttpRequest) -> func.HttpResponse:

    env_reader = ReadEnvironment.EnvironmentReader()

    logging.debug("GetToots started")

    mastodon = Mastodon(
        access_token= env_reader.mastodonAPIKey(),
        api_base_url= env_reader.mastodonBaseURL()  
    )
    
    search_term = req.params.get('search_term')

    if not search_term:
        return func.HttpResponse("Please pass a search_term in the query string.", status_code=400)
    
    # public_toots = mastodon.search_v2(q=search_term, result_type='statuses')
    max_id = None #111093673846648284 -1# 111093680257171174 - 100
    #print(max_id)
    statuses = (mastodon.search_v2(q=search_term,result_type='statuses',max_id=max_id))['statuses']
    add_sentiments_to_statuses_inplace(statuses=statuses)
    
    return func.HttpResponse(
        json.dumps(statuses,default=my_serializer),
        mimetype="application/json"
    )
