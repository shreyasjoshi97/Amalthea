from Amalthea import BehaviourAnalysis
from datetime import datetime
import pandas as pd


class BehaviourInit:
    def __init__(self):
        self.time_taken = datetime.strptime("2018-12-23 17:18:46.242", "%Y-%m-%d %H:%M:%S.%f")
        self.df = pd.read_csv("behaviour.csv")
        self.vss_arr = []
        self.rss_arr = []
        self.cpu_arr = []
        self.process_names = ""

    def process_data(self):
        for vss in self.df['VSS']:
            vss_val = float(vss[:-1])
            self.vss_arr.append(vss_val)

        for rss in self.df['RSS']:
            rss_val = float(rss[:-1])
            self.rss_arr.append(rss_val)

        for cpu in self.df['CPU']:
            cpu_val = float(cpu[:-1])
            self.cpu_arr.append(cpu_val)

        self.df['VSS'] = self.vss_arr
        self.df['RSS'] = self.rss_arr
        self.df['CPU'] = self.cpu_arr
        self.df['Time'] = pd.to_datetime(self.df['Time'])

        hours = []
        for time in self.df['Time']:
            dtime = time - self.time_taken
            timecolumn = int(dtime.seconds / 60)
            hours.append(timecolumn)

        self.df['Hour'] = hours
        self.process_names = self.df['Name'].unique()

    def begin_analysis(self):
        for process in self.process_names:
            data = self.df.loc[self.df['Name'] == process]
            analyse = BehaviourAnalysis.Analyse()
            analyse.loadData(data, process)
