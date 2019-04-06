import pandas as pd
import math
import numpy as np


class DeltaCalculator:
    def __init__(self):
        self.df = pd.read_csv("delta.csv")

        vss_arr = []
        rss_arr = []
        cpu_arr = []

        for vss in self.df['VSS']:
            vss_val = float(vss[:-1])
            vss_arr.append(vss_val)

        for rss in self.df['RSS']:
            rss_val = float(rss[:-1])
            rss_arr.append(rss_val)

        for cpu in self.df['CPU']:
            cpu_val = float(cpu[:-1])
            cpu_arr.append(cpu_val)

        self.df['VSS'] = vss_arr
        self.df['RSS'] = rss_arr
        self.df['CPU'] = cpu_arr
        self.df['Time'] = pd.to_datetime(self.df['Time'])
        self.df['Mem Ratio'] = self.df['RSS'] / self.df['VSS']
        self.df.fillna(value=0, inplace=True)
    
    def load_data(self, name, data):
        delta_list = []
        active = data[data['PCY'] == 'fg']
        idle = data[data['PCY'] == 'bg']
        delta_list.extend(self.get_stat_list(active, 'CPU'))
        delta_list.extend(self.get_stat_list(idle, 'CPU'))
        delta_list.extend(self.get_stat_list(active, 'Mem Ratio'))
        delta_list.extend(self.get_stat_list(idle, 'Mem Ratio'))

        result = name + ',' + ','.join(delta_list) + "$"
        # result = name + "," + str(avg_active_cpu) + "," + str(avg_idle_cpu) + "," + str(avg_active_mem) + "," + \
        #          str(avg_idle_mem) + "$"
        return result

    def get_stat_list(self, data, column):
        stat_list = []
        stat_list.append(str(data[column].quantile(0.25)))
        stat_list.append(str(data[column].median()))
        stat_list.append(str(data[column].quantile(0.75)))
        return stat_list

    def get_delta(self, slot, column):
        min_value = slot[column].min()
        max_value = slot[column].max()
        delta = max_value - min_value
    
        if math.isnan(delta):
            delta = 0
    
        return delta

    def begin_analysis(self):
        results = ''
        process_names = self.df['Name'].unique()
        # load_data()

        for process in process_names:
            data = self.df.loc[self.df['Name'] == process]
            result = self.load_data(process, data)
            results += result
        return results
