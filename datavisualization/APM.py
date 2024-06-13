import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import PercentFormatter
from ELK_module import elasticsearch_api
from dotenv import load_dotenv
from .Datatemplate import Datatemplate  # Importing Datatemplate class from datatemplate.py
import os
from datetime import datetime
load_dotenv()

class JVMCPU(Datatemplate):  # Inheriting from Datatemplate
    def __init__(self, host):
        super().__init__()  # Calling the constructor of the parent class
        self.json_name = "jvm-cpu-usage.json"  # Overriding the json_name attribute
        self.host = host

    def prepare_plot(self):
        self.get_data()
        print(self.data)
        # Extract the aggregation data
        # Function to convert timestamp to human-readable format
        # Function to convert timestamp to human-readable format
        def convert_timestamp(timestamp):
            return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

        # Extract data and organize it into a list of dictionaries
        data_list = []
        for bucket in self.data['aggregations']['0']['buckets']:
            service = bucket['key']
            for time_bucket in bucket['1']['buckets']:
                timestamp = time_bucket['key']
                doc_count = time_bucket['doc_count']
                value_50 = time_bucket['2']['values'].get('50.0')  # Use .get() to handle None gracefully
                if value_50 is not None:
                    time_str = convert_timestamp(timestamp)
                    data_list.append({
                        "service": service,
                        "time": time_str,
                        "doc_count": doc_count,
                        "value_50": value_50 * 100  # Convert to percentage
                    })

        # Create a pandas DataFrame
        df = pd.DataFrame(data_list)

        # Convert 'time' column to datetime
        df['time'] = pd.to_datetime(df['time'])

        # Plotting the data
        plt.figure(figsize=(10, 5))

        for service in df['service'].unique():
            service_data = df[df['service'] == service]
            plt.plot(service_data['time'], service_data['value_50'], label=service)

        plt.xlabel('Time')
        plt.ylabel('50th Percentile Value (%)')
        plt.title('50th Percentile Values Over Time (as %)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

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
        
        # Function to convert timestamp to human-readable format
        def convert_timestamp(timestamp):
            return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

        # Extract data and organize it into a list of dictionaries
        data_list = []
        for bucket in self.data['aggregations']['0']['buckets']:
            timestamp = bucket['key']
            for service_bucket in bucket['1']['buckets']:
                service = service_bucket['key']
                avg_memory_usage_bytes = service_bucket['2']['value']
                time_str = convert_timestamp(timestamp)
                # Convert bytes to GB
                avg_memory_usage_gb = avg_memory_usage_bytes / (1024 ** 3)
                data_list.append({
                    "service": service,
                    "time": time_str,
                    "avg_memory_usage_gb": avg_memory_usage_gb
                })

        # Create a pandas DataFrame
        df = pd.DataFrame(data_list)

        # Convert 'time' column to datetime
        df['time'] = pd.to_datetime(df['time'])

        # Pivot the DataFrame for stacked area chart
        df_pivot = df.pivot(index='time', columns='service', values='avg_memory_usage_gb')

        # Plot stacked area chart
        plt.figure(figsize=(14, 8))
        df_pivot.plot(kind='area', stacked=True)

        # Customize the plot
        plt.xlabel('Time')
        plt.ylabel('Memory Usage (GB)')
        plt.title('Memory Usage Over Time (GB)')
        plt.legend(title='Service', loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()

    def show_plot(self):
        plt.show()

    def save_plot(self, output_dir='output', filename='JVMMemory_usage_area_stacked.png'):
        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Save plot to the output directory
        output_path = os.path.join(output_dir, filename)
        plt.savefig(output_path)
# Example usage:
# docker_cpu = DockerCPU(host='my_host')
# docker_cpu.prepare_plot()
# docker_cpu.show_plot()
# docker_cpu.save_plot()

# docker_memory = DockerMemory(host='my_host')
# docker_memory.prepare_plot()
# docker_memory.show_plot()
# docker_memory.save_plot()
