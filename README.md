# PCA ANN for Bacterial Spectrum Analysis

# Requirements
- Windows
- Python 3.10 ([Download](https://www.python.org/downloads/release/python-31014/))
- Docker ([Download](https://www.docker.com/products/docker-desktop/))

Also make sure Python 3.10 has an alias to `python3.10`

# About
This project was built to be a friendly interface to a Principal Component Analysis (PCA) and Artificial Neural Network (ANN) code used for analyzing bacterial spectra.

In Dr. Rehse's lab, the PCA and (more so) ANN code have parameters that are varied with the intent of measuring how they affect the accuracy in the predictions. This app allows for a visualization of how these parameters can be varied, along with a user-friendly flow chart for how a typical analysis is done on the spectral data.

In case the UI is not clear enough, a typical use case of the app would be as follows:

1. One obtains the pre-formatted spectral data that is outputted from a laser shooting
2. `run.bat` is executed
3. Any desired `*.xlsx` data is selected from the prompt
4. The app is started
5. The data is selected (`Load Raw Data`)
6. The PCA parameters are set
7. The PCA code is run (`Run PCA`)
8. The ANN parameters are set
9. The ANN code is run (`Run ANN`)
10. Results are outputted (`View Results`)

If one already has a set of PCA scores, one can skip steps 1-6 and use the `Load PCA Scores` button and continue with the rest of the steps.

More detail is written in the SOP & documentation.


# Quick Start
1. Start Docker
2. Clone this repo 
    ```
    git clone https://github.com/bolst/PCAANN
    ```

3. Move into the directory (i.e., on the same level as `root`)
    ```
    cd PCAANN
    ```

4. Start the helper
    ```
    run
    ```

5. Select any raw data to be used

6. Start the app from the helper