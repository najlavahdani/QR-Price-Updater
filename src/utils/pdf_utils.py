# src/utils/pdf_utils.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from math import ceil

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\Tahoma.ttf",
]

def _find_system_font():
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    return None

def _shape_text_if_possible(text: str) -> str:
    """
    Try to use arabic_reshaper + python-bidi to shape Arabic/Persian text.
    If those packages are not installed, return the original text.
    """
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception:
        # if libs not available, return text as-is (may appear disconnected)
        return text

def create_qr_pdf(qr_items, output_path, font_path: str | None = None, title: str | None = None):
    """
    Create a PDF with QR images in 2x3 grid per page, with product name and ID below each image.

    Args:
        qr_items (list[dict]): each dict: { "image_path": str, "product_id": str, "product_name": str }
        output_path (str): destination PDF path
        font_path (str|None): optional path to a TTF font that supports Persian. If None, the function tries to auto-find one.
        title (str|None): optional title to print at top of each page.

    Returns:
        str: output_path
    Raises:
        RuntimeError: if no suitable font is found.
        ValueError: if qr_items is empty.
    """
    if not qr_items:
        raise ValueError("No QR items provided.")

    # find or validate font
    if font_path:
        if not os.path.exists(font_path):
            raise RuntimeError(f"Provided font_path not found: {font_path}")
    else:
        font_path = _find_system_font()
    if not font_path:
        raise RuntimeError(
            "No suitable TTF font found on the system. لطفاً یک فونت TTF یونیکد (مثلاً Tahoma یا DejaVuSans یا Vazirmatn) "
            "در مسیر مشخص قرار دهید یا مسیر آن را به پارامتر font_path بدهید."
        )

    # register font
    font_name = "CustomPDFFont"
    pdfmetrics.registerFont(TTFont(font_name, font_path))

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    cols, rows = 2, 3
    margin_x, margin_y = 50, 80
    spacing_x, spacing_y = 30, 30

    # calculate cell sizes (reserve some space for text under image)
    cell_w = (width - 2 * margin_x - (cols - 1) * spacing_x) / cols
    cell_h = (height - 2 * margin_y - (rows - 1) * spacing_y) / rows
    img_max_h = cell_h * 0.72  # reserve ~28% for text
    img_max_w = cell_w * 0.9

    items_per_page = cols * rows
    total_pages = ceil(len(qr_items) / items_per_page)

    for idx, item in enumerate(qr_items):
        page_idx = idx // items_per_page
        pos = idx % items_per_page

        if pos == 0:
            # new page
            c.showPage() if idx != 0 else None
            if title:
                t = _shape_text_if_possible(title)
                c.setFont(font_name, 16)
                c.drawCentredString(width / 2, height - 40, t)

        col = pos % cols
        row = pos // cols

        x = margin_x + col * (cell_w + spacing_x)
        y_top = height - margin_y - row * (cell_h + spacing_y)  # top y of the cell

        img_path = item.get("image_path")
        prod_id = str(item.get("product_id", ""))
        prod_name = str(item.get("product_name", ""))

        if os.path.exists(img_path):
            try:
                img = ImageReader(img_path)
                iw, ih = img.getSize()
                scale = min(img_max_w / iw, img_max_h / ih)
                draw_w = iw * scale
                draw_h = ih * scale
                draw_x = x + (cell_w - draw_w) / 2
                draw_y = y_top - draw_h - 30  # leave 30pt for spacing above text

                c.drawImage(img, draw_x, draw_y, draw_w, draw_h, preserveAspectRatio=True, mask='auto')
            except Exception as e:
                print(f"Warning: failed to draw image {img_path}: {e}")
        else:
            print(f"Warning: image not found: {img_path}")

        # prepare and draw product text (shape for RTL if possible)
        text = f"{prod_name}\nID: {prod_id}"
        text = _shape_text_if_possible(text)

        c.setFont(font_name, 11)
        # draw two lines centered under the image
        cx = x + cell_w / 2
        # starting Y: a bit below drawn image or a default if image missing
        text_start_y = (draw_y - 8) if os.path.exists(img_path) else (y_top - img_max_h - 20)

        lines = text.split("\n")
        for i_line, line in enumerate(lines):
            c.drawCentredString(cx, text_start_y - (i_line * 14), line)

    # save (if last page hasn't been shownPage called after loop, saving is fine)
    c.save()
    return output_path
