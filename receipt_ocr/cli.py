import click
from click_default_group import DefaultGroup
import math
import pathlib
import re

from paddleocr import PPStructureV3

from receipt_ocr.utils import user_dir, get_receipts_dir


@click.group(
    cls=DefaultGroup,
    default="run",
    default_if_no_args=True,
)
@click.version_option()
def cli():
    "Receipt OCR"
    pass


@cli.command(name="run")
@click.option(
    "--image-dir", 
    type=click.Path(file_okay=False, dir_okay=True, path_type=pathlib.Path),
    help="Directory containing receipt images to process",
    default=lambda: get_receipts_dir()
)
@click.option("--device", default="gpu:0", help="cpu | gpu:0")
@click.option("--lang", default="en", help="Language (en for English receipts)")
def run_command(image_dir: pathlib.Path, device: str, lang: str):
    "Process images in the specified directory"
    click.echo(f"Processing images in {image_dir}")
    
    pipeline = PPStructureV3(
        device=device,
        use_doc_orientation_classify=False,  # receipts are rarely upside-down
        use_doc_unwarping=False,             # set True if photos, not scans
        use_textline_orientation=False,
        use_table_recognition=True,
    )

    for img_path in sorted(image_dir.iterdir()):
        if img_path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"}:
            continue

        click.echo(f"→ {img_path.name}", err=True)
        output = pipeline.predict(input=str(img_path))

        for result in output:
            result.print() 
            result.save_to_json(save_path=f"{img_path.stem}.json") 
            result.save_to_markdown(save_path=f"{img_path.stem}.md")


@cli.command(name="info")
def info_command():
    "Display information about directories used by the application"
    user_directory = user_dir()
    receipts_directory = get_receipts_dir()
    
    click.echo(f"User directory: {user_directory}")
    click.echo(f"Receipts directory: {receipts_directory}")

