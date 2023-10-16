import azure.functions as func
from mastodon import Mastodon
import os
import json

@func.HttpTrigger
def main(req: func.HttpRequest) -> func.HttpResponse:
    mastodon = Mastodon(
        access_token=os.environ.get('MASTODON_SENTIMENT_MASTODON_API_KEY'),
        api_base_url='https://mas.to/'  # Replace with the Mastodon instance URL
    )
    
    public_toots = mastodon.timeline_public()
    
    return func.HttpResponse(
        json.dumps(public_toots),
        mimetype="application/json"
    )
