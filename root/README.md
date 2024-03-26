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
2. This data (`*.xlsx`) is copied into the `PCA-ANN-code/RAW-DATA` folder
3. The app is started
4. The data is selected (`Load Raw Data`)
5. The PCA parameters are set
6. The PCA code is run (`Run PCA`)
7. The ANN parameters are set
8. The ANN code is run (`Run ANN`)
9. Results are outputted (`View Results`)

If one already has a set of PCA scores, one can skip steps 1-6 and use the `Load PCA Scores` button and continue with the rest of the steps.

More detail is written in the SOP.


# Quick Start
1. Start Docker
2. Clone this repo 
    ```
    git clone https://github.com/bolst/PCAANN
    ```

3. Move into the directory 
    ```
    cd PCAANN
    ```

4. Build the environment 
    ```
    .\build.ps1
    ```

5. Move any available raw data into `PCA-ANN-code/RAW-DATA`

6. Run with 
    ```
    .\run.ps1
    ```