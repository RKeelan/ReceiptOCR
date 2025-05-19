import os
from pathlib import Path


def user_dir() -> Path:
    """
    Returns:
        Path: The directory path for storing user data.
    """
    if os.environ.get("RECEIPT_OCR_USER_PATH"):
        path = os.environ.get("RECEIPT_OCR_USER_PATH")
    else:
        # Handle different platforms
        if os.name == "nt":  # Windows
            app_data = os.environ.get("APPDATA") or str(
                Path.home() / "AppData" / "Roaming"
            )
            path = Path(app_data) / "ReceiptOCR"
        else:
            # Add MacOS and Linux support if required
            raise NotImplementedError("MacOS and Linux support is not implemented")

    # Ensure the directory exists
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_receipts_dir() -> Path:
    """
    Get the default directory for storing receipt images.

    Returns:
        Path: The path to the images directory.
    """
    receipts_dir = user_dir() / "Receipts"
    receipts_dir.mkdir(parents=True, exist_ok=True)
    return receipts_dir