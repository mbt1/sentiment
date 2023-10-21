from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from bs4 import BeautifulSoup
import logging
from . import ReadEnvironment


class SentimentAnalyzer:

    def __init__(self):
        env_reader = ReadEnvironment.EnvironmentReader()
        endpoint = env_reader.languageModelEndpoint()
        key = env_reader.languageModelKey()
        self.text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    def clean_text(self, raw_text):
        soup = BeautifulSoup(raw_text, 'html.parser')
        return soup.get_text()

    def analyze_sentiment(self, raw_texts):
        cleaned_texts = [self.clean_text(text) for text in raw_texts]
        documents = [{"id": str(i+1), "language": "en", "text": cleaned_texts[i]} for i in range(len(cleaned_texts))]
        
        response = self.text_analytics_client.analyze_sentiment(documents=documents)
        
        results = []
        for resp in response:
            results.append((resp.sentiment, resp.confidence_scores))

        return results
    
