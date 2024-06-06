import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import PercentFormatter
from ELK_module import elasticsearch_api

class PostgresLongQuery:

    def __init__(self):
        self.api = elasticsearch_api.elasticsearch_api()
        self.data = self.api.get_data('./api-json-template/postgres_duration_table.json') 

    def get_dataframe(self):

        hits = self.data.body['hits']['hits']
        # Extract the 'fields' from each log entry
        fields_data = [entry['fields'] for entry in hits]
        # Normalize the JSON data to create a DataFrame
        df = pd.json_normalize(fields_data)

        return df