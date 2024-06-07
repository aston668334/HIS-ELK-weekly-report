import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import PercentFormatter
from ELK_module import elasticsearch_api
from dotenv import load_dotenv
from .Datatemplate import Datatemplate  # Importing Datatemplate class from datatemplate.py
import os
load_dotenv()

class JVMCPU(Datatemplate):  # Inheriting from Datatemplate
    def __init__(self, host):
        super().__init__()  # Calling the constructor of the parent class
        self.json_name = "docker-cpu-usage.json"  # Overriding the json_name attribute
        self.host = host

    def prepare_plot(self):
        self.get_data()
        # Extract the aggregation data
        buckets = self.data['aggregations']['0']['buckets']
        print(buckets)
        # Transform data into a DataFrame
        # Extracting data
        records = []
        for entry in buckets:
            record = {
                'timestamp': entry['key_as_string'],
                'timestamp_ms': entry['key'],
                'doc_count': entry['doc_count'],
                'value_1': entry['1']['value'],
                'value_2': entry['2']['value'],
                'value_3': entry['3']['value'],
                'value_4': entry['4']['value'],
                'value_5': entry['5']['value'],
                'value_6': entry['6']['value'],
            }
            records.append(record)

        # Creating the DataFrame
        df = pd.DataFrame(records)
        return df

        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Create the plot
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        # Plotting stacked bars
        df.set_index('timestamp').plot(kind='bar', stacked=True, ax=self.ax, width=0.5)

        # Customize the plot
        self.ax.set_xticklabels(df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S'), rotation=45, ha='right')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Usage (%)')
        self.ax.set_title('CPU Usage Over Time ({})'.format(self.host))
        self.ax.yaxis.set_major_formatter(PercentFormatter(1.0))
        self.ax.legend(loc='lower left', title='CPU Usage')  # Set legend to bottom left
        self.fig.tight_layout()

    def show_plot(self):
        if self.fig is not None and self.ax is not None:
            plt.show()
        else:
            print("Plot has not been prepared. Call prepare_plot() first.")

    def save_plot(self, output_dir='output', filename='Services_cpu_usage_over_time.png'):
        if self.fig is not None and self.ax is not None:
            # Ensure the output directory exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # Save plot to the output directory
            filename = 'Services_cpu_usage_over_time_{}.png'.format(self.host)
            output_path = os.path.join(output_dir, filename)
            self.fig.savefig(output_path)
        else:
            print("Plot has not been prepared. Call prepare_plot() first.")


class JVMMemory(Datatemplate):  # Inheriting from Datatemplate
    def __init__(self, host):
        super().__init__()  # Calling the constructor of the parent class
        self.json_name = "jvm-memory-usage.json"  # Overriding the json_name attribute
        self.host = host

    def prepare_plot(self):
        self.get_data()
        # Extract the aggregation data
        buckets = self.data['aggregations']['0']['buckets']

        # Extracting data
        records = []
        for entry in buckets:
            for bucket in entry['1']['buckets']:
                record = {
                    'service_name': entry['key'],
                    'total_doc_count': entry['doc_count'],
                    'timestamp': bucket['key_as_string'],
                    'timestamp_ms': bucket['key'],
                    'doc_count': bucket['doc_count'],
                    'avg_memory_usage_bytes': bucket['2']['value']
                }
                records.append(record)

        # Creating the DataFrame
        df = pd.DataFrame(records)

        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Convert value from bytes to GB
        df['value'] = df['avg_memory_usage_bytes'] / (1024 ** 3)

        # Pivot the DataFrame
        df_pivot = df.pivot(index='timestamp', columns='service_name', values='value')

        # Plot stacked area chart
        self.fig, self.ax = plt.subplots(figsize=(14, 8))
        df_pivot.plot(kind='area', stacked=True, ax=self.ax)

        # Customize the plot
        self.ax.set_title('Services Memory Usage')
        self.ax.set_xlabel('Timestamp')
        self.ax.set_ylabel('Memory (GB)')
        self.ax.legend(loc='lower left', title='Services')  # Set legend to bottom left
        self.fig.tight_layout()

    def show_plot(self):
        if self.fig is not None and self.ax is not None:
            plt.show()
        else:
            print("Plot has not been prepared. Call prepare_plot() first.")

    def save_plot(self, output_dir='output', filename='Services_memory_usage_over_time_.png'):
        if self.fig is not None and self.ax is not None:
            # Ensure the output directory exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # Save plot to the output directory
            filename = 'Services_memory_usage_over_time_{}.png'.format(self.host)
            output_path = os.path.join(output_dir, filename)
            self.fig.savefig(output_path)
        else:
            print("Plot has not been prepared. Call prepare_plot() first.")

# Example usage:
# docker_cpu = DockerCPU(host='my_host')
# docker_cpu.prepare_plot()
# docker_cpu.show_plot()
# docker_cpu.save_plot()

# docker_memory = DockerMemory(host='my_host')
# docker_memory.prepare_plot()
# docker_memory.show_plot()
# docker_memory.save_plot()
