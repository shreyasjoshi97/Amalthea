import numpy as np


class BehaviourAnalysis:
    data = []
    slots = []
    name = ""
    cpu_mean = 0
    rss_mean = 0

    def load_data(self, param, name):
        self.data = param
        self.name = name
        self.cpu_mean = param['CPU'].mean()
        self.rss_mean = param['RSS'].mean()
        self.slots = np.array_split(self.data, 4)
        total_spikes = self.determineSpike(self.slots[0]) + self.determineSpike(self.slots[1]) + self.determineSpike(self.slots[2]) + self.determineSpike(self.slots[3])
        print(name + ": " + str(total_spikes))

    def determine_spike(self, slot):
        cpu_extreme = self.getExtreme(slot, 'CPU')
        rss_extreme = self.getExtreme(slot, 'RSS')
        spike_recorded = 0;
        for entry in slot.itertuples():
            cpu_usage = getattr(entry, "CPU")
            rss_usage = getattr(entry, "RSS")

            if (cpu_usage > cpu_extreme) | (rss_usage > rss_extreme):
                spike_recorded = 1;
                break
        return spike_recorded

    def get_extreme(self, slot, var):
        q3 = slot[var].quantile(0.75)
        q1 = slot[var].quantile(0.25)
        iqr = q3 - q1
        outlier = 1.5 * iqr
        extreme = q3 + outlier
        return extreme
