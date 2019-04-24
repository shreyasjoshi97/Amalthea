import pandas as pd


class BehaviourChange:
    def __init__(self):
        self.df = pd.read_csv("behaviour.csv")

    def load_data(self, name, data):
        diff_list = []
        diff_list.append(str(self.get_diff(data, 'active_cpu_q1')))
        diff_list.append(str(self.get_diff(data, 'active_cpu_q2')))
        diff_list.append(str(self.get_diff(data, 'active_cpu_q3')))
        diff_list.append(str(self.get_diff(data, 'idle_cpu_q1')))
        diff_list.append(str(self.get_diff(data, 'idle_cpu_q2')))
        diff_list.append(str(self.get_diff(data, 'idle_cpu_q3')))
        diff_list.append(str(self.get_diff(data, 'active_mem_q1')))
        diff_list.append(str(self.get_diff(data, 'active_mem_q2')))
        diff_list.append(str(self.get_diff(data, 'active_mem_q3')))
        diff_list.append(str(self.get_diff(data, 'idle_mem_q1')))
        diff_list.append(str(self.get_diff(data, 'idle_mem_q2')))
        diff_list.append(str(self.get_diff(data, 'idle_mem_q3')))

        result = name + ',' + ','.join(diff_list) + "$"

        # result = name + "," + str(diff_active_cpu) + "," + str(diff_idle_cpu) + "," + str(diff_active_mem) + "," + \
        #          str(diff_idle_mem) + "$"
        return result

    def get_diff(self, data, column):
        q3 = data[column].quantile(0.75)
        maximum = data[column].max()

        if q3 == 0:
            if maximum != 0:
                percentage_change = maximum
            elif maximum == 0:
                percentage_change = 0
        else:
            diff = maximum - q3
            percentage_change = diff / q3

        percentage_change = round(percentage_change, 2)

        return percentage_change

    def begin_analysis(self):
        results = ''
        process_names = self.df['Name'].unique()

        for process in process_names:
            data = self.df.loc[self.df['Name'] == process]
            results += self.load_data(process, data)
        return results
