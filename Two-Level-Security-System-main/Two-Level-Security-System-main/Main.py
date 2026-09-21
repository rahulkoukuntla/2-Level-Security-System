from tkinter import Tk, messagebox, filedialog
import customtkinter as ctk
from Encryption import encrypt_folder, decrypt_folder, locked_files
from Database import setup_database, add_user, remove_user, fetch_all_users, validate_barcode
from Barcode_Email import generate_barcode, send_email_with_barcode, send_alert_email, send_otp_email
from FaceRecognitionUtils import scan_barcode, scan_face, validate_face
import cv2
import random
from cryptography.fernet import Fernet
import numpy as np
import threading
from MesaSimulation import *


class SecuritySystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Two-Level Security System")
        self.root.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.conn = setup_database()
        self.encryption_key = Fernet.generate_key()
        
        self.barcode_var = ctk.StringVar()
        self.email_var = ctk.StringVar()

        ctk.CTkLabel(root, text="Enter Barcode:", font=("Arial", 14)).pack(pady=10)
        ctk.CTkEntry(root, textvariable=self.barcode_var).pack(pady=10)
        ctk.CTkLabel(root, text="Enter Email:", font=("Arial", 14)).pack(pady=10)
        ctk.CTkEntry(root, textvariable=self.email_var).pack(pady=10)

        ctk.CTkButton(root, text="Add User", command=self.add_user).pack(pady=10)
        ctk.CTkButton(root, text="Remove User", command=self.remove_user).pack(pady=10)
        ctk.CTkButton(root, text="Authenticate & Unlock", command=self.authenticate).pack(pady=10)
        ctk.CTkButton(root, text="Secure File/Folder", command=self.secure_file_folder).pack(pady=10)
        ctk.CTkButton(root, text="Show Locked Files", command=self.show_locked_files).pack(pady=10)
        ctk.CTkButton(root, text="Show User Count", command=self.show_user_count).pack(pady=10)
        ctk.CTkButton(root, text="Quit", command=root.quit).pack(pady=20)

        ctk.CTkButton(root, text="Run Simulation", command=self.run_simulation).pack(pady=20)

    def run_simulation(self):
        simulation_thread = threading.Thread(target=self.simulation)
        simulation_thread.start()
        
    def simulation(self):
        server.port = 8530
        server.launch()
        self.reopen_gui()

    def reopen_gui(self):
        self.root.after(100, self.root.deiconify)

    def add_user(self):
        barcode = self.barcode_var.get()
        email = self.email_var.get()
        if not barcode or not email:
            messagebox.showerror("Error", "Please enter a barcode and email!")
            return

        otp = str(random.randint(100000, 999999))
        if not send_otp_email(email, otp):
            messagebox.showerror("Error", "Failed to send OTP. Please try again.")
            return

        user_otp = ctk.CTkInputDialog(text="Enter the OTP sent to your email:", title="OTP Verification").get_input()
        if user_otp != otp:
            messagebox.showerror("Error", "Invalid OTP!")
            return

        video_capture = cv2.VideoCapture(0)
        messagebox.showinfo("Info", "Look at the camera to register your face.")

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            face_encoding = scan_face(frame)
            if face_encoding is not None:
                if add_user(self.conn, barcode, face_encoding):
                    barcode_file = f"{barcode}.png"
                    file_path = generate_barcode(barcode, barcode_file)
                    send_email_with_barcode(email, file_path)
                    messagebox.showinfo("Success", f"User added successfully!\nBarcode sent to {email}")
                else:
                    messagebox.showerror("Error", "Barcode already exists!")
                break

        video_capture.release()
        cv2.destroyAllWindows()

    def authenticate(self):
        video_capture = cv2.VideoCapture(0)
        messagebox.showinfo("Info", "Show your barcode to the camera.")

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            scanned_barcode = scan_barcode(frame)
            if scanned_barcode:
                user = validate_barcode(self.conn, scanned_barcode)
                if not user:
                    users = fetch_all_users(self.conn)
                    send_alert_email(registed_email="rushyashrungan05@gmail.com")
                    messagebox.showerror("Error", "Invalid barcode! Alert email sent.")
                    break

                known_face_encoding = np.frombuffer(user[2], dtype=np.float64)
                messagebox.showinfo("Info", "Look at the camera to verify your face.")

                while True:
                    ret, frame = video_capture.read()
                    if not ret:
                        break

                    captured_face_encoding = scan_face(frame)
                    if captured_face_encoding is not None:
                        if validate_face(known_face_encoding, captured_face_encoding):
                            folder_path = filedialog.askdirectory(title="Select a folder to unlock")
                            decrypt_folder(folder_path, self.encryption_key)
                            messagebox.showinfo("Success", "Access granted and folder unlocked!")
                        else:
                            messagebox.showerror("Error", "Face verification failed!")
                        break
                break

        video_capture.release()
        cv2.destroyAllWindows()

    def secure_file_folder(self):
        folder_path = filedialog.askdirectory(title="Select a folder to secure")
        if folder_path:
            encrypt_folder(folder_path, self.encryption_key)
            messagebox.showinfo("Success", "Folder secured!")

    def show_locked_files(self):
        if locked_files:
            messagebox.showinfo("Locked Files", "\n".join(locked_files))
        else:
            messagebox.showinfo("Locked Files", "No files are currently locked.")

    def show_user_count(self):
        users = fetch_all_users(self.conn)
        user_count = len(users)
        if user_count == 0:
            messagebox.showinfo("user Count", "No user registered yet.")
        else:
            messagebox.showinfo("User Count", f"Total users: {user_count}")

    def remove_user(self):
        
        barcode = self.barcode_var.get()
        if not barcode:
            messagebox.showerror("Error", "Please enter a barcode to remove!")
            return

        if remove_user(self.conn, barcode):
            messagebox.showinfo("Success", f"User with barcode {barcode} removed successfully!")
        else:
            messagebox.showerror("Error", f"User with barcode {barcode} not found!")


# --- Main Application ---
if __name__ == "__main__":
    root = ctk.CTk()
    app = SecuritySystemGUI(root)
    root.mainloop()
