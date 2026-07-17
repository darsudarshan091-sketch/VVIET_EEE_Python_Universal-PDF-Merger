"""
utils/helpers.py

General helper functions used across the project.

Author : PragyanAI
"""

from pathlib import Path
from datetime import datetime
import hashlib
import os
import uuid


# ---------------------------------------------------------
# Bytes to KB / MB / GB
# ---------------------------------------------------------

def format_size(size):

    if size < 1024:
        return f"{size} Bytes"

    elif size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"

    elif size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"

    return f"{size / (1024 ** 3):.2f} GB"


# ---------------------------------------------------------
# File Size
# ---------------------------------------------------------

def file_size(file_path):

    return format_size(
        os.path.getsize(file_path)
    )


# ---------------------------------------------------------
# Current Timestamp
# ---------------------------------------------------------

def timestamp():

    return datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )


# ---------------------------------------------------------
# Human Date
# ---------------------------------------------------------

def current_datetime():

    return datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )


# ---------------------------------------------------------
# Filename
# ---------------------------------------------------------

def filename(path):

    return Path(path).name


# ---------------------------------------------------------
# Filename without Extension
# ---------------------------------------------------------

def stem(path):

    return Path(path).stem


# ---------------------------------------------------------
# Extension
# ---------------------------------------------------------

def extension(path):

    return Path(path).suffix.lower()


# ---------------------------------------------------------
# Unique Output Filename
# ---------------------------------------------------------

def unique_pdf_name(prefix="Merged"):

    return f"{prefix}_{timestamp()}.pdf"


# ---------------------------------------------------------
# UUID Filename
# ---------------------------------------------------------

def uuid_filename(ext=".pdf"):

    return f"{uuid.uuid4().hex}{ext}"


# ---------------------------------------------------------
# MD5 Hash
# ---------------------------------------------------------

def md5(file_path):

    hash_md5 = hashlib.md5()

    with open(file_path, "rb") as f:

        for chunk in iter(lambda: f.read(4096), b""):

            hash_md5.update(chunk)

    return hash_md5.hexdigest()


# ---------------------------------------------------------
# File Icon
# ---------------------------------------------------------

def file_icon(file_name):

    ext = extension(file_name)

    icons = {

        ".pdf": "📕",

        ".jpg": "🖼️",

        ".jpeg": "🖼️",

        ".png": "🖼️",

        ".bmp": "🖼️",

        ".gif": "🖼️",

        ".tif": "🖼️",

        ".tiff": "🖼️",

    }

    return icons.get(ext, "📄")


# ---------------------------------------------------------
# Status Icon
# ---------------------------------------------------------

def status_icon(status):

    icons = {

        "success": "✅",

        "warning": "⚠️",

        "error": "❌",

        "info": "ℹ️"

    }

    return icons.get(status.lower(), "•")


# ---------------------------------------------------------
# Progress Percentage
# ---------------------------------------------------------

def percentage(value, total):

    if total == 0:

        return 0

    return round((value / total) * 100, 2)


# ---------------------------------------------------------
# Safe Integer
# ---------------------------------------------------------

def to_int(value, default=0):

    try:

        return int(value)

    except:

        return default


# ---------------------------------------------------------
# Safe Float
# ---------------------------------------------------------

def to_float(value, default=0.0):

    try:

        return float(value)

    except:

        return default


# ---------------------------------------------------------
# Clamp Number
# ---------------------------------------------------------

def clamp(value, minimum, maximum):

    return max(minimum, min(value, maximum))


# ---------------------------------------------------------
# PDF Statistics
# ---------------------------------------------------------

def pdf_statistics(pdf_files, page_counts=None):

    if page_counts is None:

        page_counts = []

    return {

        "Total Files": len(pdf_files),

        "Total Pages": sum(page_counts),

        "Average Pages": round(
            sum(page_counts) / len(page_counts), 2
        ) if page_counts else 0

    }


# ---------------------------------------------------------
# Divider
# ---------------------------------------------------------

def divider(length=60):

    return "-" * length


# ---------------------------------------------------------
# Welcome Banner
# ---------------------------------------------------------

def banner():

    return """
=============================================
 Universal Document Merger
=============================================
"""


# ---------------------------------------------------------
# Merge Summary
# ---------------------------------------------------------

def merge_summary(files, output_pdf):

    return {

        "Merged Files": len(files),

        "Output": output_pdf,

        "Created": current_datetime()

    }


# ---------------------------------------------------------
# Image Extensions
# ---------------------------------------------------------

def image_extensions():

    return [

        ".jpg",

        ".jpeg",

        ".png",

        ".bmp",

        ".gif",

        ".tif",

        ".tiff"

    ]


# ---------------------------------------------------------
# Supported Extensions
# ---------------------------------------------------------

def supported_extensions():

    return [

        ".pdf",

        ".jpg",

        ".jpeg",

        ".png",

        ".bmp",

        ".gif",

        ".tif",

        ".tiff"

    ]


# ---------------------------------------------------------
# Is Image
# ---------------------------------------------------------

def is_image(file_path):

    return extension(file_path) in image_extensions()


# ---------------------------------------------------------
# Is PDF
# ---------------------------------------------------------

def is_pdf(file_path):

    return extension(file_path) == ".pdf"


# ---------------------------------------------------------
# Greeting
# ---------------------------------------------------------

def greeting():

    hour = datetime.now().hour

    if hour < 12:

        return "Good Morning"

    elif hour < 17:

        return "Good Afternoon"

    return "Good Evening"


# ---------------------------------------------------------
# About App
# ---------------------------------------------------------

def about():

    return {

        "Application": "Universal Document Merger",

        "Version": "1.0",

        "Framework": "Streamlit",

        "Language": "Python",

        "Supports": "PDF + Images",

    }


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    print(banner())

    print(about())
