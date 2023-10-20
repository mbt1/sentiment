import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# For local development on mac use these to set the variables
# launchctl setenv MASTODON_BASE_URL https://mastodon.world/
# launchctl setenv MASTODON_SENTIMENT_LANGUAGE_MODEL_ENDPOINT https://sentimentabotlanguagemodel.cognitiveservices.azure.com/
# launchctl setenv MASTODON_SENTIMENT_MASTODON_API_KEY [...]
# launchctl setenv MASTODON_SENTIMENT_LANGUAGE_MODEL_KEY [...]

# for Azure use this in an Azure Cloud Shell
# az account set --subscription [...]
# az functionapp config appsettings set --name sentimentabot --resource-group Sentimentabot --settings "MASTODON_BASE_URL=https://mastodon.world/"
# az functionapp config appsettings set --name sentimentabot --resource-group Sentimentabot --settings "MASTODON_SENTIMENT_LANGUAGE_MODEL_ENDPOINT=https://sentimentabotlanguagemodel.cognitiveservices.azure.com/"
# az functionapp config appsettings set --name sentimentabot --resource-group Sentimentabot --settings "KEY_VAULT_NAME=Sentimentabot-KV"
# az keyvault secret set --vault-name "Sentimentabot-KV" --content-type "text/plain" --name "language-model-api-key" --value "..."
# az keyvault secret set --vault-name "Sentimentabot-KV" --content-type "text/plain" --name "mastodon-api-key" --value "..."

class EnvironmentReader:
    _MASTODON_API_KEY = None
    _MASTODON_BASE_URL = None
    _LANGUAGE_MODEL_ENDPOINT = None
    _LANGUAGE_MODEL_KEY = None
    _KEY_VAULT_NAME = None

    _KEY_VAULT_SECRET_NAME_FOR_LANGUAGE_MODEL_KEY = "language-model-api-key"
    _ENV_VARIABLE_NAME_FOR_LANGUAGE_MODEL_KEY = 'MASTODON_SENTIMENT_LANGUAGE_MODEL_KEY'
    _ENV_VARIABLE_NAME_FOR_LANGUAGE_MODEL_ENDPOINT = 'MASTODON_SENTIMENT_LANGUAGE_MODEL_ENDPOINT'

    _ENV_VARIABLE_NAME_FOR_MASTODON_API_KEY = 'MASTODON_SENTIMENT_MASTODON_API_KEY'
    _ENV_VARIABLE_NAME_FOR_MASTODON_BASE_URL = 'MASTODON_BASE_URL'
    _KEY_VAULT_SECRET_NAME_FOR_MASTODON_API_KEY = "mastodon-api-key"

    _ENV_VARIABLE_NAME_FOR_KEY_VAULT_NAME = 'MASTODON_SENTIMENT_KEY_VAULT_NAME'

    def _get_environment_variable(self, key):
        return os.environ.get(key)

    def _get_secret(self, secret_name):
        keyVaultUri = f"https://{self._KEY_VAULT_NAME}.vault.azure.net"
        keyVaultCredential = DefaultAzureCredential()
        keyVaultClient = SecretClient(vault_url=keyVaultUri, credential=keyVaultCredential)

        mastodonAPIKey = keyVaultClient.get_secret(secret_name)
        return mastodonAPIKey.value

    def _use_keyvault(self):
        return self._ENV_VARIABLE_NAME_FOR_KEY_VAULT_NAME in os.environ

    def _get_secret_locally_or_vault(self, env_variable_name, secret_name):
        if self._use_keyvault():
            return self._get_secret(secret_name)
        else:
            return self._get_environment_variable(env_variable_name)

    def __init__(self):
        self._KEY_VAULT_NAME = self._get_environment_variable(self._ENV_VARIABLE_NAME_FOR_KEY_VAULT_NAME)
        self._MASTODON_BASE_URL = self._get_environment_variable(self._ENV_VARIABLE_NAME_FOR_MASTODON_BASE_URL)
        self._MASTODON_API_KEY = self._get_secret_locally_or_vault(self._ENV_VARIABLE_NAME_FOR_MASTODON_API_KEY, self._ENV_VARIABLE_NAME_FOR_MASTODON_API_KEY)
        self._LANGUAGE_MODEL_ENDPOINT = self._get_environment_variable(self._ENV_VARIABLE_NAME_FOR_LANGUAGE_MODEL_ENDPOINT)
        self._LANGUAGE_MODEL_KEY = self._get_secret_locally_or_vault(self._ENV_VARIABLE_NAME_FOR_LANGUAGE_MODEL_KEY, self._KEY_VAULT_SECRET_NAME_FOR_LANGUAGE_MODEL_KEY)

    def mastodonBaseURL(self):
        return self._MASTODON_BASE_URL
    
    def mastodonAPIKey(self):
        return self._MASTODON_API_KEY
    
    def languageModelKey(self):
        return self._LANGUAGE_MODEL_KEY
    
    def languageModelEndpoint(self):
        return self._LANGUAGE_MODEL_ENDPOINT
