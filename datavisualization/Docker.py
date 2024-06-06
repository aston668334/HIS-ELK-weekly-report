import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import PercentFormatter
from ELK_module import elasticsearch_api
from dotenv import load_dotenv 
from .Datatemplate import Datatemplate  # Importing Datatemplate class from datatemplate.py
import os
load_dotenv()

class DockerCPU(Datatemplate):  # Inheriting from Datatemplate
    def __init__(self,host):
        super().__init__()  # Calling the constructor of the parent class
        self.json_name = "docker-cpu-usage.json"  # Overriding the json_name attribute
        self.host = host
        self.data = self.api.get_data(os.path.join(self.json_path, self.json_name),self.host) # Using the parent's methods and attributes


    def prepare_plot(self):
        # Extract the aggregation data
        buckets = self.data['aggregations']['0']['buckets']
        # Transform data into a DataFrame
        df = pd.DataFrame(buckets)
        # Extract the nested values
        df['user'] = df['1'].apply(lambda x: x['value'])
        df['system'] = df['2'].apply(lambda x: x['value'])
        df['nice'] = df['3'].apply(lambda x: x['value'])
        df['irq'] = df['4'].apply(lambda x: x['value'])
        df['softirq'] = df['5'].apply(lambda x: x['value'])
        df['iowait'] = df['6'].apply(lambda x: x['value'])
        # Drop the original nested columns
        df.drop(columns=['1', '2', '3', '4', '5', '6'], inplace=True)
        # Create the plot
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        # Set x-axis labels
        x_labels = df['key_as_string']
        # Plotting stacked bars
        self.ax.bar(x_labels, df['user'], width=0.5, align='center', label='user')
        self.ax.bar(x_labels, df['system'], bottom=df['user'], width=0.5, align='center', label='system')
        self.ax.bar(x_labels, df['nice'], bottom=df['user'] + df['system'], width=0.5, align='center', label='nice')
        self.ax.bar(x_labels, df['irq'], bottom=df['user'] + df['system'] + df['nice'], width=0.5, align='center', label='irq')
        self.ax.bar(x_labels, df['softirq'], bottom=df['user'] + df['system'] + df['nice'] + df['irq'], width=0.5, align='center', label='softirq')
        self.ax.bar(x_labels, df['iowait'], bottom=df['user'] + df['system'] + df['nice'] + df['irq'] + df['softirq'], width=0.5, align='center', label='iowait')
        # Rotate x-axis labels for better readability
        self.ax.set_xticklabels(x_labels, rotation=45, ha='right')
        # Add legend
        self.ax.legend()
        # Add labels and title
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Usage (%)')
        self.ax.set_title('CPU Usage Over Time({})'.format(self.host))
        # Change y-axis to percentage
        self.ax.yaxis.set_major_formatter(PercentFormatter(1.0))
        # Adjust layout
        self.fig.tight_layout()

    def show_plot(self):
        if self.fig is not None and self.ax is not None:
            plt.show()
        else:
            print("Plot has not been prepared. Call prepare_plot() first.")

    def save_plot(self, output_dir='output', filename='cpu_usage_over_time.png'):
        if self.fig is not None and self.ax is not None:
            # Ensure the output directory exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # Save plot to the output directory
            filename = 'cpu_usage_over_time_{}.png'.format(self.host)
            output_path = os.path.join(output_dir, filename)
            self.fig.savefig(output_path)
        else:
            print("Plot has not been prepared. Call prepare_plot() first.")

# Example usage
# Assuming `data` is the dictionary containing the JSON response
# data = ...
# docker_cpu = DockerCPU()
# docker_cpu.prepare_plot(data)
# docker_cpu.show_plot()
# docker_cpu.save_plot()