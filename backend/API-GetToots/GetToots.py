import azure.functions as func
from mastodon import Mastodon
import os
import json
from datetime import datetime
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_mastodon_base_url():
    # For local development on mac use these to set the variables
    # launchctl setenv MASTODON_BASE_URL https://mastodon.world/
    # for Azure use this in an Azure Cloud Shell
    # az functionapp config appsettings set --name sentimentabot --resource-group Sentimentabot --settings "MASTODON_BASE_URL=https://mastodon.world/"
    return os.environ.get("MASTODON_BASE_URL")

def get_mastodon_api_key_in_azure():
    # For local development on mac use these to set the variables
    # launchctl setenv MASTODON_SENTIMENT_MASTODON_API_KEY [...]
    # for Azure use this in an Azure Cloud Shell
    # az functionapp config appsettings set --name sentimentabot --resource-group Sentimentabot --settings "KEY_VAULT_NAME=Sentimentabot-KV"

    keyVaultSecretNameForAPIKey = "mastodon-api-key"
    keyVaultName = os.environ.get("KEY_VAULT_NAME")
    keyVaultUri = f"https://{keyVaultName}.vault.azure.net"

    keyVaultCredential = DefaultAzureCredential()
    keyVaultClient = SecretClient(vault_url=keyVaultUri, credential=keyVaultCredential)

    print(f"Retrieving your {keyVaultSecretNameForAPIKey} from {keyVaultUri}.")
    mastodonAPIKey = keyVaultClient.get_secret(keyVaultSecretNameForAPIKey)
    return mastodonAPIKey.value

def get_mastodon_api_key():
    def use_environment_for_key():
        return 'MASTODON_SENTIMENT_MASTODON_API_KEY' in os.environ

    if use_environment_for_key():
        return os.environ.get('MASTODON_SENTIMENT_MASTODON_API_KEY')
    else:
        return get_mastodon_api_key_in_azure()

def my_serializer(o):
    if isinstance(o, datetime):
        return o.isoformat()

def main(req: func.HttpRequest) -> func.HttpResponse:
    mastodon = Mastodon(
        access_token= get_mastodon_api_key(),
        api_base_url= get_mastodon_base_url()  
    )
    
    search_term = req.params.get('search_term')

    if not search_term:
        return func.HttpResponse("Please pass a search_term in the query string.", status_code=400)
    
    # Fetch toots based on search term. Assuming MastodonAPI has a method get_toots_by_search_term
    # public_toots = mastodon.search_v2(q=search_term, result_type='statuses')
    
    return func.HttpResponse(
        json.dumps(mastodon.search_v2(q=search_term,result_type='statuses'),default=my_serializer),
        mimetype="application/json"
    )
