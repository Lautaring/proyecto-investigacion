import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from logic.Rol import Rol
from logic.Factor import Factor
from logic.Tablero import Tablero
import glob
import os

class AdminGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Administrar Factores")

        self.image_frame = tk.Frame(self.master)
        self.image_frame.pack(side=tk.LEFT)

        self.form_frame = tk.Frame(self.master)
        self.form_frame.pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(self.image_frame, width=600, height=600)
        self.canvas.pack()

        self.tablero = Tablero(self.canvas, 600, 600)

        self.cargar_imagen_button = tk.Button(self.image_frame, text="Cargar Imagen", command=self.cargar_imagen)
        self.cargar_imagen_button.pack()

        self.img = None
        self.image_label = None
        self.factor_name_entry = None
        self.diversity_entry = None
        self.last_img_path = None

        self.image_refs = []

        self.factors_dict = {}

        self.image_paths = self.obtener_rutas_imagen()

    def obtener_rutas_imagen(self):
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        resources_dir = os.path.join(base_dir, 'resources') 
        image_files = glob.glob(os.path.join(resources_dir, 'figure*.png'))

        image_files.sort()

        return image_files

    def cargar_imagen(self):
        try:
            print("image_paths: ", self.image_paths)
            img_path = self.image_paths[0]
            self.last_img_path = img_path
            self.img = cv2.imread(img_path)
            self.mostrar_imagen()
            self.crear_formulario()
        except NameError:
            print("Error: Variable no definida")
        except:
            print("Error al cargar la imagen: No existe el archivo")

    def mostrar_imagen(self):
        img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)

        original_width, original_height = img_pil.size

        new_width = original_width
        new_height = original_height
        img_pil_resized = img_pil.resize((new_width, new_height), Image.LANCZOS)

        img_tk = ImageTk.PhotoImage(image=img_pil_resized)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk

    def crear_formulario(self):
        tk.Label(self.form_frame, text="Nombre del Factor:").grid(row=0, column=0)
        self.factor_name_entry = tk.Entry(self.form_frame)
        self.factor_name_entry.grid(row=0, column=1)

        tk.Label(self.form_frame, text="Diversidad:").grid(row=1, column=0)
        self.diversity_entry = tk.Entry(self.form_frame)
        self.diversity_entry.grid(row=1, column=1)

        tk.Label(self.form_frame, text="Masa Crítica:").grid(row=2, column=0)
        self.masa_critica_entry = tk.Entry(self.form_frame)
        self.masa_critica_entry.grid(row=2, column=1)

        tk.Label(self.form_frame, text="Orden:").grid(row=3, column=0)
        self.orden_entry = tk.Entry(self.form_frame)
        self.orden_entry.grid(row=3, column=1)

        tk.Label(self.form_frame, text="Calidad:").grid(row=4, column=0)
        self.calidad_entry = tk.Entry(self.form_frame)
        self.calidad_entry.grid(row=4, column=1)

        tk.Label(self.form_frame, text="Coeficiente de Crecimiento:").grid(row=5, column=0)
        self.coef_crecimiento_entry = tk.Entry(self.form_frame)
        self.coef_crecimiento_entry.grid(row=5, column=1)

        tk.Label(self.form_frame, text="Coeficiente de Mantenimiento:").grid(row=6, column=0)
        self.coef_mantenimiento_entry = tk.Entry(self.form_frame)
        self.coef_mantenimiento_entry.grid(row=6, column=1)

        tk.Button(self.form_frame, text="Guardar Factor", command=self.guardar_factor).grid(row=7, columnspan=2)

    def guardar_factor(self):
        nombre = self.factor_name_entry.get()
        diversidad = float(self.diversity_entry.get())
        masa_critica = float(self.masa_critica_entry.get())
        orden = float(self.orden_entry.get())
        calidad = float(self.calidad_entry.get())
        coef_crecimiento = float(self.coef_crecimiento_entry.get())
        coef_mantenimiento = float(self.coef_mantenimiento_entry.get())

        factor = Factor(nombre, diversidad, masa_critica, orden, calidad, coef_crecimiento, coef_mantenimiento, None)

        if self.last_img_path: 
            img_path = self.last_img_path

            self.factors_dict[img_path] = factor
            self.guardar_en_archivo(img_path, factor) 
            self.clear_canvas()
            self.limpiar_formulario()

            self.cargar_siguiente_imagen()

    def guardar_en_archivo(self, img_path, factor):
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        database_dir = os.path.join(base_dir, 'Base de datos')
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)

        img_name = os.path.basename(img_path)
        file_name = f"{os.path.splitext(img_name)[0]}.txt"
        file_path = os.path.join(database_dir, file_name)

        with open(file_path, "w") as file:
            file.write(f"Ruta: {img_path}\n")
            file.write(f"Nombre del Factor: {factor.nombre}\n")
            file.write(f"Diversidad: {factor.diversidad}\n")
            file.write(f"Masa Crítica: {factor.masa_critica}\n")
            file.write(f"Orden: {factor.orden}\n")
            file.write(f"Calidad: {factor.calidad}\n")
            file.write(f"Coeficiente de Crecimiento: {factor.coeficiente_crecimiento}\n")
            file.write(f"Coeficiente de Mantenimiento: {factor.coeficiente_mantenimiento}\n")

    def cargar_siguiente_imagen(self):
        current_index = len(self.factors_dict)
        if current_index < len(self.image_paths):
            next_img_path = self.image_paths[current_index]
            self.last_img_path = next_img_path
            self.img = cv2.imread(next_img_path)
            if self.img is not None:
                self.mostrar_imagen()
                self.crear_formulario()
            else:
                print(f"No se pudo cargar la imagen {next_img_path}")
        else:
            print("No hay más imágenes para cargar.")
            self.mostrar_pizarra()

    def limpiar_formulario(self):
        self.factor_name_entry.delete(0, tk.END)
        self.diversity_entry.delete(0, tk.END)
        self.masa_critica_entry.delete(0, tk.END)
        self.orden_entry.delete(0, tk.END)
        self.calidad_entry.delete(0, tk.END)
        self.coef_crecimiento_entry.delete(0, tk.END)
        self.coef_mantenimiento_entry.delete(0, tk.END)

    def clear_canvas(self):
        self.canvas.delete("all")

    def mostrar_pizarra(self):
        self.master.withdraw()

        blank_board_window = tk.Toplevel()
        blank_board_window.title("Tablero en Blanco")
        blank_board_window.geometry("900x900")

        canvas_blank_board = tk.Canvas(blank_board_window, width=600, height=600, bg="white")
        canvas_blank_board.pack()

        self.loaded_images = []

        self.image_ids = []

        self.cargar_y_hacer_arrastrable(canvas_blank_board, self.image_paths[0], 100, 100)
        self.cargar_y_hacer_arrastrable(canvas_blank_board, self.image_paths[1], 300, 300)

        btn_superponer = tk.Button(blank_board_window, text="Superponer", command=lambda: self.superponer_imagenes(canvas_blank_board))
        btn_superponer.pack()

        btn_close = tk.Button(blank_board_window, text="Cerrar", command=lambda: self.cerrar_pizarra_blanca(blank_board_window))
        btn_close.pack()

        blank_board_window.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_pizarra_blanca(blank_board_window))

    def cargar_y_hacer_arrastrable(self, canvas, img_path, x, y):
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)

        image_id = canvas.create_image(x, y, anchor=tk.NW, image=img_tk)
        self.loaded_images.append(img_tk)  # Mantener una referencia a la imagen
        self.image_refs.append(img_tk)  # Mantener una referencia para evitar recolección de basura
        self.image_ids.append(image_id)  # Mantener una referencia al ID de la imagen en el canvas

        def on_drag(event):
            canvas.coords(image_id, event.x, event.y)

        canvas.tag_bind(image_id, "<B1-Motion>", on_drag)

    def superponer_imagenes(self, canvas):
        if len(self.image_paths) < 2:
            print("Hay menos de 2 imágenes, no se puede superponer.")
            return
        
        img_combinada = Image.open(self.image_paths[0]).convert("RGBA")

        for i in range(1, len(self.image_paths)):
            img_aux = Image.open(self.image_paths[i]).convert("RGBA")
            posicion = (100, 100)

            img_combinada.paste(img_aux, posicion, img_aux)

        img_tk = ImageTk.PhotoImage(image=img_combinada)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.image_refs.append(img_tk)

    def cerrar_pizarra_blanca(self, blank_board_window):
        blank_board_window.destroy()
        self.master.destroy()