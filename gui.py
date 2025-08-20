import tkinter as tk
from tkinter import filedialog, messagebox
import os

import core  # our pdf functions

# --------------------
# GUI Setup
# --------------------
root = tk.Tk()
root.title("PDF Editor - Open Source")
root.geometry("500x400")
root.resizable(False, False)


# --------------------
# Helper Functions
# --------------------
def choose_file():
    """Ask user to pick a PDF file"""
    filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    return filepath


def run_reverse():
    file = choose_file()
    if file:
        out = core.reverse_pdf(file)
        messagebox.showinfo("Success", f"Reversed PDF saved at:\n{out}")


def run_delete():
    file = choose_file()
    if file:
        pages = simple_input("Enter page range to delete (e.g. 2-4):")
        if not pages:
            return
        try:
            start, end = map(int, pages.split("-"))
            out = core.delete_pages(file, start=start, end=end)
            messagebox.showinfo("Success", f"Deleted pages {start}-{end}, saved at:\n{out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def run_replace():
    file = choose_file()
    if file:
        src = simple_input("Enter page to replace:")
        dst = simple_input("Enter page to copy from:")
        if src and dst:
            try:
                out = core.replace_page(file, src=int(src), dst=int(dst))
                messagebox.showinfo("Success", f"Replaced page {src} with {dst}, saved at:\n{out}")
            except Exception as e:
                messagebox.showerror("Error", str(e))


def run_rotate():
    file = choose_file()
    if file:
        angle = simple_input("Enter angle (90, 180, 270):")
        if angle:
            try:
                out = core.rotate_pdf(file, angle=int(angle))
                messagebox.showinfo("Success", f"Rotated PDF saved at:\n{out}")
            except Exception as e:
                messagebox.showerror("Error", str(e))


def run_encrypt():
    file = choose_file()
    if file:
        user_pw = simple_input("Enter User password:")
        owner_pw = simple_input("Enter Owner password:")
        out = core.encrypt_pdf(file, user_pw=user_pw, owner_pw=owner_pw)
        messagebox.showinfo("Success", f"Encrypted PDF saved at:\n{out}")


def run_extract_pages():
    file = choose_file()
    if file:
        pages = simple_input("Enter page range to extract (e.g. 1-5):")
        if not pages:
            return
        try:
            start, end = map(int, pages.split("-"))
            out = core.extract_pages(file, start=start, end=end)
            messagebox.showinfo("Success", f"Extracted pages {start}-{end}, saved at:\n{out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def run_extract_images():
    file = choose_file()
    if file:
        page = simple_input("Enter page number to extract image from:")
        try:
            out = core.extract_images(file, page_num=int(page))
            if out:
                messagebox.showinfo("Success", f"Image(s) extracted, saved with prefix:\n{out}")
            else:
                messagebox.showwarning("No Images", "No images found on that page.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def run_compress():
    file = choose_file()
    if file:
        try:
            out, before, after = core.compress_pdf(file)
            before_kb = round(before / 1024, 2)
            after_kb = round(after / 1024, 2)
            messagebox.showinfo(
                "Success",
                f"Compressed PDF saved at:\n{out}\n\n"
                f"Before: {before_kb} KB\nAfter: {after_kb} KB\n"
                f"Reduced: {before_kb - after_kb} KB"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))


def simple_input(prompt):
    """Small popup input box"""
    def on_submit():
        nonlocal value
        value = entry.get()
        popup.destroy()

    value = None
    popup = tk.Toplevel(root)
    popup.title("Input Required")
    tk.Label(popup, text=prompt).pack(pady=5)
    entry = tk.Entry(popup)
    entry.pack(pady=5)
    tk.Button(popup, text="OK", command=on_submit).pack(pady=5)
    popup.grab_set()
    root.wait_window(popup)
    return value


# --------------------
# UI Buttons
# --------------------
tk.Label(root, text=" PDF Editor", font=("Arial", 18, "bold")).pack(pady=15)

btns = [
    ("Reverse PDF", run_reverse),
    ("Delete Pages", run_delete),
    ("Replace Page", run_replace),
    ("Rotate PDF", run_rotate),
    ("Encrypt PDF", run_encrypt),
    ("Extract Pages", run_extract_pages),
    ("Extract Images", run_extract_images),
    ("Compress PDF", run_compress),
]

for text, cmd in btns:
    tk.Button(root, text=text, width=30, command=cmd).pack(pady=5)

tk.Button(root, text="Exit", width=30, command=root.quit, bg="red", fg="white").pack(pady=10)

root.mainloop()
