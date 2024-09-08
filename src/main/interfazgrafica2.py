import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, Toplevel
from PIL import Image, ImageTk
from shapely.geometry import box, Polygon
# Importar la clase PaintApp de la segunda ventana
from logic.Ventana_Dibujo import PaintApp  # Asegúrate de que este archivo esté en el mismo directorio


# Clase para manejar la aplicación

def rgb_a_hex(color_rgb):
    return "#{:02x}{:02x}{:02x}".format(*color_rgb)


class ImageCanvasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drag and Drop with Multi-Image Intersection Detection")

        # Crear un marco principal
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear un lienzo
        self.canvas = tk.Canvas(self.main_frame, width=800, height=600, bg='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un marco para el formulario
        self.form_frame = tk.Frame(self.main_frame)
        self.form_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Crear el formulario
        self.crear_formulario()

        # Lista para almacenar los elementos de imagen y sus coordenadas
        self.images = []

        # Cargar imagen desde el sistema de archivos
        load_button = tk.Button(self.form_frame, text="Cargar Imagen", command=self.load_image)
        load_button.grid(row=12, columnspan=2, pady=10)  # Cambiamos a grid

        # Nuevo botón para abrir la segunda ventana
        open_paint_button = tk.Button(self.form_frame, text="Abrir Paint App", command=self.open_paint_window)
        open_paint_button.grid(row=13, columnspan=2, pady=10)  # Cambiamos a grid

        # Variables para arrastrar
        self.drag_data = {"x": 0, "y": 0, "item": None}

        # Crear un marco para los botones adicionales
        self.marco_botones = tk.Frame(self.main_frame)
        self.marco_botones.pack(side=tk.BOTTOM, pady=10)  # Manteniendo pack aquí ya que es un contenedor separado

        # Conectar eventos del ratón para el arrastre
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        # Botón confirmar
        boton_confirmar = tk.Button(self.marco_botones, text="Confirmar Dibujo", command=self.confirmar_dibujo)
        boton_confirmar.pack(padx=10, pady=10)

        self.boton_agregar_factores = tk.Button(self.marco_botones, text="Agregar Factores", command=self.mostrar_factores)
        self.boton_agregar_factores.pack(padx=10, pady=10, fill="x")

        self.propiedades_colores = {
            "cloaca": {"valor": 3, "uso_suelo": 1, "extra": {"color": "#6b7e67"}},  # Ejemplo de color en formato RGB hexadecimal
            "red": {"valor": 5, "uso_suelo": 6, "extra": {"color": "#ff0000"}},     # Rojo
            "green": {"valor": 2, "uso_suelo": 4, "extra": {"color": "#00ff00"}},   # Verde
            "yellow": {"valor": 4, "uso_suelo": 3, "extra": {"color": "#ffff00"}},  # Amarillo
            "blue": {"valor": 6, "uso_suelo": 2, "extra": {"color": "#0000ff"}},    # Azul
        }

        # este boton debe salir en la pantalla Abrir paint app, en vez de color debe salir este boton que solo deja dibujar con los factores que ya se crearon
        self.lista_colores = tk.StringVar(value="Seleccionar Color")
        self.boton_selector_color = tk.OptionMenu(self.marco_botones, self.lista_colores, *self.propiedades_colores.keys(), command=self.seleccionar_color)
        self.boton_selector_color.pack(padx=10, pady=10, fill="x")

        # Crear el menú
        self.crear_menu()

    def seleccionar_color(self, color):
        self.color_trazo = color
        print(f"Color seleccionado: {color}")

    def mostrar_factores(self):
        ventana_factores = tk.Toplevel(self.root)
        ventana_factores.title("Factores")
        ventana_factores.geometry("400x300")
        ventana_factores.resizable(False, False)
        
        # Mostrar la lista de factores existentes
        lista_factores = tk.Listbox(ventana_factores)
        lista_factores.pack(fill="both", expand=True, padx=10, pady=10)
        
        for factor in self.propiedades_colores.keys():
            lista_factores.insert(tk.END, factor)
        
        # Botón para agregar un nuevo factor
        boton_agregar = tk.Button(ventana_factores, text="Agregar Factor", command=lambda: self.agregar_nuevo_factor(ventana_factores))
        boton_agregar.pack(pady=10)

    def crear_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        archivo_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Cargar Mundo", command=self.cargar_mundo)
        archivo_menu.add_command(label="Guardar Mundo", command=self.guardar_mundo)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)

        ajustar_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Ajustar", menu=ajustar_menu)

    def confirmar_dibujo(self):
        self.dinamico = True
        print("Dibujo confirmado. Ahora puedes interactuar con las celdas.")

    def guardar_mundo(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if archivo:
            imagen = Image.new("RGB", (self.columnas * self.tamaño_celda, self.filas * self.tamaño_celda), "white")
            draw = ImageDraw.Draw(imagen)

            items = self.canvas.find_all()
            for item in items:
                coords = self.canvas.coords(item)
                color = self.canvas.itemcget(item, 'fill')
                if color:
                    x1, y1, x2, y2 = coords
                    draw.rectangle([x1, y1, x2, y2], fill=color, outline=color)
            
            imagen.save(archivo)

    def seleccionar_color_nuevo(self, entrada_nombre):
        color = colorchooser.askcolor()[1]
        if color:
            self.color_seleccionado = color
            entrada_nombre.config(bg=color)

    def agregar_nuevo_factor(self, ventana_factores):
        ventana_nuevo_factor = tk.Toplevel(self.root)
        ventana_nuevo_factor.title("Agregar Nuevo Factor")
        ventana_nuevo_factor.geometry("400x300")
        ventana_nuevo_factor.resizable(False, False)
        
        # Campo para el nombre del nuevo factor
        frame_nombre = tk.Frame(ventana_nuevo_factor)
        frame_nombre.pack(fill="x", pady=5)
        tk.Label(frame_nombre, text="Nombre del Factor:", width=20, anchor="w").pack(side="left")
        entrada_nombre = tk.Entry(frame_nombre)
        entrada_nombre.pack(fill="x", expand=True)
        
        # Selector de color
        frame_color = tk.Frame(ventana_nuevo_factor)
        frame_color.pack(fill="x", pady=5)
        tk.Label(frame_color, text="Color:", width=20, anchor="w").pack(side="left")
        selector_color = tk.Button(frame_color, text="Seleccionar Color", command=lambda: self.seleccionar_color_nuevo(entrada_nombre))
        selector_color.pack(side="left")
        
        # Campos para propiedades
        frame_propiedad = tk.Frame(ventana_nuevo_factor)
        frame_propiedad.pack(fill="x", pady=5)
        tk.Label(frame_propiedad, text="Propiedad:", width=20, anchor="w").pack(side="left")
        entrada_propiedad = tk.Entry(frame_propiedad)
        entrada_propiedad.pack(fill="x", expand=True)
        
        frame_valor = tk.Frame(ventana_nuevo_factor)
        frame_valor.pack(fill="x", pady=5)
        tk.Label(frame_valor, text="Valor:", width=20, anchor="w").pack(side="left")
        entrada_valor = tk.Entry(frame_valor)
        entrada_valor.pack(fill="x", expand=True)
        
        # Botón para guardar el nuevo factor
        boton_guardar = tk.Button(ventana_nuevo_factor, text="Guardar Factor", command=lambda: self.guardar_nuevo_factor(entrada_nombre.get(), self.color_seleccionado, entrada_propiedad.get(), entrada_valor.get(), ventana_nuevo_factor))
        boton_guardar.pack(pady=10)

    def guardar_nuevo_factor(self, nombre, color, propiedad, valor, ventana):
        if nombre and color:
            # Verificar si el nuevo nombre de factor ya existe
            if nombre not in self.propiedades_colores:
                # Crear una nueva entrada con valores predeterminados
                self.propiedades_colores[nombre] = {'valor': 0, 'uso_suelo': 0, 'extra': {'color': color}}

                # Agregar propiedades adicionales si se proporcionan
                if propiedad and valor:
                    self.propiedades_colores[nombre]['extra'][propiedad] = valor

                # Actualizar la lista desplegable
                self.boton_selector_color['menu'].add_command(label=nombre, command=tk._setit(self.lista_colores, nombre))

                messagebox.showinfo("Factor Agregado", f"Factor '{nombre}' con color '{color}' agregado.")
                ventana.destroy()
                self.mostrar_factores()  # Mostrar la lista actualizada de factores
            else:
                messagebox.showwarning("Factor Existente", "El nombre del factor ya existe.")
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor, completa todos los campos necesarios.")

    def cargar_mundo(self):
        archivo_cargar = filedialog.askopenfilename(filetypes=[("Archivos PNG", "*.png")])
        if archivo_cargar:
            imagen = Image.open(archivo_cargar)

            # Verificar el tamaño de la imagen cargada
            if imagen.size != (self.columnas * self.tamaño_celda, self.filas * self.tamaño_celda):
                messagebox.showerror("Error", "La imagen no coincide con el tamaño del mundo.")
                return
            imagen = imagen.convert("RGB")

            self.canvas.delete("all")
            self.trazos = []

            for y in range(0, imagen.height, self.tamaño_celda):
                for x in range(0, imagen.width, self.tamaño_celda):
                    caja = (x, y, x + self.tamaño_celda, y + self.tamaño_celda)
                    color = imagen.crop(caja).getpixel((0, 0))
                    color_hex = rgb_a_hex(color) 
                    if color:
                        self.canvas.create_rectangle(
                            x, y, x + self.tamaño_celda, y + self.tamaño_celda,
                            fill=color_hex, outline=color_hex
                        )
                        self.propiedades_celdas[(x // self.tamaño_celda, y // self.tamaño_celda)] = {'valor': 0, 'uso_suelo': 0}

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


    # Método para abrir la ventana de pintura
    def open_paint_window(self):
        # Crear la ventana de PaintApp y pasar una referencia a la clase principal
        self.paint_window = Toplevel(self.root)
        self.paint_window.title("Paint Application")
        self.paint_window.geometry("800x600")
        #self.paint_window.attributes("-topmost", True)
        # Crear una instancia de PaintApp y pasar self (referencia a ImageCanvasApp)
        PaintApp(self.paint_window, self)


    # Método para cargar la imagen desde PaintApp en el lienzo principal
    def set_canvas_image(self, image):
        pil_image = image
        #pil_image = pil_image.resize((100, 100))
        tk_image = ImageTk.PhotoImage(pil_image)
        item_id = self.canvas.create_image(50, 50, image=tk_image, anchor=tk.NW)
        self.images.append({"id": item_id, "image": tk_image, "bbox": (50, 50, 150, 150)})


    # Método para cargar una imagen desde el sistema de archivos
    def load_image(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
        if image_path:
            pil_image = Image.open(image_path)
            pil_image = pil_image.resize((100, 100))
            tk_image = ImageTk.PhotoImage(pil_image)
            item_id = self.canvas.create_image(50, 50, image=tk_image, anchor=tk.NW)
            self.images.append({"id": item_id, "image": tk_image, "bbox": (50, 50, 150, 150)})


    # Métodos de arrastre de imágenes
    def on_press(self, event):
        # Detectar si se hace clic en una imagen
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            self.drag_data["item"] = item
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y


    def on_release(self, event):
        # Al soltar, reiniciar los datos de arrastre
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
        self.update_bbox()  # Actualizar las posiciones de los bounding boxes


    def on_drag(self, event):
        # Durante el arrastre, mover la imagen
        if self.drag_data["item"]:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            self.canvas.move(self.drag_data["item"], dx, dy)

            # Actualizar las coordenadas
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y


    # Método para actualizar las coordenadas de las imágenes
    def update_bbox(self):
        # Actualiza los "bounding boxes" (áreas) de las imágenes después de que sean movidas
        for img in self.images:
            bbox = self.canvas.bbox(img["id"])
            img["bbox"] = bbox
        self.check_intersections()


    # Método para verificar intersecciones entre imágenes
    def check_intersections(self):
        # Eliminar cualquier intersección previa dibujada
        self.canvas.delete("intersection")

        # Almacenar las intersecciones en una lista
        all_intersections = []

        # Calcular intersecciones entre pares, tríos y cuartetos de imágenes
        num_images = len(self.images)
        if num_images >= 2:
            # Intersecciones entre pares de imágenes
            for i in range(num_images):
                for j in range(i + 1, num_images):
                    bbox1 = self.images[i]["bbox"]
                    bbox2 = self.images[j]["bbox"]

                    # Crear rectángulos de Shapely
                    rect1 = box(bbox1[0], bbox1[1], bbox1[2], bbox1[3])
                    rect2 = box(bbox2[0], bbox2[1], bbox2[2], bbox2[3])

                    # Verificar si hay intersección
                    if rect1.intersects(rect2):
                        intersection = rect1.intersection(rect2)
                        all_intersections.append((i, j, intersection))
                        self.draw_intersection(intersection, color="blue")  # Intersecciones de pares

        if num_images >= 3:
            # Intersecciones entre tríos de imágenes
            for i in range(num_images):
                for j in range(i + 1, num_images):
                    for k in range(j + 1, num_images):
                        bbox1 = self.images[i]["bbox"]
                        bbox2 = self.images[j]["bbox"]
                        bbox3 = self.images[k]["bbox"]

                        # Crear rectángulos de Shapely
                        rect1 = box(bbox1[0], bbox1[1], bbox1[2], bbox1[3])
                        rect2 = box(bbox2[0], bbox2[1], bbox2[2], bbox2[3])
                        rect3 = box(bbox3[0], bbox3[1], bbox3[2], bbox3[3])

                        # Unificar la intersección de los tres
                        intersection = rect1.intersection(rect2).intersection(rect3)
                        if not intersection.is_empty:
                            all_intersections.append((i, j, k, intersection))
                            self.draw_intersection(intersection, color="green")  # Intersecciones de tríos

        if num_images >= 4:
            # Intersección entre cuatro imágenes
            bbox1 = self.images[0]["bbox"]
            bbox2 = self.images[1]["bbox"]
            bbox3 = self.images[2]["bbox"]
            bbox4 = self.images[3]["bbox"]

            # Crear rectángulos de Shapely
            rect1 = box(bbox1[0], bbox1[1], bbox1[2], bbox1[3])
            rect2 = box(bbox2[0], bbox2[1], bbox2[2], bbox2[3])
            rect3 = box(bbox3[0], bbox3[1], bbox3[2], bbox3[3])
            rect4 = box(bbox4[0], bbox4[1], bbox4[2], bbox4[3])

            # Unificar la intersección de los cuatro
            intersection = rect1.intersection(rect2).intersection(rect3).intersection(rect4)
            if not intersection.is_empty:
                all_intersections.append((0, 1, 2, 3, intersection))
                self.draw_intersection(intersection, color="red")  # Intersección de los cuatro

        # Imprimir las intersecciones y sus imágenes asociadas
        for inter in all_intersections:
            indices = inter[:-1]
            intersection = inter[-1]
            print(f"Intersección entre imágenes: {indices}")
            print(f"Detalles de la intersección: {intersection}")


    # Método para dibujar las intersecciones
    def draw_intersection(self, intersection, color):
        # Dibujar la intersección en el lienzo
        if isinstance(intersection, Polygon):
            x, y = intersection.exterior.coords.xy
            points = list(zip(x, y))
            # Convertir los puntos en coordenadas de Tkinter (lista de tuplas planas)
            flattened_points = [coord for point in points for coord in point]
            self.canvas.create_polygon(flattened_points, outline=color, fill='', tags="intersection")


    # Método para guardar los datos del formulario
    def guardar_factor(self):
        # Aquí puedes implementar la lógica para guardar los datos del formulario
        tipo_factor = self.tipo_factor_var.get()
        componente = self.componente_var.get()
        factor_name = self.factor_name_entry.get()
        diversidad = self.diversity_entry.get()
        masa_critica = self.masa_critica_entry.get()
        orden = self.orden_entry.get()
        calidad = self.calidad_entry.get()
        coef_crecimiento = self.coef_crecimiento_entry.get()
        coef_mantenimiento = self.coef_mantenimiento_entry.get()
        tipo_rol = self.tipo_rol_var.get()
        tipo_permeabilidad = self.tipo_permeabilidad_var.get()

        # Verificar si los campos están vacíos
        if not all([factor_name, diversidad, masa_critica, orden, calidad, coef_crecimiento, coef_mantenimiento]):
            messagebox.showerror("Error", "Todos los campos deben ser completados")
            return

        # Aquí podrías agregar lógica para guardar los datos, por ejemplo en un archivo o base de datos
        print("Datos guardados:")
        print(f"Tipo de factor: {tipo_factor}")
        print(f"Componente del Factor: {componente}")
        print(f"Nombre del Factor: {factor_name}")
        print(f"Diversidad: {diversidad}")
        print(f"Masa Crítica: {masa_critica}")
        print(f"Orden: {orden}")
        print(f"Calidad: {calidad}")
        print(f"Coeficiente de Crecimiento: {coef_crecimiento}")
        print(f"Coeficiente de Mantenimiento: {coef_mantenimiento}")
        print(f"Tipo de Rol: {tipo_rol}")
        print(f"Tipo de Permeabilidad: {tipo_permeabilidad}")


# Inicializar la aplicación
root = tk.Tk()
app = ImageCanvasApp(root)
root.mainloop()



"""Ver esta opcion"""
# def abrir_ventana_paint(self):
#     Crear una nueva ventana (Toplevel)
#     new_window = Toplevel(self.root)
#     PaintApp(new_window)
