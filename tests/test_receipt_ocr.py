from click.testing import CliRunner
from paddle import utils
from receipt_ocr.cli import cli


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")


def test_paddle_installation():
    """Test that PaddlePaddle is properly installed and can run its self-check."""
    utils.run_check()