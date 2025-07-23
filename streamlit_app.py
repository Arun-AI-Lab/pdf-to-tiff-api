import streamlit as st
import os
from app.converter import convert_pdf_pages_to_tiff
from pdf2image import convert_from_path
from PIL import Image
import shutil

st.set_page_config(page_title="PDF to TIFF Converter", layout="centered")
st.title("📄➡️🖼 Convert Selected PDF Pages to TIFF")

uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_pdf:
    st.success("PDF uploaded successfully.")
    page_input = st.text_input("Enter page numbers (e.g., 1,2,5)")

    if st.button("Convert to TIFF"):
        if not page_input.strip():
            st.error("Please enter page numbers.")
        else:
            try:
                os.makedirs("input_pdfs", exist_ok=True)
                os.makedirs("output_tiffs", exist_ok=True)

                # Save uploaded file
                file_path = f"input_pdfs/{uploaded_pdf.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_pdf.read())

                page_indices = [int(p.strip()) - 1 for p in page_input.split(",") if p.strip().isdigit()]
                tiff_paths = convert_pdf_pages_to_tiff(file_path, "output_tiffs", page_indices)

                st.success(f"{len(tiff_paths)} page(s) converted.")
                for tiff_path in tiff_paths:
                    with open(tiff_path, "rb") as f:
                        st.download_button(
                            label=f"Download {os.path.basename(tiff_path)}",
                            data=f,
                            file_name=os.path.basename(tiff_path),
                            mime="image/tiff"
                        )
            except Exception as e:
                st.error(f"Error: {str(e)}")
