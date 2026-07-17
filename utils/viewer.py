"""
utils/viewer.py

PDF Viewer Utilities

Uses:
    PyMuPDF (fitz)

Features
--------
✔ Open PDF
✔ Render Page
✔ Zoom
✔ Page Navigation
✔ Thumbnail
✔ PDF Metadata
✔ Page Size
✔ Close PDF

Author : PragyanAI
"""

import fitz
from PIL import Image
import io
from pathlib import Path


# -----------------------------------------------------
# Open PDF
# -----------------------------------------------------

def open_pdf(pdf_path):
    """
    Open PDF document.

    Returns
    -------
    fitz.Document
    """

    return fitz.open(pdf_path)


# -----------------------------------------------------
# Close PDF
# -----------------------------------------------------

def close_pdf(doc):
    """
    Close document safely.
    """

    if doc:
        doc.close()


# -----------------------------------------------------
# Page Count
# -----------------------------------------------------

def page_count(doc):

    return doc.page_count


# -----------------------------------------------------
# Metadata
# -----------------------------------------------------

def metadata(doc):

    return doc.metadata


# -----------------------------------------------------
# Page Size
# -----------------------------------------------------

def page_size(doc, page_number):

    page = doc.load_page(page_number)

    rect = page.rect

    return {

        "width": rect.width,

        "height": rect.height

    }


# -----------------------------------------------------
# Render Page
# -----------------------------------------------------

def render_page(
    doc,
    page_number,
    zoom=2.0
):
    """
    Convert page to PIL Image.
    """

    page = doc.load_page(page_number)

    matrix = fitz.Matrix(zoom, zoom)

    pix = page.get_pixmap(matrix=matrix)

    image = Image.open(
        io.BytesIO(
            pix.tobytes("png")
        )
    )

    return image


# -----------------------------------------------------
# Thumbnail
# -----------------------------------------------------

def thumbnail(
    doc,
    page_number,
    width=180
):
    """
    Generate page thumbnail.
    """

    page = doc.load_page(page_number)

    zoom = width / page.rect.width

    matrix = fitz.Matrix(zoom, zoom)

    pix = page.get_pixmap(matrix=matrix)

    image = Image.open(
        io.BytesIO(
            pix.tobytes("png")
        )
    )

    return image


# -----------------------------------------------------
# Render All Thumbnails
# -----------------------------------------------------

def all_thumbnails(
    doc,
    width=150
):

    thumbs = []

    for page in range(doc.page_count):

        thumbs.append(
            thumbnail(
                doc,
                page,
                width
            )
        )

    return thumbs


# -----------------------------------------------------
# First Page
# -----------------------------------------------------

def first_page():

    return 0


# -----------------------------------------------------
# Last Page
# -----------------------------------------------------

def last_page(doc):

    return doc.page_count - 1


# -----------------------------------------------------
# Next Page
# -----------------------------------------------------

def next_page(
    current,
    total
):

    if current < total - 1:
        return current + 1

    return current


# -----------------------------------------------------
# Previous Page
# -----------------------------------------------------

def previous_page(current):

    if current > 0:
        return current - 1

    return current


# -----------------------------------------------------
# Go To Page
# -----------------------------------------------------

def goto_page(
    page,
    total
):

    if page < 0:
        return 0

    if page >= total:
        return total - 1

    return page


# -----------------------------------------------------
# Render Multiple Pages
# -----------------------------------------------------

def render_pages(
    doc,
    start=0,
    end=None,
    zoom=1.5
):

    if end is None:
        end = doc.page_count

    pages = []

    for page in range(start, end):

        pages.append(
            render_page(
                doc,
                page,
                zoom
            )
        )

    return pages


# -----------------------------------------------------
# Search Text
# -----------------------------------------------------

def search_text(
    doc,
    keyword
):
    """
    Returns page numbers containing keyword.
    """

    results = []

    keyword = keyword.lower()

    for page_no in range(doc.page_count):

        page = doc.load_page(page_no)

        text = page.get_text()

        if keyword in text.lower():

            results.append(page_no)

    return results


# -----------------------------------------------------
# Extract Text
# -----------------------------------------------------

def extract_page_text(
    doc,
    page_number
):

    page = doc.load_page(page_number)

    return page.get_text()


# -----------------------------------------------------
# PDF Information
# -----------------------------------------------------

def pdf_information(doc):

    return {

        "Pages": doc.page_count,

        "Title": doc.metadata.get("title", ""),

        "Author": doc.metadata.get("author", ""),

        "Subject": doc.metadata.get("subject", ""),

        "Creator": doc.metadata.get("creator", ""),

        "Producer": doc.metadata.get("producer", ""),

        "Keywords": doc.metadata.get("keywords", ""),

    }


# -----------------------------------------------------
# File Size
# -----------------------------------------------------

def pdf_size(pdf_path):

    return round(
        Path(pdf_path).stat().st_size /
        (1024 * 1024),
        2
    )


# -----------------------------------------------------
# Validate Page Number
# -----------------------------------------------------

def valid_page(
    doc,
    page_number
):

    return 0 <= page_number < doc.page_count


# -----------------------------------------------------
# Zoom Levels
# -----------------------------------------------------

def zoom_levels():

    return {

        "50%": 0.5,

        "75%": 0.75,

        "100%": 1.0,

        "125%": 1.25,

        "150%": 1.5,

        "200%": 2.0,

        "300%": 3.0

    }


# -----------------------------------------------------
# Rotation
# -----------------------------------------------------

def page_rotation(
    doc,
    page_number
):

    page = doc.load_page(page_number)

    return page.rotation


# -----------------------------------------------------
# Test
# -----------------------------------------------------

if __name__ == "__main__":

    print("Viewer Module Loaded Successfully")
