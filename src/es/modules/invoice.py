import tkinter as tk
import TKinterModernThemes as TKMT

class WriteInvoice(TKMT.ThemedTKinterFrame):

    def __init__(self): 
        super().__init__("Analyse", mode="dark")

        self.root.geometry("500x500")
        self.root.title("Analyse")
        self.root.protocol("WM_DELETE_WINDOW", self.handleExit)

        self.Label("Analyse").grid(row=1, column=0, pady=(30, 0))

    def handleExit(self):
        self.root.destroy()