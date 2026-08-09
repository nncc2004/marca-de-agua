
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from app.processor import process_images

image_paths=[]
output_folder=""

def add_images():
    global image_paths
    files=filedialog.askopenfilenames(title="Seleccionar imágenes",
        filetypes=[("Imágenes","*.jpg *.jpeg *.png *.webp *.bmp *.tif *.tiff")])
    for f in files:
        p=Path(f)
        if p not in image_paths:
            image_paths.append(p)
    lbl_images.config(text=f"{len(image_paths)} imágenes seleccionadas")

def choose_output():
    global output_folder
    folder=filedialog.askdirectory(title="Seleccionar carpeta destino")
    if folder:
        output_folder=folder
        lbl_output.config(text=folder)

def update_progress(c,t):
    progress["maximum"]=t
    progress["value"]=c
    root.update_idletasks()

def cancel():
    global image_paths,output_folder
    image_paths.clear()
    output_folder=""
    lbl_images.config(text="0 imágenes seleccionadas")
    lbl_output.config(text="Ninguna carpeta seleccionada")
    progress["value"]=0

def process():
    if not image_paths:
        messagebox.showwarning("Aviso","Seleccione al menos una imagen."); return
    if not output_folder:
        messagebox.showwarning("Aviso","Seleccione una carpeta destino."); return
    btn_generate.config(state="disabled")
    threading.Thread(target=worker,daemon=True).start()

def worker():
    try:
        folder=process_images(image_paths=image_paths,output_folder=output_folder,progress_callback=update_progress)
        root.after(0,lambda:messagebox.showinfo("Proceso finalizado",f"Archivos generados en:\n\n{folder}"))
    except Exception as e:
        root.after(0,lambda:messagebox.showerror("Error",str(e)))
    finally:
        root.after(0,lambda:btn_generate.config(state="normal"))

root=tk.Tk()
root.title("Generador imágenes con marca de agua")
root.geometry("750x530")
root.resizable(False,False)

tk.Label(root,text="Generador marca de agua",font=("Arial",16,"bold")).pack(pady=20)
tk.Button(root,text="Agregar imágenes",width=30,command=add_images).pack()
lbl_images=tk.Label(root,text="0 imágenes seleccionadas"); lbl_images.pack(pady=(5,20))
tk.Button(root,text="Seleccionar ruta",width=30,command=choose_output).pack()
lbl_output=tk.Label(root,text="Ninguna carpeta seleccionada",wraplength=450); lbl_output.pack(pady=(5,20))
progress=ttk.Progressbar(root,orient="horizontal",mode="determinate",length=350); progress.pack(pady=(0,20))
btn_generate=tk.Button(root,text="Generar",width=30,command=process); btn_generate.pack()
tk.Button(root,text="Cancelar",width=30,fg="red",command=cancel).pack(pady=20)
root.bind("<Return>",lambda e:process())
root.mainloop()
