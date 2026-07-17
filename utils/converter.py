"""
converter.py
----------------------------------------
Converts supported image formats into PDF.

Supported:
    - PDF (returns original path)
    - JPG
    - JPEG
    - PNG
    - BMP
    - TIFF
    - GIF

Author: PragyanAI
"""

from pathlib import Path
from PIL import Image
import os


SUPPORTED_IMAGES = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tiff",
    ".tif",
    ".gif",
)


def ensure_directory(directory):
    """
    Create directory if it doesn't exist.
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


def image_to_pdf(image_path, output_folder):
    """
    Convert image to PDF.

    Parameters
    ----------
    image_path : str
        Input image

    output_folder : str
        Folder to save PDF

    Returns
    -------
    str
        Output PDF path
    """

    ensure_directory(output_folder)

    image_path = Path(image_path)

    pdf_path = Path(output_folder) / f"{image_path.stem}.pdf"

    image = Image.open(image_path)

    # Convert transparency if present
    if image.mode in ("RGBA", "LA", "P"):
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
        image = background

    elif image.mode != "RGB":
        image = image.convert("RGB")

    image.save(pdf_path, "PDF", resolution=100.0)

    return str(pdf_path)


def convert_file(file_path, output_folder):
    """
    Convert supported file to PDF.

    Parameters
    ----------
    file_path : str

    output_folder : str

    Returns
    -------
    str
        PDF file path
    """

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return file_path

    if extension in SUPPORTED_IMAGES:
        return image_to_pdf(file_path, output_folder)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


def convert_multiple(file_list, output_folder):
    """
    Convert multiple files.

    Parameters
    ----------
    file_list : list

    output_folder : str

    Returns
    -------
    list
        List of PDF paths
    """

    ensure_directory(output_folder)

    pdf_files = []

    for file in file_list:
        pdf = convert_file(file, output_folder)
        pdf_files.append(pdf)

    return pdf_files


def is_pdf(file_path):
    """
    Check if file is PDF.
    """

    return Path(file_path).suffix.lower() == ".pdf"


def is_image(file_path):
    """
    Check if file is image.
    """

    return Path(file_path).suffix.lower() in SUPPORTED_IMAGES


def supported_extensions():
    """
    Return supported extensions.
    """

    return [".pdf"] + list(SUPPORTED_IMAGES)


def validate_file(file_path):
    """
    Validate file.

    Returns
    -------
    bool
    """

    if not os.path.exists(file_path):
        return False

    ext = Path(file_path).suffix.lower()

    return ext in supported_extensions()


def file_type(file_path):
    """
    Return file category.
    """

    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        return "PDF"

    if ext in SUPPORTED_IMAGES:
        return "IMAGE"

    return "UNKNOWN"


def count_supported(files):
    """
    Count supported files.
    """

    count = 0

    for file in files:
        if validate_file(file):
            count += 1

    return count


def count_images(files):
    """
    Count image files.
    """

    return sum(is_image(f) for f in files)


def count_pdfs(files):
    """
    Count pdf files.
    """

    return sum(is_pdf(f) for f in files)


def get_summary(files):
    """
    Return summary dictionary.
    """

    return {
        "total": len(files),
        "pdfs": count_pdfs(files),
        "images": count_images(files),
        "supported": count_supported(files),
    }


if __name__ == "__main__":

    print("Supported Extensions")

    for ext in supported_extensions():
        print(ext)
