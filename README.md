# ReceiptOCR

[![Changelog](https://img.shields.io/github/v/release/RKeelan/ReceiptOCR?include_prereleases&label=changelog)](https://github.com/RKeelan/ReceiptOCR/releases)
[![Tests](https://github.com/RKeelan/ReceiptOCR/actions/workflows/test.yml/badge.svg)](https://github.com/RKeelan/ReceiptOCR/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/RKeelan/ReceiptOCR/blob/master/LICENSE)

Receipt OCR

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

Install dependencies (including test):
```powershell
uv pip install -e '.[test]'
uv pip install --upgrade pip wheel
uv pip install --upgrade setuptools
uv pip install paddlepaddle-gpu==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
```

Verify paddle installation:
```
python -c "import paddle; print(paddle.utils.run_check())"
```

Run the tests:
```powershell
python -m pytest
```

Run the app:
```powershell
receipt-ocr --version
```
