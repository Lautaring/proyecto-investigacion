import tkinter as tk
from AdminGUI import AdminGUI

def main():
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()