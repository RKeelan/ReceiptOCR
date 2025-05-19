import click


@click.command()
@click.version_option()
def cli():
    "Receipt OCR"
    click.echo("Receipt OCR")
