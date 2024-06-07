from elasticsearch import Elasticsearch
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv 
import os

load_dotenv()

class elasticsearch_api:
    def __init__(self):
        self.key = os.getenv("ELASTICSEARCH_API_KEY")
        self.url = os.getenv("ELASTICSEARCH_URL")
        self.client = Elasticsearch(
            self.url,
            api_key=self.key,
            verify_certs=False
        )

    def get_data(self, path, host=None):
        with open(path, 'r') as file:
            query_str = file.read()

        # Calculate timestamps for gte and lte
        now = datetime.utcnow()  # use UTC time
        week_ago = now - timedelta(weeks=1)

        # Format timestamps as strings
        gte_timestamp = week_ago.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        lte_timestamp = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        # Replace placeholders in the query string
        query_str = query_str.replace("this_should_be_start_time", gte_timestamp)
        query_str = query_str.replace("this_should_be_end_time", lte_timestamp)
        
        if host:
            query_str = query_str.replace("this_should_be_server_hostname", host)

        # Convert the modified query string back to JSON
        query = json.loads(query_str)

        response = self.client.search(index="*", body=query)

        return response

# Example usage
# elasticsearch = elasticsearch_api()
# response = elasticsearch.get_data('path_to_query.json', host='example_host')
# print(response)