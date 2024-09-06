import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from logic.Rol import Rol
from logic.Factor import Factor
from logic.Tablero import Tablero
from logic.Validacion import Validacion
from logic.Permeabilidad import Permeabilidad
from tkinter import messagebox
import glob
import os

class AdminGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Administrar Factores")

        # Crear frames para la imagen y el formulario
        self.image_frame = tk.Frame(self.master)
        self.image_frame.pack(side=tk.LEFT)

        self.form_frame = tk.Frame(self.master)
        self.form_frame.pack(side=tk.RIGHT)

        # Crear canvas para mostrar la imagen
        self.canvas = tk.Canvas(self.image_frame, width=600, height=600)
        self.canvas.pack()

        # Inicializar Tablero
        pixel_size = 10
        self.tablero = Tablero(self.canvas, 600 // pixel_size, 600 // pixel_size, pixel_size)

        # Botón para cargar imagen
        self.cargar_imagen_button = tk.Button(self.image_frame, text="Cargar Imagen", command=self.cargar_imagen)
        self.cargar_imagen_button.pack()

        self.img = None
        self.image_label = None
        self.factor_name_entry = None
        self.diversity_entry = None
        self.last_img_path = None

        # Almacenar referencias de imágenes y sus IDs
        self.image_refs = []
        self.image_ids = []

        # Diccionario para almacenar factores asociados a las imágenes
        self.factors_dict = {}
        self.image_paths = self.obtener_rutas_imagen()
        self.ruta_imagen_actual = None
        self.indice_imagen_actual = 0  # Inicialización correcta del índice
        
        self.validacion = Validacion() 

    def obtener_rutas_imagen(self):
        # Obtener rutas de imágenes en el directorio "resources"
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
        self.tipo_factor_var.set("Fisico")  # Valor por defecto
        tipo_factor_options = ["Fisico", "Simbolico", "Cultural"]
        self.tipo_factor_menu = tk.OptionMenu(self.form_frame, self.tipo_factor_var, *tipo_factor_options)
        self.tipo_factor_menu.grid(row=0, column=1)

        # Menú desplegable para los componentes del factor
        tk.Label(self.form_frame, text="Componente del Factor:").grid(row=1, column=0)
        self.componente_var = tk.StringVar(self.form_frame)
        self.componente_var.set("Componente 1")  # Valor por defecto
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
        self.tipo_rol_var = tk.StringVar(self.form_frame)
        self.tipo_rol_var.set("Gestor")  # Valor por defecto
        tipo_rol_options = ["Gestor", "Transmisor", "Productor"]
        self.tipo_rol_menu = tk.OptionMenu(self.form_frame, self.tipo_rol_var, *tipo_rol_options)
        self.tipo_rol_menu.grid(row=9, column=1)
        
        # Permeabilidad
        tk.Label(self.form_frame, text="Tipo de Permeabilidad: ").grid(row=10, column=0)
        self.tipo_permeabilidad_var = tk.StringVar(self.form_frame)
        self.tipo_permeabilidad_var.set("Cerrado")  # Valor por defecto
        tipo_permeabilidad_options = ["Cerrado", "Abierto"]
        self.tipo_permeabilidad_menu = tk.OptionMenu(self.form_frame, self.tipo_permeabilidad_var, *tipo_permeabilidad_options)
        self.tipo_permeabilidad_menu.grid(row=10, column=1)

        tk.Button(self.form_frame, text="Guardar Factor", command=self.guardar_factor).grid(row=11, columnspan=2)

    def guardar_factor(self):
        try:
            # Capturar los valores del formulario
            nombre = self.factor_name_entry.get()
            diversidad = self.diversity_entry.get()
            masa_critica = self.masa_critica_entry.get()
            orden = self.orden_entry.get()
            calidad = self.calidad_entry.get()
            coef_crecimiento = self.coef_crecimiento_entry.get()
            coef_mantenimiento = self.coef_mantenimiento_entry.get()

            # Crear instancia de la clase Validacion
            validacion = Validacion()

            # Validar los campos utilizando la clase Validacion
            if validacion.validar_campos(nombre, diversidad, masa_critica, orden, calidad, coef_crecimiento, coef_mantenimiento):
                # Convertir los valores a float si la validación fue exitosa
                diversidad = float(diversidad)
                masa_critica = float(masa_critica)
                orden = float(orden)
                calidad = float(calidad)
                coef_crecimiento = float(coef_crecimiento)
                coef_mantenimiento = float(coef_mantenimiento)

                # Crear el objeto Factor y guardarlo
                factor = Factor(nombre, diversidad, masa_critica, orden, calidad, Permeabilidad(self.tipo_permeabilidad_var.get(), 1),
                                coef_crecimiento, coef_mantenimiento, Rol(self.tipo_rol_var.get(), "Descripción"))
                self.factors_dict[self.last_img_path] = factor
                self.guardar_en_archivo(self.last_img_path, factor)

                # Limpiar formulario y cargar la siguiente imagen
                self.limpiar_formulario()
                self.cargar_siguiente_imagen()
        except ValueError as e:
            print(f"Error de validación: {e}")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            print(f"Error al guardar el factor: {e}")
            messagebox.showerror("Error", "Ocurrió un error al guardar el factor.")
        

    def guardar_en_archivo(self, img_path, factor):
        # Directorio para guardar archivos
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        database_dir = os.path.join(base_dir, 'database') 

        if not os.path.exists(database_dir):
            os.makedirs(database_dir)

        file_name = os.path.splitext(os.path.basename(img_path))[0] + ".txt"
        file_path = os.path.join(database_dir, file_name)
        
        with open(file_path, "w") as file:
            file.write(f"Imagen: {img_path}\n")
            file.write(f"Nombre: {factor.nombre}\n")
            file.write(f"Diversidad: {factor.diversidad}\n")
            file.write(f"Masa Crítica: {factor.masa_critica}\n")
            file.write(f"Orden: {factor.orden}\n")
            file.write(f"Calidad: {factor.calidad}\n")
            file.write(f"Coeficiente de Crecimiento: {factor.coef_crecimiento}\n")
            file.write(f"Coeficiente de Mantenimiento: {factor.coef_mantenimiento}\n")

    def limpiar_formulario(self):
        self.factor_name_entry.delete(0, tk.END)
        self.diversity_entry.delete(0, tk.END)
        self.masa_critica_entry.delete(0, tk.END)
        self.orden_entry.delete(0, tk.END)
        self.calidad_entry.delete(0, tk.END)
        self.coef_crecimiento_entry.delete(0, tk.END)
        self.coef_mantenimiento_entry.delete(0, tk.END)

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
            # self.cerrar_pizarra_blanca()
            self.btn_confirmar.pack()
            self.cargar_tablero()

    def cargar_tablero(self):
        # Iterar sobre las imágenes cargadas y guardarlas en el tablero
        for img_path, factor in self.factors_dict.items():
            # Supongamos que ya se tiene la posición de la imagen en el tablero (x, y)
            x, y = self.canvas_blank_board.coords(self.image_ids[self.image_paths.index(img_path)])
            fila = int(y // self.tablero.pixel_size)
            columna = int(x // self.tablero.pixel_size)

            color = "#%02x%02x%02x" % (int(255 * factor.diversidad), int(255 * factor.calidad), int(255 * factor.orden))
            
            self.tablero.agregar_celda(fila, columna, color)

        self.tablero.dibujar_tablero()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        tablero_file = os.path.join(base_dir, 'tablero_guardado.txt')
        self.tablero.guardar_tablero(tablero_file)

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

            img_combinada.paste(img_aux, img_aux)

        img_tk = ImageTk.PhotoImage(image=img_combinada)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.image_refs.append(img_tk)

    def cerrar_pizarra_blanca(self):
        self.blank_board_window.destroy()
        self.master.deiconify() 
