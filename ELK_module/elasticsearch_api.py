from elasticsearch import Elasticsearch
import json
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv 
import os
load_dotenv()

class elasticsearch_api:
    def __init__(self):
        self.key=os.getenv("ELASTICSEARCH_API_KEY")
        self.url=os.getenv("ELASTICSEARCH_URL")
        self.client = Elasticsearch(
            self.url,  # Elasticsearch endpoint
            api_key=self.key,
            verify_certs=False
        )


    def get_data(self,path,host = None):
        with open(path, 'r') as file:
            query = json.load(file)
        # Calculate timestamps for gte and lte
        now = datetime.now()
        week_ago = now - timedelta(weeks=1)

        # Format timestamps as strings
        gte_timestamp = week_ago.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        lte_timestamp = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        # Update the query with formatted timestamps
        query['query']['bool']['filter'][2]['range']['@timestamp']['gte'] = gte_timestamp
        query['query']['bool']['filter'][2]['range']['@timestamp']['lte'] = lte_timestamp

        if host:
            query['query']['bool']['filter'][0]['match_phrase']['host.name'] = host

        response = self.client.search(index="*", body=query)

        return response