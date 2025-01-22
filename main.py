import tkinter as tk
from gui import MedscribeGUI

def main():
    root = tk.Tk()
    app = MedscribeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()