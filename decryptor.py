from cryptography.fernet import Fernet
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog, messagebox

enc_file = Path("data.txt.enc")

def decrypt_file(filename):
    root = tk.Tk()
    root.withdraw()
    key_input = simpledialog.askstring("Decryption", "Enter decryption key:")
    if not key_input:
        messagebox.showerror("Error", "No key provided.")
        return

    try:
        fernet = Fernet(key_input.encode())
        with open(filename, "rb") as file:
            encrypted = file.read()
        decrypted = fernet.decrypt(encrypted)
        with open(filename.with_suffix(".decrypted.txt"), "wb") as dec_file:
            dec_file.write(decrypted)
        messagebox.showinfo("Success", "File decrypted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {e}")

decrypt_file(enc_file)