import pikepdf
from pikepdf import Pdf, PdfImage
import os
from tkinter import filedialog


# --------------------
# Helpers
# --------------------
def get_save_path(default_name="output.pdf"):
    """Ask user for destination file path"""
    return filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        initialfile=default_name
    )


# --------------------
# PDF Functions
# --------------------
def reverse_pdf(file):
    pdf = Pdf.open(file)
    pdf.pages.reverse()
    out = get_save_path("reverse.pdf")
    if out:
        pdf.save(out)
        return out
    return None


def delete_pages(file, start, end):
    pdf = Pdf.open(file)
    del pdf.pages[start - 1:end]
    out = get_save_path("delete.pdf")
    if out:
        pdf.save(out)
        return out
    return None


def replace_page(file, src, dst):
    pdf = Pdf.open(file)
    pdf.pages[src - 1] = pdf.pages[dst - 1]
    out = get_save_path("replace.pdf")
    if out:
        pdf.save(out)
        return out
    return None


def rotate_pdf(file, angle):
    pdf = Pdf.open(file)
    for page in pdf.pages:
        page.Rotate = (page.Rotate or 0) + angle
    out = get_save_path("rotate.pdf")
    if out:
        pdf.save(out)
        return out
    return None


def encrypt_pdf(file, user_pw, owner_pw):
    pdf = Pdf.open(file)
    out = get_save_path("encrypted.pdf")
    if out:
        pdf.save(out, encryption=pikepdf.Encryption(user=user_pw, owner=owner_pw))
        return out
    return None


def extract_pages(file, start, end):
    pdf = Pdf.open(file)
    new_pdf = Pdf.new()
    for i in range(start - 1, end):
        new_pdf.pages.append(pdf.pages[i])
    out = get_save_path(f"pages_{start}_{end}.pdf")
    if out:
        new_pdf.save(out)
        return out
    return None


def extract_images(file, page_num):
    pdf = Pdf.open(file)
    page = pdf.pages[page_num - 1]
    if not page.images:
        return None

    for i, (name, raw_image) in enumerate(page.images.items(), start=1):
        pdf_image = PdfImage(raw_image)
        out = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=f"image_page{page_num}_{i}.png",
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")]
        )
        if out:
            pdf_image.extract_to(fileprefix=os.path.splitext(out)[0])
    return "Images saved"


def compress_pdf(file):
    pdf = Pdf.open(file)

    # Save temporary compressed file
    out = get_save_path("compressed.pdf")
    if not out:
        return None, None, None

    before_size = os.path.getsize(file)

    pdf.save(
        out,
        compress_streams=True,
        recompress_flate=True
    )

    after_size = os.path.getsize(out)
    return out, before_size, after_size
