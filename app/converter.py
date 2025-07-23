import fitz  # PyMuPDF
from PIL import Image, ImageOps, ImageFilter
import os

def convert_pdf_pages_to_tiff(pdf_path, output_dir, page_indices, dpi=300):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    output_files = []

    for i in page_indices:
        if i < 0 or i >= len(doc):
            continue

        # Render page to image
        pix = doc.load_page(i).get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        gray = img.convert("L")
        enhanced = ImageOps.autocontrast(gray, cutoff=1)
        sharpened = enhanced.filter(ImageFilter.SHARPEN)

        filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{i+1}.tiff"
        output_path = os.path.join(output_dir, filename)
        sharpened.save(output_path, format='TIFF', compression='tiff_lzw')

        output_files.append(output_path)

    return output_files
