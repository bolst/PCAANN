import os
from subprocess import call
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA as sklearnPCA
import xlsxwriter

RAW_DATA_PATH = 'PCA-ANN-code/RAW-DATA'
SCORES_DIR = 'PCA-ANN-code/SCORES'


class PCA:
    isRunnable = False

    def __init__(self, path, components=10, full_spectrum=True):
        # verify input data
        m = self.checkInput(path)
        if len(m) != 0:
            raise ValueError(m)
        self.input_filename, self.input_file_extension = os.path.splitext(path)
        # convert xlsx to csv (and store conversion time)
        st_cpu = time.process_time()
        st_wall = time.time()
        csv_path = self.xlsxToCSV(path)
        self.conversion_CPUTime = time.process_time() - st_cpu
        self.conversion_WallTime = time.time() - st_wall
        if len(csv_path) == 0:
            raise ValueError('Unable to convert to CSV')

        # store filename and data
        self.csv_filename = csv_path
        self.df = pd.read_csv(
            self.csv_filename, low_memory=False)  # enter file name

        # delete csv file since data is in self.df
        try:
            os.remove(self.csv_filename)
        except:
            print(f'Unable to remove {self.filename}')

        # set parameters
        self.num_components = components
        self.is_full_spectrum = full_spectrum
        self.output_filename = SCORES_DIR + '/' + \
            self.input_filename.split('/')[-1] + '-SCORES.xlsx'

        self.isRunnable = True

    # ----------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------

    def run(self):

        if not self.isRunnable:
            print('No instance of PCAFullSpectrum found. Construct first?')
            return

        st_wall = time.time()
        st_cpu = time.process_time()

        big_array = self.df.to_numpy()  # dtype='float64'
        array_transposed = np.transpose(big_array)
        dataf = pd.DataFrame(array_transposed[1:], columns=array_transposed[0])
        data_array = array_transposed[1:, 1:]

        samplenames = self.df.columns

        # lines = dataf.columns[35:42523] #only these columns needed bc everything after 621.82 nm not useful (to change back to full spectrum, dataf.columns[:53434])
        if (self.is_full_spectrum):
            # Number of rows in input data
            NUM_ROWS = len(self.df) - 1  # 53242 #53434
            lines = dataf.columns[:NUM_ROWS]
        else:
            # TODO: make dynamic
            lines = dataf.columns[35:42523]

        # x = dataf.loc[:, lines].values
        # x = dataf.truncate(before=34)

        y = dataf.loc[:, ['Class']].values

        x_mc = dataf.loc[:, lines].values  # dataframe to be meancentered
        # x_mc = dataf.astype(float)

        # x_mc_new = x_mc.to_numpy(dtype='float64')
        # np.delete(x_mc, [0,34], axis = 1)

        # mean centering:
        # find average of each column for mean centering (array includes class average as well in first column position)
        average = dataf.mean(axis=0).values
        # stdev = dataf.std(axis=0).values
        average = np.mean(x_mc, axis=0, dtype='float64')
        # stdev = np.std(x_mc, axis=0, dtype='float64')

        # TODO: what is this number from?
        rows = 42488

        # Number of columns in input data
        NUM_COLUMNS = len(self.df.columns) - 1  # 425 #1596
        for n in range(0, NUM_COLUMNS):
            for m in range(0, rows):
                try:
                    x_mc[n][m] = x_mc[n][m] - average[m]
                except:
                    print(n, m)
                    print(len(x_mc), len(x_mc[0]))
                    exit(0)
                # x_mc[n][m] = x_mc[n][m]*(1/stdev[m])

        # log preprocessing
        # for n in range (0, 1596):
            # for m in range(0, rows):
                # x_mc[n][m] = x_mc[n][m] + 1324
                # x_mc[n][m] = np.log(x_mc[n][m])

        pca = sklearnPCA(n_components=self.num_components)

        principalComponents = pca.fit_transform(
            x_mc)  # change variable in brackets
        principalDf = pd.DataFrame(data=principalComponents,
                                   columns=['principal component ' + str(i) for i in range(1, self.num_components + 1)])

        finalDf = pd.concat([principalDf, dataf[['Class']]], axis=1)
        # print(finalDf)

        print(pca.explained_variance_ratio_)  # output PC values

        # %% PCA Plots

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.set_xlabel('PC 1', fontsize=10)
        ax.set_ylabel('PC 2', fontsize=10)
        ax.set_zlabel('PC 3', fontsize=10)
        ax.set_title('3 component PCA', fontsize=20)
        Classes = [0, 1, 2, 3, 4]
        colors = ['r', 'g', 'b', 'm', 'c']
        for Class, color in zip(Classes, colors):
            indicesToKeep = finalDf['Class'] == Class
            # print(indicesToKeep)
            ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1'], finalDf.loc[indicesToKeep,
                       'principal component 2'], finalDf.loc[indicesToKeep, 'principal component 3'], c=color, s=50)
        ax.legend(Classes)
        ax.grid()

        # ax.view_init(10, 0) # use this to change the viewing angle of the 3d plot

        '''
        plt.figure()
        ax = plt.axes(projection='3d')
        plt.scatter(principalComponents[:,0], principalComponents[:,1], principalComponents[:,2])
        plt.show()
        '''

        # %%loadings = pd.DataFrame(pca.components_.T, columns=['PC1', 'PC2', 'PC3'], index=lines)#find loadings for each wavelength and corresponding PC

        # find loadings for each wavelength and corresponding PC
        loadings = pd.DataFrame(pca.components_.T, columns=[
                                'PC' + str(i) for i in range(1, self.num_components + 1)], index=lines)
        print("Loadings:")
        print(loadings)
        '''
        plt.figure()
        loadings["PC1"].plot(title = 'PC1 Loadings', fontsize = 6)
        plt.show()
        
        plt.figure()
        loadings["PC2"].plot(title = 'PC2 Loadings', fontsize = 6)
        plt.show()
        
        plt.figure()
        loadings["PC3"].plot(title = 'PC3 Loadings', fontsize = 6)
        plt.show()
        
        array = loadings.to_numpy()
        
        #output all loadings to excel sheet titled "Loadings" within the workbook
        
        loadingsdata = workbook.add_worksheet('Loadings')
        for i in range(0, 40653): 
            loadingsdata.write(i, 0, lines[i])
        for r in range(0, 40653):
            for c in range(0, 20):
                loadingsdata.write(r, c+1,abs(array[r][c]))
        '''
        # %% scores
        workbook = xlsxwriter.Workbook(self.output_filename)
        data = workbook.add_worksheet('All Data')

        samplenames = self.df.columns

        scores = []
        scores = pca.fit_transform(data_array)
        max_score = np.max(scores)

        # TODO: put this into documentation
        '''
        Need to determine the spans of columns that contains individual classes (ex: which columns have staphfive? staphten? etc)
        It seems that a standard naming convention for each column follows "date_class_samplenum" (ex: 111323_staphfive_01)
        This means that in order for this to work, the input data must follow this pattern
        It doesn't actually matter what the date and samplenum are - the code will just search for columns with the same 'class' name
        '''

        # for our case, we have staphfive 1-101 (100), staphten 102-211 (109), ecolifive 212-311 (99), ecoliten 312-426 (114)

        # for i in range(100):
        #    data.write(i + 1, 0, samplenames[i+1])
        #    data.write(i + 1, 1, 0)
        # for i in range(110):
        #    data.write(i + 101, 0, samplenames[i+101])
        #    data.write(i + 101, 1, 1)
        # for i in range(100):
        #    data.write(i + 211, 0, samplenames[i+211])
        #    data.write(i + 211, 1, 2)
        # for i in range(115):
        #    data.write(i + 311, 0, samplenames[i+311])
        #    data.write(i + 311, 1, 3)

        # Q: can the above 4 for loops be refactored? Yes:
        class_range_map = calc_class_indices(samplenames[1:])
        for i in range(NUM_COLUMNS):
            samplename = samplenames[i + 1]
            classname = parse_header(samplename)
            index = class_range_map[classname]

            data.write(i + 1, 0, samplename)
            data.write(i + 1, 1, index)

        # %%

        for i in range(1, self.num_components + 1):
            data.write(0, i+1, f'PC{i} Score')

        # print(data_array)
        # print(scores)

        for i in range(0, NUM_COLUMNS):
            for j in range(0, self.num_components):
                # scores[i][j] = scores[i][j] + max_score
                data.write(i+1, j+2, scores[i][j])
        workbook.close()

        et_wall = time.time()
        et_cpu = time.process_time()

        self.wall_time = et_wall - st_wall
        self.cpu_time = et_cpu - st_cpu
        print(f"Wall time: {self.wall_time + self.conversion_WallTime}")
        print(f"CPU time: {self.cpu_time + self.conversion_CPUTime}")

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

    def xlsxToCSV(self, path: str):
        filename, extension = os.path.splitext(path)
        csv_filename = self.uniquify(filename + '.csv')

        call(['cscript.exe', 'PCA-ANN-code/ExcelToCSV.vbs', path, csv_filename, '1'])

        if not os.path.exists(csv_filename):
            return ''

        return csv_filename

    def uniquify(self, path: str) -> str:
        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = filename + " (" + str(counter) + ")" + extension
            counter += 1

        return path

# assume every header is labelled as "date_class_samplenum" and return "class"
# sometimes label is "date_class#_samplenum", but whatever the # is should be ignored


def parse_header(header: str, ignore_numerical_suffix=False):
    retval = header.split('_')[1]

    # trim trailing numbers if there are any
    if ignore_numerical_suffix:
        while retval[-1].isnumeric():
            retval = retval[:-1]

    return retval

# function to parse list of column headers (which would contain class names)
# returns a map of each class name to an index


def calc_class_indices(headers: list) -> dict:

    tracked_classes = []
    retval = {}
    current_index = -1
    for header in headers:
        classname_nonum = parse_header(header, ignore_numerical_suffix=True)
        classname = parse_header(header)

        if classname_nonum not in tracked_classes:
            current_index += 1
            tracked_classes.append(classname_nonum)

        retval[classname] = current_index

    return retval


if __name__ == '__main__':
    fname = 'Nov 2023 Data for PCA Test.xlsx'
    pca_instance = PCA(fname)
    pca_instance.run()
