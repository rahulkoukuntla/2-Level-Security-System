import os
from cryptography.fernet import Fernet
from tkinter import messagebox

locked_files = []

def encrypt_folder(folder_path, key):
    global locked_files
    key_file = os.path.join(folder_path, "encryption_key.key")
    with open(key_file, 'wb') as f:
        f.write(key)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                data = f.read()
            encrypted_data = Fernet(key).encrypt(data)
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            global locked_files
            locked_files.append(file_path)

def decrypt_folder(folder_path, key=None):
    key_file = os.path.join(folder_path, "encryption_key.key")
    if not key and os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            key = f.read()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file == "encryption_key.key":
                continue
            with open(file_path, 'rb') as f:
                data = f.read()
            decrypted_data = Fernet(key).decrypt(data)
            with open(file_path, 'wb') as f:
                f.write(decrypted_data)

def show_locked_files(self):
    if not locked_files:  # Check if locked_files is empty
        messagebox.showinfo("Locked Files", "No files are currently locked.")
    else:
        # Show locked files with better formatting
        locked_files_list = "\n".join(locked_files)
        messagebox.showinfo("Locked Files", f"Locked Files:\n{locked_files_list}")