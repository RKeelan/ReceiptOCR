import os
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

import pytest
from click.testing import CliRunner

from receipt_ocr.cli import cli, get_receipts_dir


def test_run_command_default_dir():
    """Test that the run command uses the default directory when no directory is specified."""
    runner = CliRunner()
    default_dir = get_receipts_dir()
    
    with patch('receipt_ocr.cli.get_receipts_dir') as mock_get_dir, \
         patch('pathlib.Path.iterdir') as mock_iterdir, \
         patch('pathlib.Path.is_file', return_value=True), \
         patch('receipt_ocr.cli.PaddleOCR') as mock_ocr_class:
        
        # Setup mock OCR
        mock_ocr = mock_ocr_class.return_value
        mock_ocr.ocr.return_value = [[]]
        
        # Setup mock to return an empty list of files
        mock_get_dir.return_value = default_dir
        mock_iterdir.return_value = []
        
        result = runner.invoke(cli, ["run"])
        
        assert result.exit_code == 0
        assert f"Processing images in {default_dir}" in result.output
        mock_ocr_class.assert_called_once_with(use_angle_cls=True, lang='en')


def test_run_command_custom_dir():
    """Test that the run command uses a custom directory when specified."""
    runner = CliRunner()
    custom_dir = Path("/custom/test/path")
    
    with patch('pathlib.Path.iterdir') as mock_iterdir, \
         patch('pathlib.Path.is_file', return_value=True), \
         patch('receipt_ocr.cli.PaddleOCR') as mock_ocr_class:
        
        # Setup mock OCR
        mock_ocr = mock_ocr_class.return_value
        mock_ocr.ocr.return_value = [[]]
        
        # Setup mock to return an empty list of files
        mock_iterdir.return_value = []
        
        result = runner.invoke(cli, ["run", "--image-dir", str(custom_dir)])
        
        assert result.exit_code == 0
        assert f"Processing images in {custom_dir}" in result.output
        mock_ocr_class.assert_called_once_with(use_angle_cls=True, lang='en')


def test_run_command_processes_files():
    """Test that the run command correctly processes files and skips directories and non-image files."""
    runner = CliRunner()
    test_dir = Path("/test/dir")
    
    # Create mock files and directories
    image_file = MagicMock(spec=Path)
    image_file.is_file.return_value = True
    image_file.name = "receipt1.jpg"
    image_file.__str__.return_value = str(test_dir / "receipt1.jpg")
    
    non_image_file = MagicMock(spec=Path)
    non_image_file.is_file.return_value = True
    non_image_file.name = "document.txt"
    non_image_file.__str__.return_value = str(test_dir / "document.txt")
    
    directory = MagicMock(spec=Path)
    directory.is_file.return_value = False
    directory.name = "subdirectory"
    
    with patch('pathlib.Path.iterdir') as mock_iterdir, \
         patch('receipt_ocr.cli.PaddleOCR') as mock_ocr_class:
        
        # Setup mock OCR
        mock_ocr = mock_ocr_class.return_value
        mock_ocr.ocr.return_value = [[]]
        
        # Setup mock to return our test files and directory
        mock_iterdir.return_value = [image_file, non_image_file, directory]
        
        result = runner.invoke(cli, ["run", "--image-dir", str(test_dir)])
        
        assert result.exit_code == 0
        assert f"Processing images in {test_dir}" in result.output
        assert "Processing receipt1.jpg" in result.output
        # Should not process non-image files
        assert "Processing document.txt" not in result.output
        # Should not process directories
        assert "Processing subdirectory" not in result.output
        
        # OCR should only be called for the image file
        mock_ocr.ocr.assert_called_once_with(str(test_dir / "receipt1.jpg"), cls=True)


def test_run_command_with_empty_dir():
    """Test that the run command handles an empty directory gracefully."""
    runner = CliRunner()
    empty_dir = Path("/empty/dir")
    
    with patch('pathlib.Path.iterdir') as mock_iterdir, \
         patch('receipt_ocr.cli.PaddleOCR') as mock_ocr_class:
        
        # Setup mock OCR
        mock_ocr = mock_ocr_class.return_value
        
        # Setup mock to return an empty list of files
        mock_iterdir.return_value = []
        
        result = runner.invoke(cli, ["run", "--image-dir", str(empty_dir)])
        
        assert result.exit_code == 0
        assert f"Processing images in {empty_dir}" in result.output
        # No processing messages should appear since there are no files
        
        # OCR should not be called at all
        mock_ocr.ocr.assert_not_called()


def test_ocr_text_extraction():
    """Test that OCR text extraction works correctly."""
    runner = CliRunner()
    test_dir = Path("/test/dir")
    
    # Create mock file
    image_file = MagicMock(spec=Path)
    image_file.is_file.return_value = True
    image_file.name = "receipt1.jpg"
    image_file.__str__.return_value = str(test_dir / "receipt1.jpg")
    
    # Sample OCR results with text and confidence scores
    ocr_results = [
        [
            [
                [[1, 2], [3, 4], [5, 6], [7, 8]],  # Bounding box (unused in the current implementation)
                ["Total: $15.99", 0.95]  # Text and confidence
            ],
            [
                [[10, 20], [30, 40], [50, 60], [70, 80]],
                ["Date: 2023-06-15", 0.90]
            ]
        ]
    ]
    
    with patch('pathlib.Path.iterdir') as mock_iterdir, \
         patch('receipt_ocr.cli.PaddleOCR') as mock_ocr_class:
        
        # Setup mock OCR
        mock_ocr = mock_ocr_class.return_value
        mock_ocr.ocr.return_value = ocr_results
        
        # Setup mock to return our test file
        mock_iterdir.return_value = [image_file]
        
        result = runner.invoke(cli, ["run", "--image-dir", str(test_dir)])
        
        assert result.exit_code == 0
        assert "Processing receipt1.jpg" in result.output
        assert "Extracted text from receipt1.jpg:" in result.output
        assert "Total: $15.99 (Confidence: 0.95)" in result.output
        assert "Date: 2023-06-15 (Confidence: 0.90)" in result.output 