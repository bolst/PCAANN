import os
import xlsxwriter
import pandas as pd
import numpy as np
import utils
import sklearn.preprocessing as sk
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import callbacks

RESULTS_DIR = 'PCA-ANN-code/RESULTS'


class ANN:

    def __init__(self,
                 path,
                 Framework='TensorFlow',
                 Optimizer='adam',
                 Activation='relu',
                 Loss='categorial_crossentropy',
                 Epochs=200,
                 BatchSize=64,
                 Patience=range(20, 50, 5),
                 HiddenNodes=range(80, 180, 10),
                 Runs=3,
                 ClassNumber=3,
                 PrincipalComponents=10
                 ):
        print('uh1h')

        # check input file
        m = self.checkInput(path)
        if len(m) != 0:
            raise ValueError(m)
        print('uhh2')
        self.input_filename, self.input_file_extension = os.path.splitext(path)
        # output stored in file with same name as input suffixed with "-ANNResults"
        self.output_filename = RESULTS_DIR + '/' + \
            self.input_filename.split('/')[-1] + '-ANNRESULTS.xlsx'

        self.workbook = xlsxwriter.Workbook(self.output_filename)
        self.data = self.workbook.add_worksheet('Opt')

        # make dict of excel header index for each category
        # this way if another category is to be removed/added, one just needs to remove/add to 'excel_headers'
        excel_headers = ['Patience', 'Hidden Nodes',
                         'Batch Size', 'Epochs', 'Overall Sens', 'Overall Spec']
        self.CATEGORY_INDEX = {excel_header: i for (excel_header, i) in zip(
            excel_headers, range(0, len(excel_headers)))}

        for category in self.CATEGORY_INDEX:
            self.data.write(0, self.CATEGORY_INDEX[category], category)

        # self.data.write(0, 0, 'Patience')
        # self.data.write(0, 1, 'Hidden Nodes')
        # self.data.write(0, 2, 'Overall Sens')
        # self.data.write(0, 3, 'Overall Spec')

        self.framework = Framework
        self.optimizer = Optimizer
        self.activation = Activation
        self.loss = Loss

        self.num_pcs = PrincipalComponents

        # self.batch = 64 #change to 64 for 1500 data set
        self.batch_range = utils.to_range(BatchSize)

        # self.pmin = 20
        # self.pmax = 50
        # self.pstep = 5
        self.patience_range = utils.to_range(Patience)

        self.epochs_range = utils.to_range(Epochs)

        # self.hiddenmin = 80
        # self.hiddenmax = 180
        # self.hiddenstep = 10
        self.hidden_range = utils.to_range(HiddenNodes)

        self.runs = Runs

        self.class_number = ClassNumber

        self.dataset = pd.read_excel(path)

        print(self.patience_range)

    # ----------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------
    def run(self):
        print("starting")

        self.dataset.head()

        x = self.dataset.iloc[:, -self.num_pcs:].values
        y = self.dataset.iloc[:, 1].values

        # %%need to one hot encode the categories
        enc = sk.OneHotEncoder(sparse=False)

        y = y.reshape(-1, 1)
        y = enc.fit_transform(y)

        # %%Split the data directly into training and testing

        from sklearn.model_selection import train_test_split

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,
                                                            shuffle=True, stratify=y)

        # %% Building the ANN

        if self.class_number == 3:
            i = 1
            for patience in self.patience_range:

                self.data.write(i, self.CATEGORY_INDEX['Patience'], patience)

                for hidden_nodes in self.hidden_range:

                    self.data.write(
                        i, self.CATEGORY_INDEX['Hidden Nodes'], hidden_nodes)

                    for batch_size in self.batch_range:

                        self.data.write(
                            i, self.CATEGORY_INDEX['Batch Size'], batch_size)

                        for epochs in self.epochs_range:

                            self.data.write(
                                i, self.CATEGORY_INDEX['Epochs'], epochs)

                            overallsens1 = 0
                            overallsens2 = 0
                            overallsens3 = 0
                            # overallsens4 = 0

                            overallspec1 = 0
                            overallspec2 = 0
                            overallspec3 = 0
                            # overallspec4 = 0

                            for c in range(0, self.runs):

                                model = Sequential()

                                model.add(
                                    Dense(hidden_nodes, input_dim=self.num_pcs, activation=self.activation))
                                model.add(
                                    Dense(self.class_number, activation='softmax'))

                                model.compile(
                                    loss=self.loss, optimizer=self.optimizer, metrics=['accuracy'])

                                earlyStopLoss = callbacks.EarlyStopping(monitor="loss",
                                                                        mode="min", patience=patience,
                                                                        restore_best_weights=True)

                                model.fit(x_train, y_train, epochs=epochs,
                                          batch_size=batch_size, callbacks=[earlyStopLoss])

                                # Make predictions on the test data

                                y_pred = model.predict(x_test)

                                # test
                                # probs = pd.DataFrame(y_pred)
                                # test

                                y_predVals = np.argmax(y_pred, axis=1)
                                y_testVals = np.argmax(y_test, axis=1)

                                results = confusion_matrix(
                                    y_predVals, y_testVals)

                                # sens and spec for each class for each of specified number of runs, for 3 class
                                sens1 = results[0][0] / \
                                    (results[0][0] + results[1]
                                     [0] + results[2][0])
                                sens2 = results[1][1] / \
                                    (results[0][1] + results[1]
                                     [1] + results[2][1])
                                sens3 = results[2][2] / \
                                    (results[0][2] + results[1]
                                     [2] + results[2][2])

                                spec1 = (results[1][1] + results[1][2] + results[2][1] + results[2][2]) / (
                                    results[0][1] + results[0][2] + results[1][1] + results[1][2] + results[2][1] + results[2][2])
                                spec2 = (results[0][0] + results[2][0] + results[0][2] + results[2][2]) / (
                                    results[0][0] + results[1][0] + results[2][0] + results[0][2] + results[1][2] + results[2][2])
                                spec3 = (results[0][0] + results[0][1] + results[1][0] + results[1][1]) / (
                                    results[0][0] + results[0][1] + results[1][0] + results[1][1] + results[2][0] + results[2][1])

                                overallsens1 += sens1
                                overallsens2 += sens2
                                overallsens3 += sens3
                                # overallsens4 += sens4

                                overallspec1 += spec1
                                overallspec2 += spec2
                                overallspec3 += spec3
                                # overallspec4 += spec4

                            # sens and spec for each class averaged over specified number of runs
                            overallsens1 /= self.runs
                            overallsens2 /= self.runs
                            overallsens3 /= self.runs
                            # overallsens4 /= runs

                            overallspec1 /= self.runs
                            overallspec2 /= self.runs
                            overallspec3 /= self.runs
                            # overallspec4 /= runs

                            # sens and spec averaged over all classes over specified number of runs
                            # + overallsens4
                            averagesens = (
                                overallsens1 + overallsens2 + overallsens3) / 3
                            # + overallsens4
                            averagespec = (
                                overallspec1 + overallspec2 + overallspec3) / 3

                            self.data.write(
                                i, self.CATEGORY_INDEX['Overall Sens'], averagesens)
                            self.data.write(
                                i, self.CATEGORY_INDEX['Overall Spec'], averagespec)

                            i += 1
        elif self.class_number == 4:
            i = 1
            for patience in self.patience_range:

                self.data.write(i, self.CATEGORY_INDEX['Patience'], patience)

                for hidden_nodes in self.hidden_range:

                    self.data.write(
                        i, self.CATEGORY_INDEX['Hidden Nodes'], hidden_nodes)

                    for batch_size in self.batch_range:

                        self.data.write(
                            i, self.CATEGORY_INDEX['Batch Size'], batch_size)

                        for epochs in self.epochs_range:

                            self.data.write(
                                i, self.CATEGORY_INDEX['Epochs'], epochs)

                            overallsens1 = 0
                            overallsens2 = 0
                            overallsens3 = 0
                            overallsens4 = 0

                            overallspec1 = 0
                            overallspec2 = 0
                            overallspec3 = 0
                            overallspec4 = 0

                            for c in range(0, self.runs):

                                model = Sequential()

                                model.add(
                                    Dense(hidden_nodes, input_dim=self.num_pcs, activation=self.activation))
                                model.add(
                                    Dense(self.class_number, activation='softmax'))

                                model.compile(
                                    loss=self.loss, optimizer=self.optimizer, metrics=['accuracy'])

                                earlyStopLoss = callbacks.EarlyStopping(monitor="loss",
                                                                        mode="min", patience=patience,
                                                                        restore_best_weights=True)

                                model.fit(x_train, y_train, epochs=epochs,
                                          batch_size=batch_size, callbacks=[earlyStopLoss])

                                # Make predictions on the test data

                                y_pred = model.predict(x_test)

                                y_predVals = np.argmax(y_pred, axis=1)
                                y_testVals = np.argmax(y_test, axis=1)

                                results = confusion_matrix(
                                    y_predVals, y_testVals)

                                # sens and spec for each class for each of specified number of runs, for 3 class
                                # sens1 = results[0][0] / (results[0][0] + results[1][0] + results[2][0])
                                # sens2 = results[1][1] / (results[0][1] + results[1][1] + results[2][1])
                                # sens3 = results[2][2] / (results[0][2] + results[1][2] + results[2][2])

                                # spec1 = (results[1][1] + results[1][2] + results[2][1] + results[2][2]) / (results[0][1] + results[0][2] + results[1][1] + results[1][2] + results[2][1] + results[2][2])
                                # spec2 = (results[0][0] + results[2][0] + results[0][2] + results[2][2]) / (results[0][0] + results[1][0] + results[2][0] + results[0][2] + results[1][2] + results[2][2])
                                # spec3 = (results[0][0] + results[0][1] + results[1][0] + results[1][1]) / (results[0][0] + results[0][1] + results[1][0] + results[1][1] + results[2][0] + results[2][1])

                                # for 4 class:
                                sens1 = results[0][0] / (
                                    results[0][0] + results[1][0] + results[2][0] + results[3][0])
                                sens2 = results[1][1] / (
                                    results[0][1] + results[1][1] + results[2][1] + results[3][1])
                                sens3 = results[2][2] / (
                                    results[0][2] + results[1][2] + results[2][2] + results[3][2])
                                sens4 = results[3][3] / (
                                    results[0][3] + results[1][3] + results[2][3] + results[3][3])

                                spec1 = (results[1][1] + results[1][2] + results[1][3] + results[2][1] + results[2][2] + results[2][3] + results[3][1] + results[3][2] + results[3][3]) / (
                                    results[0][1] + results[0][2] + results[0][3] + results[1][1] + results[1][2] + results[1][3] + results[2][1] + results[2][2] + results[2][3] + results[3][1] + results[3][2] + results[3][3])
                                spec2 = (results[0][0] + results[2][0] + results[3][0] + results[0][2] + results[0][3] + results[2][2] + results[2][3] + results[3][2] + results[3][3]) / (
                                    results[0][0] + results[1][0] + results[2][0] + results[3][0] + results[0][2] + results[0][3] + results[1][2] + results[1][3] + results[2][2] + results[2][3] + results[3][2] + results[3][3])
                                spec3 = (results[0][0] + results[0][1] + results[1][0] + results[1][1] + results[3][0] + results[3][1] + results[0][3] + results[1][3] + results[3][3]) / (
                                    results[0][0] + results[0][1] + results[1][0] + results[1][1] + results[2][0] + results[2][1] + results[3][0] + results[3][1] + results[0][3] + results[1][3] + results[2][3] + results[3][3])
                                spec4 = (results[0][0] + results[0][1] + results[0][2] + results[1][0] + results[1][1] + results[1][2] + results[2][0] + results[2][1] + results[2][2]) / (
                                    results[0][0] + results[0][1] + results[0][2] + results[1][0] + results[1][1] + results[1][2] + results[2][0] + results[2][1] + results[2][2] + results[3][0] + results[3][1] + results[3][2])

                                overallsens1 += sens1
                                overallsens2 += sens2
                                overallsens3 += sens3
                                overallsens4 += sens4

                                overallspec1 += spec1
                                overallspec2 += spec2
                                overallspec3 += spec3
                                overallspec4 += spec4

                            # sens and spec for each class averaged over specified number of runs
                            overallsens1 /= self.runs
                            overallsens2 /= self.runs
                            overallsens3 /= self.runs
                            overallsens4 /= self.runs

                            overallspec1 /= self.runs
                            overallspec2 /= self.runs
                            overallspec3 /= self.runs
                            overallspec4 /= self.runs

                            # sens and spec averaged over all classes over specified number of runs
                            # + overallsens4
                            averagesens = (
                                overallsens1 + overallsens2 + overallsens3 + overallsens4) / 4
                            # + overallsens4
                            averagespec = (
                                overallspec1 + overallspec2 + overallspec3 + overallsens4) / 4

                            self.data.write(
                                i, self.CATEGORY_INDEX['Overall Sens'], averagesens)
                            self.data.write(
                                i, self.CATEGORY_INDEX['Overall Spec'], averagespec)

                            i += 1
        else:
            print("Invalid class number")
            return None

            # print(confusion_matrix(y_predVals, y_testVals))

        self.workbook.close()

        return self.output_filename

    # ----------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------

    def checkInput(self, filename: str) -> str:

        if not os.path.exists(filename):
            return 'File not found: ' + os.getcwd()

        if not filename.lower().endswith('.xlsx'):
            return 'File not .xlsx format'

        return ''


if __name__ == '__main__':
    ann_instance = ANN('MasterBacteria_fullspectrumSCORES.xlsx')
    ann_instance.run()
