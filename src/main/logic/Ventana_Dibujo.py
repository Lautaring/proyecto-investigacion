import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageDraw, ImageGrab, ImageTk


class PaintApp:
    def __init__(self, root, parent_app=None):
        self.root = root
        self.root.title("Paint Application")
        self.root.resizable(False, False)
        self.parent_app = parent_app  # Ventana principal

        self.color = 'black'
        self.brush_size = 1
        self.draw_tool = 'pencil'
        self.shapes = []
        self.selected_shape = None
        self.select_rect = None
        self.select_start = None
        self.canvas_image_id = None
        self.polyline_points = []
        self.polyline_colors = []

        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image = None
        self.canvas_image = None

        self.setup_ui()
        self.bind_events()

    def setup_ui(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        load_btn = tk.Button(toolbar, text="Load Image", command=self.load_image)
        load_btn.pack(side=tk.LEFT, padx=2, pady=2)

        color_btn = tk.Button(toolbar, text="Color", command=self.choose_color)
        color_btn.pack(side=tk.LEFT, padx=2, pady=2)

        erase_all_btn = tk.Button(toolbar, text="Erase All", command=self.erase_all)
        erase_all_btn.pack(side=tk.LEFT, padx=2, pady=2)

        erase_selected_btn = tk.Button(toolbar, text="Erase Selected", command=self.erase_selected)
        erase_selected_btn.pack(side=tk.LEFT, padx=2, pady=2)

        shape_menu = tk.Menubutton(toolbar, text="Shapes", relief=tk.RAISED)
        shape_menu.menu = tk.Menu(shape_menu, tearoff=0)
        shape_menu["menu"] = shape_menu.menu

        shape_menu.menu.add_command(label="Rectangle", command=lambda: self.set_draw_tool('rectangle'))
        shape_menu.menu.add_command(label="Oval", command=lambda: self.set_draw_tool('oval'))
        shape_menu.menu.add_command(label="Line", command=lambda: self.set_draw_tool('line'))
        shape_menu.menu.add_command(label="Polyline", command=lambda: self.set_draw_tool('polyline'))
        shape_menu.menu.add_command(label="Select", command=lambda: self.set_draw_tool('select'))

        shape_menu.pack(side=tk.LEFT, padx=2, pady=2)

        # Botón para guardar y cerrar
        save_close_btn = tk.Button(toolbar, text="Guardar y Cerrar", command=self.save_and_close)
        save_close_btn.pack(side=tk.LEFT, padx=2, pady=2)

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.root.bind("<Return>", self.close_polyline)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        self.image = Image.open(file_path)
        self.canvas.config(width=self.image.width, height=self.image.height)
        self.root.geometry(f"{self.image.width}x{self.image.height + 30}")  # Adjust window size
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.canvas_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)

        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        self.color = colorchooser.askcolor()[1]

    def set_draw_tool(self, tool):
        self.draw_tool = tool
        if tool != 'polyline':
            self.polyline_points = []  # Reset polyline points when changing tool
            self.polyline_colors = []  # Reset polyline colors when changing tool

    def erase_all(self):
        self.canvas.delete("all")
        if self.canvas_image_id:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)
        self.shapes = []

    def erase_selected(self):
        if self.selected_shape:
            self.canvas.delete(self.selected_shape)
            self.selected_shape = None
        elif self.select_rect:
            selected_shapes = self.canvas.find_enclosed(self.select_start[0], self.select_start[1], self.select_end[0], self.select_end[1])
            for shape in selected_shapes:
                if shape != self.canvas_image_id:
                    self.canvas.delete(shape)
            self.canvas.delete(self.select_rect)
            self.select_rect = None

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.draw_tool == 'polyline':
            self.polyline_points.append((event.x, event.y))
            self.polyline_colors.append(self.color)  # Store the color for this point
            if len(self.polyline_points) > 1:
                self.canvas.create_line(self.polyline_points[-2], self.polyline_points[-1], fill=self.polyline_colors[-2], width=self.brush_size, tags="current_polyline")
        elif self.draw_tool == 'select':
            self.select_start = (event.x, event.y)

    def on_mouse_drag(self, event):
        if self.draw_tool in ['rectangle', 'oval', 'line']:
            self.canvas.delete("current_shape")
            if self.draw_tool == 'rectangle':
                self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.color, tags="current_shape")
            elif self.draw_tool == 'oval':
                self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.color, tags="current_shape")
            elif self.draw_tool == 'line':
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=self.brush_size, tags="current_shape")
        elif self.draw_tool == 'select':
            if self.select_start:
                if self.select_rect:
                    self.canvas.delete(self.select_rect)
                self.select_end = (event.x, event.y)
                self.select_rect = self.canvas.create_rectangle(
                    self.select_start[0], self.select_start[1], event.x, event.y,
                    outline='red', dash=(2, 2), tags="select_rect")

    def on_button_release(self, event):
        end_x, end_y = event.x, event.y
        if self.draw_tool == 'rectangle':
            shape = self.canvas.create_rectangle(self.start_x, self.start_y, end_x, end_y, outline=self.color, tags="shape")
            self.shapes.append(shape)
            if self.image:
                self.draw.rectangle((self.start_x, self.start_y, end_x, end_y), outline=self.color)
        elif self.draw_tool == 'oval':
            shape = self.canvas.create_oval(self.start_x, self.start_y, end_x, end_y, outline=self.color, tags="shape")
            self.shapes.append(shape)
            if self.image:
                self.draw.ellipse((self.start_x, self.start_y, end_x, end_y), outline=self.color)
        elif self.draw_tool == 'line':
            shape = self.canvas.create_line(self.start_x, self.start_y, end_x, end_y, fill=self.color, width=self.brush_size, tags="shape")
            self.shapes.append(shape)
            if self.image:
                self.draw.line((self.start_x, self.start_y, end_x, end_y), fill=self.color, width=self.brush_size)

    def close_polyline(self, event):
        if self.draw_tool == 'polyline' and len(self.polyline_points) > 1:
            self.canvas.create_line(self.polyline_points[-1], self.polyline_points[0], fill=self.polyline_colors[-1], width=self.brush_size, tags="shape")
            for i in range(len(self.polyline_points) - 1):
                self.shapes.append(self.canvas.create_line(self.polyline_points[i], self.polyline_points[i + 1], fill=self.polyline_colors[i], width=self.brush_size, tags="shape"))
            self.shapes.append(self.canvas.create_line(self.polyline_points[-1], self.polyline_points[0], fill=self.polyline_colors[-1], width=self.brush_size, tags="shape"))
            self.polyline_points = []
            self.polyline_colors = []

    def on_right_click(self, event):
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if items:
            self.selected_shape = items[-1]  # Select the topmost item
            if self.selected_shape != self.canvas_image_id:
                self.canvas.itemconfig(self.selected_shape, outline="red")


    def save_and_close(self):
        # Definir un margen para evitar el recorte de formas
        margin = 1  # Puedes ajustar este valor según sea necesario
        
        # Obtener las coordenadas mínimas y máximas de todas las formas para ajustar el tamaño de la imagen
        min_x, min_y, max_x, max_y = float('inf'), float('inf'), float('-inf'), float('-inf')

        for shape in self.shapes:
            coords = self.canvas.coords(shape)
            min_x = min(min_x, *coords[::2])  # Comparar sólo coordenadas x
            min_y = min(min_y, *coords[1::2])  # Comparar sólo coordenadas y
            max_x = max(max_x, *coords[::2])  # Comparar sólo coordenadas x
            max_y = max(max_y, *coords[1::2])  # Comparar sólo coordenadas y

        # Asegurarse de que haya algo dibujado
        if min_x == float('inf') or min_y == float('inf'):
            return  # No hay formas dibujadas, no hay nada que guardar

        # Añadir márgenes a los límites para evitar el recorte de las formas
        min_x -= margin
        min_y -= margin
        max_x += margin
        max_y += margin

        # Calcular el tamaño de la imagen a partir de los límites con el margen añadido
        width = int(max_x - min_x)
        height = int(max_y - min_y)

        # Crear una nueva imagen con el tamaño exacto para contener todas las formas
        image = Image.new("RGBA", (width, height), (255, 255, 255, 0))  # Fondo blanco con transparencia
        draw = ImageDraw.Draw(image)

        # Recorrer las formas dibujadas y volcarlas a la imagen, ajustando las coordenadas relativas
        for shape in self.shapes:
            coords = self.canvas.coords(shape)
            shape_type = self.canvas.type(shape)
            # Ajustar las coordenadas para que sean relativas al nuevo tamaño
            adjusted_coords = [(x - min_x, y - min_y) for x, y in zip(coords[::2], coords[1::2])]

            if shape_type == 'rectangle':
                draw.rectangle(adjusted_coords, outline=self.color)
            elif shape_type == 'oval':
                draw.ellipse(adjusted_coords, outline=self.color)
            elif shape_type == 'line':
                draw.line(adjusted_coords, fill=self.color, width=self.brush_size)

        # Pasar la imagen a la aplicación principal (ImageCanvasApp)
        if self.parent_app:
            self.parent_app.set_canvas_image(image)

        # Cerrar la ventana de PaintApp
        self.root.destroy()

