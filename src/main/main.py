import tkinter as tk
from AdminGUI import AdminGUI
from interfazgrafica2 import ImageCanvasApp
from logic.Tablero import Tablero


def main():
    root = tk.Tk()
    app = ImageCanvasApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()