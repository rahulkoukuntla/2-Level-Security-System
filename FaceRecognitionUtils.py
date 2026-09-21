import cv2
import face_recognition
import numpy as np

def scan_barcode(frame):
    from pyzbar.pyzbar import decode
    try:
        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            return barcode_data
    except Exception as e:
        print(f"Error decoding barcode: {e}")
    return None

def scan_face(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    if face_encodings:
        return face_encodings[0]
    return None

def validate_face(known_face_encoding, captured_face_encoding):
    results = face_recognition.compare_faces([known_face_encoding], captured_face_encoding)
    return results[0]
