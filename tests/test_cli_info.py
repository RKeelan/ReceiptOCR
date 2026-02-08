import os
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from receipt_ocr.cli import cli


def test_info_command():
    """Test that the info command displays the correct directory information."""
    expected_user_dir = Path("/tmp/receipt-ocr-user")
    expected_receipts_dir = expected_user_dir / "Receipts"
    runner = CliRunner()

    with patch("receipt_ocr.cli.user_dir", return_value=expected_user_dir), \
         patch("receipt_ocr.cli.get_receipts_dir", return_value=expected_receipts_dir), \
         runner.isolated_filesystem():
        result = runner.invoke(cli, ["info"])

        assert result.exit_code == 0
        assert f"User directory: {expected_user_dir}" in result.output
        assert f"Receipts directory: {expected_receipts_dir}" in result.output


@pytest.mark.skipif(os.name != "nt", reason="Windows-specific test")
def test_info_command_windows_paths():
    """Test that the info command shows correct Windows paths."""
    test_appdata = "C:\\Users\\Test\\AppData\\Roaming"
    expected_user_dir = Path(test_appdata) / "ReceiptOCR"
    expected_receipts_dir = expected_user_dir / "Receipts"
    
    runner = CliRunner()
    
    # Patch environment and directory creation
    with patch.dict(os.environ, {"APPDATA": test_appdata}), \
         patch('pathlib.Path.mkdir'), \
         patch('receipt_ocr.cli.user_dir', return_value=expected_user_dir), \
         patch('receipt_ocr.cli.get_receipts_dir', return_value=expected_receipts_dir):
        
        result = runner.invoke(cli, ["info"])
        
        assert result.exit_code == 0
        assert f"User directory: {expected_user_dir}" in result.output
        assert f"Receipts directory: {expected_receipts_dir}" in result.output


def test_info_command_with_env_var():
    """Test that the info command respects RECEIPT_OCR_USER_PATH environment variable."""
    test_path = "/custom/test/path"
    expected_user_dir = Path(test_path)
    expected_receipts_dir = expected_user_dir / "Receipts"
    
    runner = CliRunner()
    
    # Patch environment and directory creation
    with patch.dict(os.environ, {"RECEIPT_OCR_USER_PATH": test_path}), \
         patch('pathlib.Path.mkdir'), \
         patch('receipt_ocr.cli.user_dir', return_value=expected_user_dir), \
         patch('receipt_ocr.cli.get_receipts_dir', return_value=expected_receipts_dir):
        
        result = runner.invoke(cli, ["info"])
        
        assert result.exit_code == 0
        assert f"User directory: {expected_user_dir}" in result.output
        assert f"Receipts directory: {expected_receipts_dir}" in result.output 
