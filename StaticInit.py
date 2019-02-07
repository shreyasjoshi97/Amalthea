import numpy as np
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pandas as pd

class StaticInit:
    data = ""
    model = ""

    def __init__(self):
        self.permissions = {}
        self.results = {}
        self.initialise_permissions()
        self.file = open("permissions.txt", "r")
        self.init_model()
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
                if permission in self.permissions:
                    self.permissions.update({permission: 1})
            prediction = list(self.permissions.values())
            prediction_array = np.array(prediction).reshape(1, -1)
            result = self.make_prediction(prediction_array)
            self.results.update({name: result[0]})
            self.initialise_permissions()
        print(self.results)
        return self.results

    def init_model(self):
        self.data = pd.read_csv("train.csv", sep=';')
        array = self.data.values
        X = array[:, 0:330]
        Y = array[:, 330]
        validation_size = 0.30
        seed = 10
        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size,
                                                                                        random_state=seed)

        # test = pd.read_csv("test.csv", sep=';')
        # test_values = test.values;
        # X_test = test_values[:, 0:330]
        # Y_test = test_values[:, 330]

        self.model =LogisticRegression(solver='lbfgs')
        self.model.fit(X_train, Y_train)

    def make_prediction(self, predictor):
        pred = self.model.predict(predictor)
        return pred

