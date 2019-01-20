import StaticAnalysis
import numpy as np


class StaticInit:
    def __init__(self):
        self.permissions = {}
        self.results = {}
        self.initialise_permissions()
        self.file = open("permissions.txt", "r")
        self.static_analysis = StaticAnalysis.StaticAnalysis()
        self.static_analysis.init_model()
        self.initialise_results()

    def initialise_permissions(self):
        p = open("permissiontypes.txt")
        for x in p:
            name = x[:-1]
            self.permissions.update({name: 0})

    def initialise_results(self):
        for x in self.file:
            line = x.split(',')
            name = line[0]
            line.pop(0)
            for permission in line:
                print(permission)
                if permission in self.permissions:
                    self.permissions.update({permission: 1})
            prediction = list(self.permissions.values())
            prediction_array = np.array(prediction).reshape(1, -1)
            result = self.static_analysis.make_prediction(prediction_array)
            self.results.update({name: result[0]})
            self.initialise_permissions()
        print(self.results)
