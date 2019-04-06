import pandas as pd


class AverageCalculator:
    df = None

    def __init__(self):
        self.df = pd.read_csv("averages.csv")

    def find_averages(self, name, data):
        avg_list = []
        avg_list.append(str(data['active_cpu_q1'].mean()))
        avg_list.append(str(data['active_cpu_q2'].mean()))
        avg_list.append(str(data['active_cpu_q3'].mean()))
        avg_list.append(str(data['idle_cpu_q1'].mean()))
        avg_list.append(str(data['idle_cpu_q2'].mean()))
        avg_list.append(str(data['idle_cpu_q3'].mean()))
        avg_list.append(str(data['active_mem_q1'].mean()))
        avg_list.append(str(data['active_mem_q2'].mean()))
        avg_list.append(str(data['active_mem_q3'].mean()))
        avg_list.append(str(data['idle_mem_q1'].mean()))
        avg_list.append(str(data['idle_mem_q2'].mean()))
        avg_list.append(str(data['idle_mem_q3'].mean()))

        result = name + ',' + ','.join(avg_list) + "$"

        # result = name + "," + str(avg_active_cpu) + "," + str(avg_idle_cpu) + "," + str(avg_active_mem) + "," + \
        #          str(avg_idle_mem) + "$"
        return result

    def begin_analysis(self):
        results = ''
        process_names = self.df['Name'].unique()

        for process in process_names:
            data = self.df.loc[self.df['Name'] == process]
            results += self.find_averages(process, data)
        return results
