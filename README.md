# ReceiptOCR

[![Tests](https://github.com/RKeelan/ReceiptOCR/actions/workflows/test.yml/badge.svg)](https://github.com/RKeelan/ReceiptOCR/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/RKeelan/ReceiptOCR/blob/master/LICENSE)

This project is for prototyping optical character recognition of receipts (currently using Paddle OCR).

## Setup

Checkout the code:
```powershell
git clone https://github.com/RKeelan/ReceiptOCR.git
cd ReceiptOCR
```

Create a new virtual environment:
```powershell
uv venv && .venv\Scripts\activate.ps1
```

This part of the setup instructions should be taken with a grain of salt, becuase I wrote them after muddling through the environment setup, then never tested them (because that would require un-installing then re-installing all this stuff). It is also quite likely that they will become obselete quickly.
Install dependencies (including test):
```powershell
uv pip install -e '.[test]'
uv pip install --upgrade pip wheel
uv pip install --upgrade setuptools
uv pip install paddlepaddle-gpu -i https://www.paddlepaddle.org.cn/packages/stable/cu126/

# Setup Nvida CUDA dependency
nvidia-smi # Make sure Nvidia GPU and driver is detected

# Install CUDA 11.7
winget install --id Nvidia.CUDA --version 11.7 -e --accept-package-agreements --accept-source-agreements
Push-Path 'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\bin'

# Install cuDNN for CUDA 11.x from https://developer.nvidia.com/rdp/cudnn-archive
# In Adminstrator window
cd ~\Downloads
Expand-Archive cudnn-windows-x86_64-8.9.7.29_cuda11-archive.zip -DestinationPath cudnn
$cuda = 'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7'
cp cudnn\cudnn-windows-x86_64-8.9.7.29_cuda11-archive\bin\cudnn*.dll "$cuda\bin\"
cp cudnn\cudnn-windows-x86_64-8.9.7.29_cuda11-archive\include\cudnn*.h "$cuda\include\"
cp cudnn\cudnn-windows-x86_64-8.9.7.29_cuda11-archive\lib\x64\cudnn*.lib "$cuda\lib\x64\"
```

Verify paddle installation:
```
python -c "import paddle; print(paddle.utils.run_check())"
```

Run the tests:
```powershell
python -m pytest
```

Show Receipts directory
```powershell
ocr info
```

Run OCR on all images in the receipts directory:
```powershell
ocr run
```
