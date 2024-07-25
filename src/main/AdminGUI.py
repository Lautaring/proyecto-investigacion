import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from logic.Rol import Rol
from logic.Factor import Factor
from logic.Tablero import Tablero
"""from logic.Validacion import Validacion"""
from tkinter import messagebox
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

        pixel_size = 10 
        self.tablero = Tablero(self.canvas, 600 // pixel_size, 600 // pixel_size, pixel_size)


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

        self.ruta_imagen_actual = None


    def obtener_rutas_imagen(self):
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        resources_dir = os.path.join(base_dir, 'resources') 
        image_files = glob.glob(os.path.join(resources_dir, 'figure*.png'))

        image_files.sort()

        return image_files

    def cargar_imagen(self):
        try:
            print("image_paths: ", self.image_paths)
            self.indice_imagen_actual = 0 
            img_path = self.image_paths[self.indice_imagen_actual]
            self.last_img_path = img_path
            self.ruta_imagen_actual = img_path 
            self.img = cv2.imread(img_path)
            if self.img is not None:
                self.mostrar_imagen(self.indice_imagen_actual)  
                self.crear_formulario()
            else:
                print(f"No se pudo cargar la imagen {img_path}")
        except NameError:
            print("Error: Variable no definida")
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")




    def mostrar_imagen(self, indice):
        if indice >= len(self.image_paths):
            print("No hay más imágenes.")
            return

        img_path = self.image_paths[indice]
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)

        if hasattr(self, 'canvas_blank_board'): 
            self.canvas_blank_board.delete("all")
            self.id_imagen_actual = self.canvas_blank_board.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas_blank_board.image = img_tk

            def on_drag(event):
                self.canvas_blank_board.coords(self.id_imagen_actual, event.x, event.y)

            self.canvas_blank_board.tag_bind(self.id_imagen_actual, "<B1-Motion>", on_drag)
        else:
            self.canvas.delete("all")
            self.id_imagen_actual = self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk 





    def crear_formulario(self):
        # Menú desplegable para el tipo de factor
        tk.Label(self.form_frame, text="Tipo de factor: ").grid(row=0, column=0)
        self.tipo_factor_var = tk.StringVar(self.form_frame)
        self.tipo_factor_var.set("Selecciona un tipo")  # Valor por defecto
        tipo_factor_options = ["Fisico", "Simbolico", "Cultural"]
        self.tipo_factor_menu = tk.OptionMenu(self.form_frame, self.tipo_factor_var, *tipo_factor_options)
        self.tipo_factor_menu.grid(row=0, column=1)

        # Menú desplegable para los componentes del factor
        tk.Label(self.form_frame, text="Componente del Factor:").grid(row=1, column=0)
        self.componente_var = tk.StringVar(self.form_frame)
        self.componente_var.set("Selecciona un componente")  # Valor por defecto
        componente_options = [f"Componente {i}" for i in range(1, 11)]
        self.componente_menu = tk.OptionMenu(self.form_frame, self.componente_var, *componente_options)
        self.componente_menu.grid(row=1, column=1)

        # Otros campos del formulario
        tk.Label(self.form_frame, text="Nombre del Factor:").grid(row=2, column=0)
        self.factor_name_entry = tk.Entry(self.form_frame)
        self.factor_name_entry.grid(row=2, column=1)

        tk.Label(self.form_frame, text="Diversidad:").grid(row=3, column=0)
        self.diversity_entry = tk.Entry(self.form_frame)
        self.diversity_entry.grid(row=3, column=1)

        tk.Label(self.form_frame, text="Masa Crítica:").grid(row=4, column=0)
        self.masa_critica_entry = tk.Entry(self.form_frame)
        self.masa_critica_entry.grid(row=4, column=1)

        tk.Label(self.form_frame, text="Orden:").grid(row=5, column=0)
        self.orden_entry = tk.Entry(self.form_frame)
        self.orden_entry.grid(row=5, column=1)

        tk.Label(self.form_frame, text="Calidad:").grid(row=6, column=0)
        self.calidad_entry = tk.Entry(self.form_frame)
        self.calidad_entry.grid(row=6, column=1)

        tk.Label(self.form_frame, text="Coeficiente de Crecimiento:").grid(row=7, column=0)
        self.coef_crecimiento_entry = tk.Entry(self.form_frame)
        self.coef_crecimiento_entry.grid(row=7, column=1)

        tk.Label(self.form_frame, text="Coeficiente de Mantenimiento:").grid(row=8, column=0)
        self.coef_mantenimiento_entry = tk.Entry(self.form_frame)
        self.coef_mantenimiento_entry.grid(row=8, column=1)
        
        # Menú desplegable para los roles del factor
        tk.Label(self.form_frame, text="Tipo de Rol: ").grid(row=9, column=0)
        self.tipo_factor_var = tk.StringVar(self.form_frame)
        self.tipo_factor_var.set("Selecciona un rol")  # Valor por defecto
        tipo_factor_options = ["Gestor", "Transmisor", "Productor"]
        self.tipo_factor_menu = tk.OptionMenu(self.form_frame, self.tipo_factor_var, *tipo_factor_options)
        self.tipo_factor_menu.grid(row=9, column=1)

        tk.Button(self.form_frame, text="Guardar Factor", command=self.guardar_factor).grid(row=10, columnspan=2)

    def guardar_factor(self):
        if not self.validar_campos():
            return
        
        
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
            self.ruta_imagen_actual = next_img_path 
            self.img = cv2.imread(next_img_path)
            if self.img is not None:
                self.mostrar_imagen(current_index)
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

        self.blank_board_window = tk.Toplevel()
        self.blank_board_window.title("Tablero en Blanco")
        self.blank_board_window.geometry("900x900")

        self.canvas_blank_board = tk.Canvas(self.blank_board_window, width=600, height=600, bg="white")
        self.canvas_blank_board.pack()

        self.indice_imagen_actual = 0
        self.mostrar_imagen(self.indice_imagen_actual)

        self.btn_confirmar = tk.Button(self.blank_board_window, text="Confirmar", command=self.confirmar_ubicacion)
        self.btn_confirmar.pack()

        self.btn_cerrar = tk.Button(self.blank_board_window, text="Cerrar", command=self.cerrar_pizarra_blanca)
        self.btn_cerrar.pack()

        self.blank_board_window.protocol("WM_DELETE_WINDOW", self.cerrar_pizarra_blanca)


    def confirmar_ubicacion(self):
        x, y = self.canvas_blank_board.coords(self.id_imagen_actual)
        print(f"Imagen {self.ruta_imagen_actual} ubicada en: ({x}, {y})")
        
        self.indice_imagen_actual += 1
        if self.indice_imagen_actual < len(self.image_paths):
            self.mostrar_imagen(self.indice_imagen_actual)
        else:
            print("Has terminado de ubicar todas las imágenes.")
            self.cerrar_pizarra_blanca()


    def cargar_y_hacer_arrastrable(self, canvas, img_path, x, y):
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)

        image_id = canvas.create_image(x, y, anchor=tk.NW, image=img_tk)
        self.loaded_images.append(img_tk)
        self.image_refs.append(img_tk)
        self.image_ids.append(image_id)

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
            posicion = (0, 0)

            img_combinada.paste(img_aux, posicion, img_aux)

        img_tk = ImageTk.PhotoImage(image=img_combinada)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.image_refs.append(img_tk)

    def cerrar_pizarra_blanca(self):
        self.blank_board_window.destroy()
        self.master.deiconify() 

    """Valida que el valor sea un string no vacío"""

    def validar_campos(self):
        """Valida que todos los campos del formulario estén llenos y que los valores sean correctos."""
        # Obtener los valores de los campos
        nombre = self.factor_name_entry.get().strip()
        diversidad = self.diversity_entry.get().strip()
        masa_critica = self.masa_critica_entry.get().strip()
        orden = self.orden_entry.get().strip()
        calidad = self.calidad_entry.get().strip()
        coef_crecimiento = self.coef_crecimiento_entry.get().strip()
        coef_mantenimiento = self.coef_mantenimiento_entry.get().strip()

        # Verificar que ninguno de los campos esté vacío
        if not nombre:
            messagebox.showerror("Error", "El nombre del factor no puede estar vacío.")
            return False
        if not diversidad:
            messagebox.showerror("Error", "La diversidad no puede estar vacía.")
            return False
        if not masa_critica:
            messagebox.showerror("Error", "La masa crítica no puede estar vacía.")
            return False
        if not orden:
            messagebox.showerror("Error", "El orden no puede estar vacío.")
            return False
        if not calidad:
            messagebox.showerror("Error", "La calidad no puede estar vacía.")
            return False
        if not coef_crecimiento:
            messagebox.showerror("Error", "El coeficiente de crecimiento no puede estar vacío.")
            return False
        if not coef_mantenimiento:
            messagebox.showerror("Error", "El coeficiente de mantenimiento no puede estar vacío.")
            return False

        # Verificar que los valores numéricos sean válidos
        try:
            float(diversidad)
            float(masa_critica)
            float(orden)
            float(calidad)
            float(coef_crecimiento)
            float(coef_mantenimiento)
        except ValueError:
            messagebox.showerror("Error", "Todos los valores numéricos deben ser válidos.")
            return False

        return True