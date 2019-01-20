from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pandas as pd


class StaticAnalysis:
    data = ""
    model = ""

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
        print('Making prediction')
        pred = self.model.predict(predictor)
        return pred
