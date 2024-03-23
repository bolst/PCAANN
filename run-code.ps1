$ErrorActionPreference = "Stop"

python3.10 -m venv .\PCA-ANN-code\pcaann

.\PCA-ANN-code\pcaann\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r .\PCA-ANN-code\requirements.txt

python .\PCA-ANN-code\app.py