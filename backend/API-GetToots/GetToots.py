import logging
from . import ReadEnvironment
import azure.functions as func
from mastodon import Mastodon
import json
from datetime import datetime

def my_serializer(o):
    if isinstance(o, datetime):
        return o.isoformat()

def main(req: func.HttpRequest) -> func.HttpResponse:

    env_reader = ReadEnvironment.EnvironmentReader()

    logging.critical("GetToots started")

    mastodon = Mastodon(
        access_token= env_reader.mastodonAPIKey(),
        api_base_url= env_reader.mastodonBaseURL()  
    )
    
    search_term = req.params.get('search_term')

    if not search_term:
        return func.HttpResponse("Please pass a search_term in the query string.", status_code=400)
    
    # Fetch toots based on search term. Assuming MastodonAPI has a method get_toots_by_search_term
    # public_toots = mastodon.search_v2(q=search_term, result_type='statuses')
    max_id = None #111093673846648284 -1# 111093680257171174 - 100
    #print(max_id)
    result = (mastodon.search_v2(q=search_term,result_type='statuses',max_id=max_id))['statuses']

    return func.HttpResponse(
        json.dumps(result,default=my_serializer),
        mimetype="application/json"
    )
