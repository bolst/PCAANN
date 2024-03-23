import os
from flask import Flask, request
from pca import PCA, RAW_DATA_PATH, SCORES_DIR
from ann import ANN, RESULTS_DIR

app = Flask(__name__)

pca_instance = None
ann_instance = None

raw_data_filepath = ''
pca_scores_filepath = ''
ann_results_filepath = ''


def success():
    print('done!')
    return 'success'


@app.route('/raw-data/files')
def raw_data_files():
    return os.listdir(RAW_DATA_PATH)


@app.route('/scores/files')
def scores_files():
    return os.listdir(SCORES_DIR)


@app.route('/results/files')
def results_files():
    return os.listdir(RESULTS_DIR)


@app.route('/loadfile', methods=['POST'])
def loadfile():
    global raw_data_filepath

    received_data = request.json
    print(received_data)
    filename = received_data['rawDataFilename']

    raw_data_filepath = RAW_DATA_PATH + '/' + filename

    if not os.path.isfile(raw_data_filepath):
        return 'error: cannot find file'

    print('Loaded!')

    return success()


@app.route('/runpca', methods=['POST'])
def runpca():
    received_data = request.json

    try:
        global pca_instance, raw_data_filepath, pca_scores_filepath
        filepath = raw_data_filepath
        components = received_data['components']
        full_spectrum = received_data['fullSpectrum']

        pca_instance = PCA(filepath, components=components,
                           full_spectrum=full_spectrum)
        pca_scores_filepath = pca_instance.run()
    except Exception as exc:
        # TODO: yell
        print(exc)
        return 'error'

    return success()


@app.route('/loadpca', methods=['POST'])
def load_pca_scores():
    global pca_scores_filepath

    received_data = request.json
    print(received_data)
    filename = received_data['pcaScoresFilename']

    pca_scores_filepath = SCORES_DIR + '/' + filename

    if not os.path.isfile(pca_scores_filepath):
        return 'error: cannot find file'

    print('Loaded!')

    return success()


@app.route('/runann', methods=['POST'])
def runann():
    received_data = request.json
    try:
        global ann_instance, pca_scores_filepath, ann_results_filepath
        received_data = parse_ranges(received_data)
        framework = received_data['framework']
        optimizer = received_data['optimizer']
        activation = received_data['activation']
        loss = received_data['loss']
        epochs = received_data['epochs']
        batchSize = received_data['batchSize']
        patience = received_data['patience']
        hiddenNodes = received_data['hiddenNodes']
        runs = received_data['runs']
        classNumber = received_data['classNumber']
        principalComponents = received_data['components']
        ann_instance = ANN(pca_scores_filepath,
                           Framework=framework,
                           Optimizer=optimizer,
                           Activation=activation,
                           Loss=loss,
                           Epochs=epochs,
                           BatchSize=batchSize,
                           Patience=patience,
                           HiddenNodes=hiddenNodes,
                           Runs=runs,
                           ClassNumber=classNumber,
                           PrincipalComponents=principalComponents)

        ann_results_filepath = ann_instance.run()
    except Exception as exc:
        # TODO: yell
        print('oh man\n\n\n')
        print(exc)
        return 'error'

    return success()


@app.route('/viewresults')
def view_results():
    # TODO: verify this works
    if len(ann_results_filepath) == 0:
        return 'error: not sure what file is trying to be opened'
    try:
        os.system(f'start EXCEL.EXE "{ann_results_filepath}"')
    except Exception as exc:
        print(exc)
        return 'error'
    return success()


def parse_ranges(data: dict) -> dict:
    for key in data:
        print(data)
        print('\n\n', key)
        value = data[key]
        print(value)

        if value == None:
            continue
        # if the value is an encoded range
        try:
            if type(value) is str and ' ' in value:
                val, start, stop, step = value.split(' ')
                start = int(start)
                stop = int(stop)
                step = int(step)
                data[key] = range(start, stop, step)
            elif type(value) is str and value.isnumeric():
                data[key] = int(value)
        except:
            continue

    return data


if __name__ == "__main__":
    app.run(port=8000, debug=True)
