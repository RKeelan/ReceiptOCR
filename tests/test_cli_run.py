from pathlib import Path
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from receipt_ocr.cli import cli


def test_run_command_custom_dir_uses_pipeline_defaults(tmp_path: Path):
    runner = CliRunner()

    with patch("receipt_ocr.cli.PPStructureV3") as mock_pipeline_cls:
        mock_pipeline = mock_pipeline_cls.return_value
        mock_pipeline.predict.return_value = []

        result = runner.invoke(cli, ["run", "--image-dir", str(tmp_path)])

        assert result.exit_code == 0
        assert f"Processing images in {tmp_path}" in result.output
        mock_pipeline_cls.assert_called_once_with(
            device="gpu:0",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            use_table_recognition=True,
        )


def test_run_command_processes_only_supported_image_extensions(tmp_path: Path):
    runner = CliRunner()

    image = tmp_path / "receipt1.jpg"
    image.write_text("fake image bytes")
    ignored = tmp_path / "notes.txt"
    ignored.write_text("not an image")

    fake_result = MagicMock()

    with patch("receipt_ocr.cli.PPStructureV3") as mock_pipeline_cls:
        mock_pipeline = mock_pipeline_cls.return_value
        mock_pipeline.predict.return_value = [fake_result]

        result = runner.invoke(cli, ["run", "--image-dir", str(tmp_path), "--device", "cpu"])

        assert result.exit_code == 0
        mock_pipeline.predict.assert_called_once_with(input=str(image))
        fake_result.save_to_json.assert_called_once_with(save_path="receipt1.json")
        fake_result.save_to_markdown.assert_called_once_with(save_path="receipt1.md")
