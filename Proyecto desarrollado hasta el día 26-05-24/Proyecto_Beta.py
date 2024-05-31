import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
#from your_classes_file import Factor, Rol  # Importa las clases Factor y Rol desde tu archivo

#_____________________________________________________________________________________________________________________________________________
class Rol:
    def __init__(self, nombre, peso_influencia):
        self.nombre = nombre
        self.peso_influencia = peso_influencia
    
    def Get_nombre(self):
        return self.nombre
    
    def Get_peso_influencia(self):
        return self.peso_influencia


#_____________________________________________________________________________________________________________________________________________

class Permeabilidad:
    def __init__(self, Tipo, valor):
        self.tipo = Tipo
        self.valor = valor

    def Get_tipo(self):
        return self.tipo
    
    def Get_valor(self):
        return self.valor
    
#_____________________________________________________________________________________________________________________________________________

class Vinculo:
    def __init__(self, Tipo, valor):
        self.tipo = Tipo
        self.valor = valor

    def Get_tipo(self):
        return self.tipo
    
    def Get_valor(self):
        return self.valor


#_____________________________________________________________________________________________________________________________________________

class Factor:
    def __init__(self, nombre, diversidad, masa_critica, orden, calidad, coeficiente_crecimiento, coeficiente_mantenimiento, rol_1 : Rol):
        self.nombre = nombre
        self.diversidad = diversidad
        self.masa_critica = masa_critica
        self.orden = orden
        self.calidad = calidad
        self.coeficiente_crecimiento = coeficiente_crecimiento
        self.coeficiente_mantenimiento = coeficiente_mantenimiento
        self.rol = rol_1


#_____________________________________________________________________________________________________________________________________________

class Relacion:
    def __init__(self, factor_1 : Factor, permeabilidad_1 : Permeabilidad, vinculo_1 : Vinculo):
        self.factor = factor_1
        self.permeabilidad = permeabilidad_1
        self.vinculo = vinculo_1
        
    def Get_factor(self):
        return self.factor
    
    def Get_permeabilidad(self):
        return self.permeabilidad

    def Get_vinculo(self):
        return self.vinculo


#_____________________________________________________________________________________________________________________________________________2

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
        
        # Inicializar el diccionario para almacenar los factores
        self.factors_dict = {}
        # Aquí agrega más campos de formulario según tus necesidades

    def load_image(self):
        img_path = 'figure_1.png'  # Cambia la ruta de la imagen según tu necesidad
        self.img = cv2.imread(img_path)
        if self.img is not None:
            self.show_image()
            self.create_form()
        else:
            print(f"No se pudo cargar la imagen {img_path}")

    def show_image(self):
        img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_width, img_height = img_pil.size

        # Ajusta el tamaño del lienzo al tamaño de la imagen
        self.canvas.config(width=img_width, height=img_height)

        img_tk = ImageTk.PhotoImage(image=img_pil)
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

        tk.Label(self.form_frame, text="Nombre del Rol:").grid(row=7, column=0)
        self.rol_nombre_entry = tk.Entry(self.form_frame)
        self.rol_nombre_entry.grid(row=7, column=1)

        tk.Label(self.form_frame, text="Peso de Influencia del Rol:").grid(row=8, column=0)
        self.rol_peso_influencia_entry = tk.Entry(self.form_frame)
        self.rol_peso_influencia_entry.grid(row=8, column=1)

        save_button = tk.Button(self.form_frame, text="Guardar Factor", command=self.save_factor)
        save_button.grid(row=9, column=0, columnspan=2)

    def save_factor(self):
        nombre = self.factor_name_entry.get()
        diversidad = float(self.diversity_entry.get())
        masa_critica = float(self.masa_critica_entry.get())
        orden = float(self.orden_entry.get())
        calidad = float(self.calidad_entry.get())
        coef_crecimiento = float(self.coef_crecimiento_entry.get())
        coef_mantenimiento = float(self.coef_mantenimiento_entry.get())
        rol_nombre = self.rol_nombre_entry.get()
        rol_peso_influencia = float(self.rol_peso_influencia_entry.get())

        # Crear un objeto Rol
        rol = Rol(rol_nombre, rol_peso_influencia)

        # Crear un objeto Factor con las propiedades ingresadas
        factor = Factor(nombre, diversidad, masa_critica, orden, calidad, coef_crecimiento, coef_mantenimiento, rol)

        # Obtener la ruta de la imagen cargada
        img_path = 'figure_1.png'  # Cambiar por la ruta correcta según tu implementación

        # Almacenar el factor junto con la imagen en el diccionario
        self.factors_dict[img_path] = factor

        # Limpia el formulario después de guardar el factor
        self.clear_form()
        
        # Cargar la siguiente imagen y mostrarla
        self.load_next_image()
    
    def clear_form(self):
        # Borra los valores de todos los campos del formulario
        self.factor_name_entry.delete(0, tk.END)
        self.diversity_entry.delete(0, tk.END)
        self.masa_critica_entry.delete(0, tk.END)
        self.orden_entry.delete(0, tk.END)
        self.calidad_entry.delete(0, tk.END)
        self.coef_crecimiento_entry.delete(0, tk.END)
        self.coef_mantenimiento_entry.delete(0, tk.END)
        self.rol_nombre_entry.delete(0, tk.END)
        self.rol_peso_influencia_entry.delete(0, tk.END)

    def load_next_image(self):
        # Lista de rutas de imágenes
        image_paths = ['figure_1.png', 'figure_2.png']  # Agrega todas las rutas necesarias

        # Obtener la ruta de la imagen actual
        current_index = len(self.factors_dict)  # Índice de la imagen actual
        if current_index < len(image_paths):
            next_img_path = image_paths[current_index]
        else:
            print("No hay más imágenes para cargar.")
            return

        # Cargar la siguiente imagen
        self.img = cv2.imread(next_img_path)
        if self.img is not None:
            self.show_image()
            self.create_form()
        else:
            print(f"No se pudo cargar la imagen {next_img_path}")


def main():
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()