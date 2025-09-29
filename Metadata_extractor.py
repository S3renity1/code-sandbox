import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
from dataclasses import dataclass
from typing import Iterator
from PIL import Image, ExifTags
from PyPDF2 import PdfReader

@dataclass
class MetadataItem:
    key: str
    value: str

def extract_exif(path: Path) -> Iterator[MetadataItem]:
    try:
        image = Image.open(path)
        exif = image._getexif() or {}
        for tag_id, value in exif.items():
            tag = ExifTags.TAGS.get(tag_id, str(tag_id))
            yield MetadataItem(tag, str(value))
    except Exception as e:
        yield MetadataItem("EXIF Error", str(e))

def extract_pdf(path: Path) -> Iterator[MetadataItem]:
    try:
        reader = PdfReader(path)
        meta = reader.metadata or {}
        for key, value in meta.items():
            clean_key = key.strip('/') if isinstance(key, str) else str(key)
            yield MetadataItem(clean_key, str(value))
    except Exception as e:
        yield MetadataItem("PDF Error", str(e))

def extract_metadata(path: Path) -> Iterator[MetadataItem]:
    suffix = path.suffix.lower()
    if suffix in {'.jpg', '.jpeg', '.tiff'}:
        yield from extract_exif(path)
    elif suffix == '.pdf':
        yield from extract_pdf(path)
    else:
        yield MetadataItem("Unsupported File Type", suffix)

def browse_file():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("PDF and Images", "*.pdf *.jpg *.jpeg *.tiff")]
    )
    if not file_path:
        return

    path = Path(file_path)
    output.delete(1.0, tk.END)

    if not path.exists():
        messagebox.showerror("Error", f"File not found:\n{path}")
        return

    for item in extract_metadata(path):
        output.insert(tk.END, f"{item.key:25}: {item.value}\n")

root = tk.Tk()
root.title("Metadata Extractor")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

btn = tk.Button(frame, text="Select File", command=browse_file)
btn.pack(pady=5)

output = scrolledtext.ScrolledText(frame, width=80, height=20)
output.pack()

root.mainloop()