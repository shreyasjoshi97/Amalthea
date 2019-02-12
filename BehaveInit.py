import pandas as pd
import numpy as np
import time as t
from datetime import datetime


class BehaveInit:
    df = ''


    def load_data(self, name, data):
        slots = np.array_split(data, 4)
        ovr_active = 0
        ovr_idle = 0
        ovr_cpu = 0
        for slot in slots:
            active = slot[slot['PCY'] == 'fg']
            idle = slot[slot['PCY'] == 'bg']
            active_delta = self.get_delta(active)
            ovr_active += active_delta
            idle_delta = self.get_delta(idle)
            ovr_idle += idle_delta
            ovr_cpu = slot['CPU']
        avg_active = ovr_active / 4
        avg_idle = ovr_idle / 4
        print(name + "\n-------------------------")
        print("Active: " + str(avg_active) + "\nIdle: " + str(avg_idle))
        print("-------------------------")
    
    def get_delta(self, slot):
        min_value = slot['Mem Ratio'].min()
        max_value = slot['Mem Ratio'].max()
        delta = max_value - min_value
        return delta
    
    def __init__(self):
        start = t.time()
        time_taken = datetime.strptime("2019-02-10 17:43:38.244", "%Y-%m-%d %H:%M:%S.%f")
        self.df = pd.read_csv("SampleLogs.csv")
        
        # print(self.df.head())
        # print(self.df.iloc[0])
        
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
        self.df['Mem Ratio'] = self.df['RSS']/self.df['VSS']
        self.df.fillna(value=0, inplace=True)
        
        
        hours = []
        for time in self.df['Time']:
            dtime = time - time_taken
            time_column = int(dtime.seconds / 60)
            hours.append(time_column)
        
        self.df['Hour'] = hours

        def create_output(self):
            process_names = self.df['Name'].unique()
            # load_data()

            for process in process_names:
                data = self.df.loc[self.df['Name'] == process]
                self.load_data(process, data)

            end = t.time()
            diff = end - start
            print("Execution time: " + str(diff))

