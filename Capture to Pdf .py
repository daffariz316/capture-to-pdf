import cv2
import os
from tkinter import Tk, Label, Button, messagebox
from fpdf import FPDF
from PIL import Image

# Folder untuk menyimpan hasil capture
OUTPUT_FOLDER = "captured_documents"
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def capture_image():
    cap = cv2.VideoCapture(0)  # Membuka kamera (0 untuk kamera bawaan)
    
    if not cap.isOpened():
        messagebox.showerror("Error", "Failed to access the camera. Make sure the camera is connected.")
        return

    cv2.namedWindow("Press SPACE to capture, ESC to exit")
    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to read from the camera.")
            break

        cv2.imshow("Press SPACE to capture, ESC to exit", frame)
        key = cv2.waitKey(1)

        if key == 27:  # ESC untuk keluar
            break
        elif key == 32:  # SPACE untuk capture
            file_path = os.path.join(OUTPUT_FOLDER, "captured_image.jpg")
            cv2.imwrite(file_path, frame)
            messagebox.showinfo("Success", f"Image captured and saved to: {file_path}")
            cap.release()
            cv2.destroyAllWindows()
            return file_path

    cap.release()
    cv2.destroyAllWindows()

def save_as_pdf(image_path):
    try:
        img = Image.open(image_path)
        pdf = FPDF()
        pdf.add_page()
        img.save("temp_image.jpg")  # Simpan sebagai file sementara
        pdf.image("temp_image.jpg", x=10, y=10, w=190)
        pdf_file = os.path.join(OUTPUT_FOLDER, "captured_document.pdf")
        pdf.output(pdf_file)
        os.remove("temp_image.jpg")  # Hapus file sementara
        messagebox.showinfo("Success", f"PDF saved to: {pdf_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save as PDF: {e}")

def capture_and_convert():
    image_path = capture_image()
    if image_path:
        save_as_pdf(image_path)

# GUI Setup
root = Tk()
root.title("Capture to PDF")

Label(root, text="Capture Image and Save as PDF").pack(pady=10)
Button(root, text="Capture and Save", command=capture_and_convert).pack(pady=10)

root.mainloop()
