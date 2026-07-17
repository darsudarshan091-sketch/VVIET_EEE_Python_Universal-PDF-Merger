"""
utils/file_handler.py

Handles uploaded files for the Universal Document Merger.

Features
--------
✔ Save uploaded Streamlit files
✔ Create temp/output folders
✔ Validate file extensions
✔ Get file information
✔ Delete temporary files
✔ Delete folders
✔ List files
✔ Calculate folder size

Author : PragyanAI
"""

from pathlib import Path
import shutil
import os
from datetime import datetime


# ---------------------------------------------------
# Supported Extensions
# ---------------------------------------------------

SUPPORTED_EXTENSIONS = (
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".gif",
)


# ---------------------------------------------------
# Create Directory
# ---------------------------------------------------

def create_directory(folder):

    Path(folder).mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------
# Save Uploaded File
# ---------------------------------------------------

def save_uploaded_file(uploaded_file, folder="temp"):

    create_directory(folder)

    destination = Path(folder) / uploaded_file.name

    with open(destination, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(destination)


# ---------------------------------------------------
# Save Multiple Files
# ---------------------------------------------------

def save_multiple_files(uploaded_files, folder="temp"):

    saved_files = []

    for file in uploaded_files:
        saved_files.append(
            save_uploaded_file(file, folder)
        )

    return saved_files


# ---------------------------------------------------
# Extension
# ---------------------------------------------------

def get_extension(file_path):

    return Path(file_path).suffix.lower()


# ---------------------------------------------------
# Filename
# ---------------------------------------------------

def get_filename(file_path):

    return Path(file_path).name


# ---------------------------------------------------
# Filename without Extension
# ---------------------------------------------------

def get_stem(file_path):

    return Path(file_path).stem


# ---------------------------------------------------
# Check Supported
# ---------------------------------------------------

def is_supported(file_path):

    return get_extension(file_path) in SUPPORTED_EXTENSIONS


# ---------------------------------------------------
# Validate Files
# ---------------------------------------------------

def validate_files(file_list):

    valid = []
    invalid = []

    for file in file_list:

        if is_supported(file):
            valid.append(file)

        else:
            invalid.append(file)

    return valid, invalid


# ---------------------------------------------------
# File Size (Bytes)
# ---------------------------------------------------

def file_size(file_path):

    return os.path.getsize(file_path)


# ---------------------------------------------------
# File Size (MB)
# ---------------------------------------------------

def file_size_mb(file_path):

    size = os.path.getsize(file_path)

    return round(size / (1024 * 1024), 2)


# ---------------------------------------------------
# File Info
# ---------------------------------------------------

def file_info(file_path):

    path = Path(file_path)

    return {

        "name": path.name,

        "stem": path.stem,

        "extension": path.suffix,

        "size_mb": file_size_mb(file_path),

        "created": datetime.fromtimestamp(
            path.stat().st_ctime
        ),

        "modified": datetime.fromtimestamp(
            path.stat().st_mtime
        )

    }


# ---------------------------------------------------
# List Files
# ---------------------------------------------------

def list_files(folder):

    folder = Path(folder)

    if not folder.exists():
        return []

    return sorted(

        [

            str(file)

            for file in folder.iterdir()

            if file.is_file()

        ]

    )


# ---------------------------------------------------
# Delete File
# ---------------------------------------------------

def delete_file(file_path):

    file = Path(file_path)

    if file.exists():

        file.unlink()

        return True

    return False


# ---------------------------------------------------
# Delete Multiple Files
# ---------------------------------------------------

def delete_files(file_list):

    for file in file_list:

        delete_file(file)


# ---------------------------------------------------
# Empty Folder
# ---------------------------------------------------

def clear_folder(folder):

    folder = Path(folder)

    if not folder.exists():
        return

    for item in folder.iterdir():

        if item.is_file():

            item.unlink()

        elif item.is_dir():

            shutil.rmtree(item)


# ---------------------------------------------------
# Delete Folder
# ---------------------------------------------------

def delete_folder(folder):

    folder = Path(folder)

    if folder.exists():

        shutil.rmtree(folder)


# ---------------------------------------------------
# Folder Size
# ---------------------------------------------------

def folder_size(folder):

    total = 0

    folder = Path(folder)

    if not folder.exists():

        return 0

    for file in folder.rglob("*"):

        if file.is_file():

            total += file.stat().st_size

    return round(total / (1024 * 1024), 2)


# ---------------------------------------------------
# Count Files
# ---------------------------------------------------

def count_files(folder):

    folder = Path(folder)

    if not folder.exists():

        return 0

    return len(

        [

            f

            for f in folder.iterdir()

            if f.is_file()

        ]

    )


# ---------------------------------------------------
# Exists
# ---------------------------------------------------

def file_exists(file_path):

    return Path(file_path).exists()


# ---------------------------------------------------
# Rename File
# ---------------------------------------------------

def rename_file(old_path, new_name):

    old = Path(old_path)

    new = old.parent / new_name

    old.rename(new)

    return str(new)


# ---------------------------------------------------
# Copy File
# ---------------------------------------------------

def copy_file(source, destination):

    shutil.copy(source, destination)

    return destination


# ---------------------------------------------------
# Move File
# ---------------------------------------------------

def move_file(source, destination):

    shutil.move(source, destination)

    return destination


# ---------------------------------------------------
# Supported File List
# ---------------------------------------------------

def supported_files():

    return list(SUPPORTED_EXTENSIONS)


# ---------------------------------------------------
# Summary
# ---------------------------------------------------

def summary(folder):

    return {

        "files": count_files(folder),

        "folder_size_mb": folder_size(folder),

        "supported_extensions": supported_files()

    }


# ---------------------------------------------------
# Test
# ---------------------------------------------------

if __name__ == "__main__":

    create_directory("temp")

    create_directory("outputs")

    print(summary("temp"))
