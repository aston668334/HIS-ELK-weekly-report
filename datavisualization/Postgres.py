import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from ELK_module import elasticsearch_api
from .Datatemplate import Datatemplate  # Importing Datatemplate class from datatemplate.py
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

class PostgresLongQuery(Datatemplate):
    def __init__(self):
        super().__init__()  # Calling the constructor of the parent class
        self.json_name = "postgres_duration_table.json"  # Overriding the json_name attribute
        self.data = self.api.get_data(os.path.join(self.json_path, self.json_name))

    def get_dataframe(self):
        hits = self.data['hits']['hits']
        fields_data = [entry['fields'] for entry in hits]
        df = pd.json_normalize(fields_data)
        return df
