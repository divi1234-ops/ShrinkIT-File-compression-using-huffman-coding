import tkinter as tk
from tkinter import filedialog, messagebox

# Placeholder for the actual compression logic
# Replace this with ShrinkIT Huffman codec implementation

def compress_file(file_path):
    print(f"Compressing: {file_path}")
    messagebox.showinfo("Compression", f"Compressed: {file_path}")

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        compress_file(file_path)

app = tk.Tk()
app.title("ShrinkIT File Compression")

frame = tk.Frame(app, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Select a file to compress using Huffman Coding:")
label.pack(pady=(0,10))

btn_select = tk.Button(frame, text="Select File", command=select_file)
btn_select.pack()

app.mainloop()