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
        stepSize = 10
        return [analysis for i in range(0,len(raw_texts),stepSize) for analysis in self.analyze_chunk(raw_texts[i:i+stepSize])]

    def analyze_chunk(self,raw_texts_chunk):
        documents = [{"id": str(i), "language": "en", "text": self.clean_text(text)} for (i,text) in enumerate(raw_texts_chunk,1)]
        return [(resp.sentiment, resp.confidence_scores) for resp in self.text_analytics_client.analyze_sentiment(documents=documents)]
    
