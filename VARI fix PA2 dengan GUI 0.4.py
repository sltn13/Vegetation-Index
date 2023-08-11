import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

# Variabel global untuk menyimpan path file gambar
image_path = None

def calculate_vari(image_path, vmin, vmax):
    # Load gambar
    image = Image.open(image_path)

    # Konversi gambar ke array NumPy
    image_array = np.array(image)

    # Ekstrak nilai piksel untuk setiap band warna
    blue_band = image_array[:, :, 2].astype(float)
    green_band = image_array[:, :, 1].astype(float)
    red_band = image_array[:, :, 0].astype(float)

    # Hitung VARI
    vari = np.divide((green_band - red_band), (green_band + red_band - blue_band),
                     out=np.zeros_like(blue_band), where=(green_band + red_band - blue_band) != 0)

    return vari

def open_image():
    global image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tif")])
    if file_path:
        image_path = file_path
        image_to_process = Image.open(file_path)
        image_to_process.thumbnail((400, 400))  # Resize gambar untuk menyesuaikan tampilan GUI
        img_tk = ImageTk.PhotoImage(image_to_process)
        original_image_label.configure(image=img_tk)
        original_image_label.image = img_tk  # Menyimpan referensi agar gambar tidak hilang saat diupdate

def process_image():
    if image_path is None:
        return

    vmin = float(vmin_textbox.get())
    vmax = float(vmax_textbox.get())

    vari = calculate_vari(image_path, vmin, vmax)

    # Menampilkan gambar VARI yang telah diproses
    processed_image_label.configure(image='')
    plt.clf()
    plt.imshow(vari, cmap='RdYlGn', vmin=vmin, vmax=vmax)
    plt.title('Vegetation Atmospheric Resistant Index (VARI)')
    plt.axis('off')

    # Mengkonversi plot menjadi gambar dan menampilkannya di GUI
    fig = plt.gcf()
    fig.set_size_inches(4, 4)  # Ukuran gambar yang diproses
    fig.canvas.draw()
    var_img = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
    var_img.thumbnail((400, 400))  # Resize gambar untuk menyesuaikan tampilan GUI
    var_img_tk = ImageTk.PhotoImage(var_img)
    processed_image_label.configure(image=var_img_tk)
    processed_image_label.image = var_img_tk  # Menyimpan referensi agar gambar tidak hilang saat diupdate

def save_image():
    if image_path is None:
        return

    file_types = [('JPEG', '*.jpg'), ('PNG', '*.png'), ('Bitmap', '*.bmp'), ('TIFF', '*.tif')]
    save_path = filedialog.asksaveasfilename(filetypes=file_types, defaultextension='.jpg')
    if save_path:
        vmin = float(vmin_textbox.get())
        vmax = float(vmax_textbox.get())

        vari = calculate_vari(image_path, vmin, vmax)

       # Menampilkan gambar VARI yang telah diproses
        plt.clf()
        plt.imshow(vari, cmap='RdYlGn', vmin=vmin, vmax=vmax)
        plt.axis('off')

        # Mengatur ukuran gambar sesuai dengan konten aktual gambar
        plt.gca().set_aspect('equal', adjustable='box')
        plt.tight_layout(pad=0)

        # Menghapus area kosong di sekitar gambar
        fig = plt.gcf()
        fig.savefig(save_path, dpi=600, bbox_inches='tight', pad_inches=0)
        fig.set_size_inches(4, 4)  # Ukuran gambar yang diproses
        plt.close(fig)  # Menutup gambar yang telah disimpan

def reset_image():
    global image_path
    image_path = None
    original_image_label.configure(image='')
    processed_image_label.configure(image='')

root = tk.Tk()
root.title('VARI Processing')

# Frame untuk kontrol
control_frame = tk.Frame(root)
control_frame.pack(padx=10, pady=10)

# Tombol 'Open' untuk membuka gambar
open_button = tk.Button(control_frame, text='Open', command=open_image)
open_button.grid(row=0, column=0, padx=5, pady=5)

# Tombol 'Process' untuk memproses gambar
process_button = tk.Button(control_frame, text='Process', command=process_image)
process_button.grid(row=0, column=1, padx=5, pady=5)

# Tombol 'Save As' untuk menyimpan gambar yang telah diproses
save_button = tk.Button(control_frame, text='Save As', command=save_image)
save_button.grid(row=0, column=2, padx=5, pady=5)

# Tombol 'Reset' untuk mereset gambar
reset_button = tk.Button(control_frame, text='Reset', command=reset_image)
reset_button.grid(row=0, column=3, padx=5, pady=5)

# TextBox untuk vmin
vmin_label = tk.Label(control_frame, text='Vmin:')
vmin_label.grid(row=1, column=0, padx=5, pady=5)
vmin_textbox = tk.Entry(control_frame, width=5)
vmin_textbox.insert(tk.END, '-1')
vmin_textbox.grid(row=1, column=1, padx=5, pady=5)

# TextBox untuk vmax
vmax_label = tk.Label(control_frame, text='Vmax:')
vmax_label.grid(row=1, column=2, padx=5, pady=5)
vmax_textbox = tk.Entry(control_frame, width=5)
vmax_textbox.insert(tk.END, '1')
vmax_textbox.grid(row=1, column=3, padx=5, pady=5)

# Frame untuk gambar asli
original_frame = tk.Frame(root)
original_frame.pack(padx=10, pady=10, side=tk.LEFT)

# Frame untuk gambar yang diproses
processed_frame = tk.Frame(root)
processed_frame.pack(padx=10, pady=10, side=tk.RIGHT)

# Label untuk gambar asli
original_image_label = tk.Label(original_frame)
original_image_label.pack()

# Label untuk gambar yang diproses
processed_image_label = tk.Label(processed_frame)
processed_image_label.pack()

# Label untuk gambar yang diproses
processed_image_label = tk.Label(processed_frame)
processed_image_label.pack()

# Membuat plot yang tidak terlihat untuk menghasilkan gambar VARI
fig, ax = plt.subplots()
plt.axis('off')

root.mainloop()
