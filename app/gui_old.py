import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from tkinterdnd2 import DND_FILES, TkinterDnD

from app.processor import process_images


image_paths = []
output_folder = ""


def add_images():
    global image_paths

    files = filedialog.askopenfilenames(
        title="Seleccionar imágenes",
        filetypes=[
            ("Imágenes", "*.jpg *.jpeg *.png *.webp *.bmp *.tif *.tiff"),
        ],
    )

    for file in files:
        path = Path(file)

        if path not in image_paths:
            image_paths.append(path)

    refresh_label()


def drop(event):
    global image_paths

    files = root.tk.splitlist(event.data)

    for file in files:
        path = Path(file)

        if path.is_file() and path not in image_paths:
            image_paths.append(path)

    refresh_label()


def refresh_label():
    lbl_images.config(
        text=f"{len(image_paths)} imágenes seleccionadas"
    )


def choose_output():
    global output_folder

    folder = filedialog.askdirectory(
        title="Seleccionar carpeta destino"
    )

    if folder:
        output_folder = folder
        lbl_output.config(text=folder)


def update_progress(current, total):
    progress["maximum"] = total
    progress["value"] = current
    root.update_idletasks()


def process():

    if not image_paths:
        messagebox.showwarning(
            "Aviso",
            "Seleccione al menos una imagen."
        )
        return

    if not output_folder:
        messagebox.showwarning(
            "Aviso",
            "Seleccione una carpeta destino."
        )
        return

    btn_process.config(state="disabled")

    threading.Thread(
        target=worker,
        daemon=True,
    ).start()


def worker():

    try:

        zip_path = process_images(
            image_paths=image_paths,
            output_folder=output_folder,
            progress_callback=update_progress,
        )

        root.after(
            0,
            lambda: messagebox.showinfo(
                "Proceso finalizado",
                f"Archivos generados en:\n\n{zip_path}",
            ),
        )

    except Exception as e:

        root.after(
            0,
            lambda: messagebox.showerror(
                "Error",
                str(e),
            ),
        )

    finally:

        root.after(
            0,
            lambda: btn_process.config(state="normal"),
        )


# ==========================
# Ventana
# ==========================

root = TkinterDnD.Tk()

root.title("Watermark Tool")
root.geometry("700x700")
root.resizable(False, False)

# ==========================
# Zona Drag & Drop
# ==========================

drop_zone = tk.Label(
    root,
    text="Arrastra aquí las imágenes\n\n\no\n\n\nPulsa 'Agregar imágenes'",
    relief="groove",
    width=55,
    height=5,
)

drop_zone.pack(pady=10)

drop_zone.drop_target_register(DND_FILES)
drop_zone.dnd_bind("<<Drop>>", drop)

# ==========================
# Agregar imágenes
# ==========================

tk.Button(
    root,
    text="Agregar imágenes",
    command=add_images,
    width=22,
).pack()

lbl_images = tk.Label(
    root,
    text="0 imágenes seleccionadas",
)

lbl_images.pack(pady=5)

# ==========================
# Destino
# ==========================

tk.Button(
    root,
    text="Seleccionar carpeta destino",
    command=choose_output,
    width=22,
).pack()

lbl_output = tk.Label(
    root,
    text="Ninguna carpeta seleccionada",
    wraplength=500,
)

lbl_output.pack(pady=5)

# ==========================
# Barra de progreso
# ==========================

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    mode="determinate",
    length=450,
)

progress.pack(pady=10)

# ==========================
# Procesar
# ==========================

btn_process = tk.Button(
    root,
    text="Procesar",
    width=22,
    command=process,
)

btn_process.pack(pady=15)

# Enter = Procesar
root.bind("<Return>", lambda event: process())

root.mainloop()