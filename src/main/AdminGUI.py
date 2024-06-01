import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from logic.Rol import Rol
from logic.Factor import Factor
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

        self.canvas = tk.Canvas(self.image_frame, width=400, height=400)
        self.canvas.pack()

        self.load_image_button = tk.Button(self.image_frame, text="Cargar Imagen", command=self.load_image)
        self.load_image_button.pack()

        self.img = None
        self.image_label = None
        self.factor_name_entry = None
        self.diversity_entry = None
        self.last_img_path = None

        # Inicializar el diccionario para almacenar los factores
        self.factors_dict = {}

    #Obtener las rutas relativas de la imagen y guardarlas en una lista de paths para luego utilizarlas
    # Obtener la lista de rutas de las imágenes
        self.image_paths = self.get_image_paths()

    def get_image_paths(self):
        # Buscar todos los archivos que coincidan con el patrón 'figureX.png' en la subcarpeta resources
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene el directorio del script actual
        resources_dir = os.path.join(base_dir, 'resources')  # Directorio de la subcarpeta resources
        image_files = glob.glob(os.path.join(resources_dir, 'figure*.png'))

        # Ordenar los archivos por nombre para asegurar el orden correcto
        image_files.sort()

        return image_files
    """    def load_image(self):
        img_path = filedialog.askopenfilename()  # Esto me deja elegir archivos
        if img_path:  # Si se seleccionó algo entonces
            self.last_img_path = img_path  # Almacena la ruta de la imagen cargada
            self.img = cv2.imread(img_path)
            if self.img is not None:
                self.show_image()
                self.create_form()
            else:
                print(f"No se pudo cargar la imagen {img_path}")"""

    #Carga de imagenes automática
    def load_image(self):
        try: 
            print("image_paths: ", self.image_paths)
            img_path = self.image_paths[0]
            #img_path = "D:\\MEGA\\MEGAsyncUploads\\IngenieriaEnInformatica\\CursadoDeLaCarrera\\ProyectoDeInvestigacion\\src\\main\\resources\\figure_1.png"
            self.last_img_path = img_path
            self.img = cv2.imread(img_path)
            self.show_image()
            self.create_form()
        except NameError:
            print("Error: Variable no definida")
        except:
            print("Error al cargar la imagen: No existe el archivo")


    def show_image(self):
        img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)

        # obtener las dimensiones de la window
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()

        # Obtener las dimensiones originales de la imagen
        original_width, original_height = img_pil.size

        # factor de escala
        width_ratio = window_width / original_width
        height_ratio = window_height / original_height
        scale_factor = min(width_ratio, height_ratio)

        # redimensiono la imagen utilizando el factor de escala
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        img_pil_resized = img_pil.resize((new_width, new_height), Image.LANCZOS)

        # ajustamos el lienzo con respecto a la ventana (verlo bien)
        self.canvas.config(width=window_width, height=window_height)

        img_tk = ImageTk.PhotoImage(image=img_pil_resized)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk

    def create_form(self):
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

        tk.Button(self.form_frame, text="Guardar Factor", command=self.save_factor).grid(row=7, columnspan=2)

    def save_factor(self):
        nombre = self.factor_name_entry.get()
        diversidad = float(self.diversity_entry.get())
        masa_critica = float(self.masa_critica_entry.get())
        orden = float(self.orden_entry.get())
        calidad = float(self.calidad_entry.get())
        coef_crecimiento = float(self.coef_crecimiento_entry.get())
        coef_mantenimiento = float(self.coef_mantenimiento_entry.get())

        # Crear un objeto Factor con las propiedades ingresadas
        factor = Factor(nombre, diversidad, masa_critica, orden, calidad, coef_crecimiento, coef_mantenimiento, None)

        if self.last_img_path:  # Verificar si se cargó una imagen previamente
            # Obtener la ruta de la imagen cargada
            img_path = self.last_img_path

            # Me guardo el factor junto con la imagen en el diccionario
            self.factors_dict[img_path] = factor
            self.clear_canvas()
            self.clear_form()

            # Cargar la siguiente imagen y mostrarla
            self.load_next_image()

    #Sirve para la carga de imagenes automática
    def load_next_image(self):
        current_index = len(self.factors_dict)  # Índice de la imagen actual
        if current_index < len(self.image_paths):
            next_img_path = self.image_paths[current_index]
            self.last_img_path = next_img_path
            self.img = cv2.imread(next_img_path)
            if self.img is not None:
                self.show_image()
                self.create_form()
            else:
                print(f"No se pudo cargar la imagen {next_img_path}")
        else:
            print("No hay más imágenes para cargar.") 

    def clear_form(self):
        # Borra los valores de todos los campos del formulario
        self.factor_name_entry.delete(0, tk.END)
        self.diversity_entry.delete(0, tk.END)
        self.masa_critica_entry.delete(0, tk.END)
        self.orden_entry.delete(0, tk.END)
        self.calidad_entry.delete(0, tk.END)
        self.coef_crecimiento_entry.delete(0, tk.END)
        self.coef_mantenimiento_entry.delete(0, tk.END)

    def clear_canvas(self):
        self.canvas.delete("all")
