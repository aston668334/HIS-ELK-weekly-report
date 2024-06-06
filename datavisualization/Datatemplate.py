import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import PercentFormatter
from ELK_module import elasticsearch_api
from dotenv import load_dotenv 
import os
load_dotenv()

class Datatemplate:
    def __init__(self):
        self.api = elasticsearch_api.elasticsearch_api()
        self.json_path = os.getenv("JSON_TEMPLATE_PATH")
