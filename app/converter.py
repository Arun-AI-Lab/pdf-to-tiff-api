from pdf2image import convert_from_path
from PIL import Image, ImageOps, ImageFilter
import os

def convert_pdf_pages_to_tiff(pdf_path, output_dir, page_indices, dpi=600):
    os.makedirs(output_dir, exist_ok=True)

    pages = convert_from_path(pdf_path, dpi=dpi)
    output_files = []

    for i in page_indices:
        if i < 0 or i >= len(pages):
            continue  # skip invalid page

        page = pages[i]
        gray = page.convert('L')
        enhanced = ImageOps.autocontrast(gray, cutoff=1)
        sharpened = enhanced.filter(ImageFilter.SHARPEN)

        filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{i+1}.tiff"
        output_path = os.path.join(output_dir, filename)
        sharpened.save(output_path, format='TIFF', compression='tiff_lzw')

        output_files.append(output_path)

    return output_files
