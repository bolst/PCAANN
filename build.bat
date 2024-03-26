@Echo off

docker build -t pca_ann_image . && ^
python3.10 -m venv PCA-ANN-code\pcaann

call PCA-ANN-code\pcaann\Scripts\activate && ^
python -m pip install --upgrade pip && ^
python -m pip install -r PCA-ANN-code\requirements.txt && ^
deactivate