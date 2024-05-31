import tkinter as tk
from AdminGUI import AdminGUI
from logic.Tablero import Tablero

def main():
    root = tk.Tk()
    app = AdminGUI(root)

    tablero = Tablero(5, 5) # aca tengo que guardar la imagen, ya vere como hago

    root.mainloop()

if __name__ == "__main__":
    main()