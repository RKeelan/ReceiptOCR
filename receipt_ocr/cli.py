import click
import paddle;


@click.command()
@click.version_option()
def cli():
    "Receipt OCR"
    click.echo("Receipt OCR")
    click.echo(paddle.utils.run_check())
