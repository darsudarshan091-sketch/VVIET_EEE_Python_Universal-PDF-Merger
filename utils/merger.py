"""
utils/merger.py

Universal Document Merger

Functions
---------
✔ Merge PDFs
✔ Delete Pages
✔ Rotate Pages
✔ Split PDF
✔ Extract Pages
✔ Count Pages
✔ Validate PDF

Author : PragyanAI
"""

from pathlib import Path
from pypdf import PdfReader, PdfWriter
import os


# ---------------------------------------------------
# Create Output Folder
# ---------------------------------------------------

def ensure_directory(folder):

    Path(folder).mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------
# Validate PDF
# ---------------------------------------------------

def is_valid_pdf(pdf_path):

    try:
        PdfReader(pdf_path)
        return True

    except Exception:
        return False


# ---------------------------------------------------
# Total Pages
# ---------------------------------------------------

def get_page_count(pdf_path):

    reader = PdfReader(pdf_path)

    return len(reader.pages)


# ---------------------------------------------------
# PDF Information
# ---------------------------------------------------

def get_pdf_info(pdf_path):

    reader = PdfReader(pdf_path)

    return {
        "pages": len(reader.pages),
        "encrypted": reader.is_encrypted,
        "metadata": reader.metadata
    }


# ---------------------------------------------------
# Merge PDFs
# ---------------------------------------------------

def merge_pdfs(pdf_files,
               output_folder="outputs",
               output_name="merged.pdf"):

    ensure_directory(output_folder)

    output_path = Path(output_folder) / output_name

    writer = PdfWriter()

    for pdf in pdf_files:

        if not is_valid_pdf(pdf):
            continue

        reader = PdfReader(pdf)

        for page in reader.pages:
            writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

    writer.close()

    return str(output_path)


# ---------------------------------------------------
# Delete Pages
# ---------------------------------------------------

def delete_pages(input_pdf,
                 page_numbers,
                 output_pdf):

    reader = PdfReader(input_pdf)

    writer = PdfWriter()

    remove = set(page_numbers)

    for index, page in enumerate(reader.pages):

        if index not in remove:
            writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    writer.close()

    return output_pdf


# ---------------------------------------------------
# Rotate Pages
# ---------------------------------------------------

def rotate_page(input_pdf,
                output_pdf,
                page_number,
                angle=90):

    reader = PdfReader(input_pdf)

    writer = PdfWriter()

    for index, page in enumerate(reader.pages):

        if index == page_number:
            page.rotate(angle)

        writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    writer.close()

    return output_pdf


# ---------------------------------------------------
# Split PDF
# ---------------------------------------------------

def split_pdf(input_pdf,
              output_folder):

    ensure_directory(output_folder)

    reader = PdfReader(input_pdf)

    files = []

    for i, page in enumerate(reader.pages):

        writer = PdfWriter()

        writer.add_page(page)

        filename = Path(output_folder) / f"page_{i+1}.pdf"

        with open(filename, "wb") as f:
            writer.write(f)

        files.append(str(filename))

    return files


# ---------------------------------------------------
# Extract Page Range
# ---------------------------------------------------

def extract_pages(input_pdf,
                  output_pdf,
                  start_page,
                  end_page):

    reader = PdfReader(input_pdf)

    writer = PdfWriter()

    for i in range(start_page, end_page + 1):

        if i < len(reader.pages):
            writer.add_page(reader.pages[i])

    with open(output_pdf, "wb") as f:
        writer.write(f)

    writer.close()

    return output_pdf


# ---------------------------------------------------
# Merge Folder PDFs
# ---------------------------------------------------

def merge_folder(folder,
                 output_pdf):

    pdfs = sorted(Path(folder).glob("*.pdf"))

    pdfs = [str(x) for x in pdfs]

    return merge_pdfs(
        pdfs,
        Path(output_pdf).parent,
        Path(output_pdf).name
    )


# ---------------------------------------------------
# List PDF Files
# ---------------------------------------------------

def list_pdfs(folder):

    return sorted(
        [
            str(x)
            for x in Path(folder).glob("*.pdf")
        ]
    )


# ---------------------------------------------------
# File Size
# ---------------------------------------------------

def get_pdf_size(pdf_path):

    size = os.path.getsize(pdf_path)

    return round(size / (1024 * 1024), 2)


# ---------------------------------------------------
# Check Encryption
# ---------------------------------------------------

def is_encrypted(pdf_path):

    reader = PdfReader(pdf_path)

    return reader.is_encrypted


# ---------------------------------------------------
# PDF Exists
# ---------------------------------------------------

def pdf_exists(pdf_path):

    return Path(pdf_path).exists()


# ---------------------------------------------------
# Copy PDF
# ---------------------------------------------------

def copy_pdf(input_pdf,
             output_pdf):

    reader = PdfReader(input_pdf)

    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    writer.close()

    return output_pdf


# ---------------------------------------------------
# Merge Statistics
# ---------------------------------------------------

def merge_statistics(pdf_files):

    total_pages = 0

    valid_files = 0

    for pdf in pdf_files:

        if is_valid_pdf(pdf):

            valid_files += 1

            total_pages += get_page_count(pdf)

    return {

        "files": valid_files,

        "pages": total_pages

    }


# ---------------------------------------------------
# Test
# ---------------------------------------------------

if __name__ == "__main__":

    print("Merger Module Loaded Successfully")
