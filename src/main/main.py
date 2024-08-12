import tkinter as tk
from AdminGUI import AdminGUI
from logic.Tablero import Tablero


def main():
    root = tk.Tk()
    app = AdminGUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()