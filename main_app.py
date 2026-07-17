"""
app.py (Part 1)
Universal Document Merger

Part 1
------
✔ Imports
✔ Page Configuration
✔ Session State
✔ Sidebar
✔ Upload Files
✔ Save Uploaded Files
✔ Convert Images → PDF
✔ Prepare PDF List

Continue with Part 2 after this.
"""

import os
from pathlib import Path

import streamlit as st

from utils.converter import convert_multiple
from utils.file_handler import (
    create_directory,
    save_multiple_files,
    clear_folder,
)
from utils.helpers import (
    file_icon,
    file_size,
    unique_pdf_name,
)

# --------------------------------------------------------
# Project Folders
# --------------------------------------------------------

TEMP_DIR = "temp"
OUTPUT_DIR = "outputs"
ASSET_DIR = "assets"

create_directory(TEMP_DIR)
create_directory(OUTPUT_DIR)

# --------------------------------------------------------
# Streamlit Configuration
# --------------------------------------------------------

st.set_page_config(
    page_title="Universal Document Merger",
    page_icon="📄",
    layout="wide",
)

# --------------------------------------------------------
# Session State
# --------------------------------------------------------

if "merged_pdf" not in st.session_state:
    st.session_state.merged_pdf = None

if "pdf_files" not in st.session_state:
    st.session_state.pdf_files = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "page_number" not in st.session_state:
    st.session_state.page_number = 0

if "zoom" not in st.session_state:
    st.session_state.zoom = 2.0

# --------------------------------------------------------
# Header
# --------------------------------------------------------

st.title("📄 Universal Document Merger")

st.caption(
    "Merge PDF files and Images into a single PDF document."
)

# --------------------------------------------------------
# Sidebar
# --------------------------------------------------------

with st.sidebar:

    st.header("Settings")

    st.session_state.zoom = st.slider(
        "Viewer Zoom",
        min_value=1.0,
        max_value=4.0,
        value=2.0,
        step=0.25,
    )

    st.divider()

    if st.button(
        "🧹 Clear Temporary Files",
        use_container_width=True,
    ):

        clear_folder(TEMP_DIR)
        clear_folder(OUTPUT_DIR)

        st.session_state.pdf_files = []
        st.session_state.uploaded_files = []
        st.session_state.merged_pdf = None
        st.session_state.page_number = 0

        st.success("Temporary files deleted.")

# --------------------------------------------------------
# Upload Area
# --------------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload PDF or Image Files",
    type=[
        "pdf",
        "jpg",
        "jpeg",
        "png",
        "bmp",
        "gif",
        "tif",
        "tiff",
    ],
    accept_multiple_files=True,
)

# --------------------------------------------------------
# Save Files
# --------------------------------------------------------

if uploaded_files:

    st.session_state.uploaded_files = uploaded_files

    saved_files = save_multiple_files(
        uploaded_files,
        TEMP_DIR,
    )

    pdf_files = convert_multiple(
        saved_files,
        OUTPUT_DIR,
    )

    st.session_state.pdf_files = pdf_files

# --------------------------------------------------------
# Uploaded Files Preview
# --------------------------------------------------------

if st.session_state.uploaded_files:

    st.subheader("Uploaded Files")

    total_size = 0

    for file in st.session_state.uploaded_files:

        icon = file_icon(file.name)

        path = os.path.join(
            TEMP_DIR,
            file.name,
        )

        if Path(path).exists():

            size = file_size(path)

            total_size += Path(path).stat().st_size

        else:

            size = "Unknown"

        st.write(f"{icon} **{file.name}** — {size}")

    st.info(
        f"Total Files : {len(st.session_state.uploaded_files)}"
    )

# --------------------------------------------------------
# Ready for Merge
# --------------------------------------------------------

if st.session_state.pdf_files:

    st.success(
        f"{len(st.session_state.pdf_files)} PDF(s) ready for merging."
    )

    st.subheader("PDF Processing Queue")

    for index, pdf in enumerate(
        st.session_state.pdf_files,
        start=1,
    ):

        st.write(
            f"{index}. {Path(pdf).name}"
        )

# --------------------------------------------------------
# Merge Section Placeholder
# --------------------------------------------------------

st.divider()

st.subheader("Merge Documents")

merge_clicked = st.button(
    "📄 Merge All Documents",
    type="primary",
    use_container_width=True,
)

# --------------------------------------------------------
# Part 2 Starts From Here
# --------------------------------------------------------
# ==========================================================
# PART 2
# Merge PDFs
# Statistics
# Download
# Open Viewer
# ==========================================================

from utils.merger import (
    merge_pdfs,
    merge_statistics,
    get_page_count,
)

from utils.viewer import (
    open_pdf,
    page_count,
)

# ----------------------------------------------------------
# Merge Process
# ----------------------------------------------------------

if merge_clicked:

    if len(st.session_state.pdf_files) == 0:

        st.warning("Please upload at least one PDF or Image.")

    else:

        output_name = unique_pdf_name("Merged")

        with st.spinner("Merging documents..."):

            merged_pdf = merge_pdfs(
                st.session_state.pdf_files,
                OUTPUT_DIR,
                output_name,
            )

        st.session_state.merged_pdf = merged_pdf
        st.session_state.page_number = 0

        st.success("Documents merged successfully.")

# ----------------------------------------------------------
# Display Merge Result
# ----------------------------------------------------------

if st.session_state.merged_pdf is not None:

    merged_pdf = st.session_state.merged_pdf

    if Path(merged_pdf).exists():

        st.divider()

        st.header("Merged PDF")

        # -------------------------------------
        # Statistics
        # -------------------------------------

        page_counts = []

        for pdf in st.session_state.pdf_files:

            try:
                page_counts.append(
                    get_page_count(pdf)
                )
            except Exception:
                page_counts.append(0)

        stats = merge_statistics(
            st.session_state.pdf_files
        )

        total_pages = sum(page_counts)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Documents",
                stats["files"],
            )

        with col2:
            st.metric(
                "Pages",
                total_pages,
            )

        with col3:
            st.metric(
                "Output Size",
                file_size(merged_pdf),
            )

        # -------------------------------------
        # Download Button
        # -------------------------------------

        with open(merged_pdf, "rb") as pdf:

            st.download_button(
                label="⬇ Download Merged PDF",
                data=pdf,
                file_name=Path(merged_pdf).name,
                mime="application/pdf",
                use_container_width=True,
            )

        # -------------------------------------
        # Viewer Initialization
        # -------------------------------------

        try:

            doc = open_pdf(merged_pdf)

            total_pages = page_count(doc)

            st.session_state.total_pages = total_pages

            st.success(
                f"Merged PDF contains {total_pages} page(s)."
            )

        except Exception as e:

            st.error(e)

            st.stop()

# ----------------------------------------------------------
# Viewer Placeholder
# ----------------------------------------------------------

st.divider()

st.header("PDF Viewer")

# Part 3 starts below
# ==========================================================
# PART 3
# PDF Viewer
# ==========================================================

from utils.viewer import (
    render_page,
    next_page,
    previous_page,
    goto_page,
    all_thumbnails,
    close_pdf,
)

# ----------------------------------------------------------
# Show Viewer
# ----------------------------------------------------------

if st.session_state.merged_pdf:

    merged_pdf = st.session_state.merged_pdf

    doc = open_pdf(merged_pdf)

    total_pages = page_count(doc)

    # ---------------------------------------------
    # Sidebar Thumbnails
    # ---------------------------------------------

    with st.sidebar:

        st.divider()

        st.subheader("Pages")

        thumbnails = all_thumbnails(
            doc,
            width=120,
        )

        for i, thumb in enumerate(thumbnails):

            st.image(
                thumb,
                use_container_width=True,
            )

            if st.button(
                f"Page {i+1}",
                key=f"thumb_{i}",
                use_container_width=True,
            ):

                st.session_state.page_number = i
                st.rerun()

    # ---------------------------------------------
    # Page Navigation
    # ---------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(
        [1, 1, 2, 1, 1]
    )

    with col1:

        if st.button("⬅ Previous"):

            st.session_state.page_number = previous_page(
                st.session_state.page_number
            )

            st.rerun()

    with col2:

        if st.button("➡ Next"):

            st.session_state.page_number = next_page(
                st.session_state.page_number,
                total_pages,
            )

            st.rerun()

    with col3:

        selected_page = st.number_input(
            "Go To Page",
            min_value=1,
            max_value=total_pages,
            value=st.session_state.page_number + 1,
        )

        if selected_page != st.session_state.page_number + 1:

            st.session_state.page_number = goto_page(
                selected_page - 1,
                total_pages,
            )

            st.rerun()

    with col4:

        st.metric(
            "Current",
            st.session_state.page_number + 1,
        )

    with col5:

        st.metric(
            "Total",
            total_pages,
        )

    # ---------------------------------------------
    # Render Page
    # ---------------------------------------------

    page_image = render_page(
        doc,
        st.session_state.page_number,
        zoom=st.session_state.zoom,
    )

    st.image(
        page_image,
        use_container_width=True,
    )

    # ---------------------------------------------
    # Page Information
    # ---------------------------------------------

    st.info(
        f"Viewing Page "
        f"{st.session_state.page_number + 1}"
        f" of {total_pages}"
    )

    # ---------------------------------------------
    # Zoom Information
    # ---------------------------------------------

    st.caption(
        f"Zoom Level : {st.session_state.zoom:.2f}x"
    )

    # ---------------------------------------------
    # PDF Details
    # ---------------------------------------------

    with st.expander("Merged PDF Information"):

        st.write(
            {
                "File": Path(merged_pdf).name,
                "Pages": total_pages,
                "Size": file_size(merged_pdf),
            }
        )

    close_pdf(doc)

# ----------------------------------------------------------
# Footer
# ----------------------------------------------------------

st.divider()

st.markdown(
    """
    <center>

    <h5>
    📄 Universal Document Merger
    </h5>

    Merge PDF and Images into a Single PDF

    Built with ❤️ using Streamlit + PyMuPDF

    </center>
    """,
    unsafe_allow_html=True,
)
