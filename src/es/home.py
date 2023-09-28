import tkinter
from tkinter import Tk
from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Entry
from tkinter import Text

from PIL import Image, ImageTk



class mainFrame:
    def __init__(self, master):
        self.master = master
        self.master.geometry("300x700+10+10")
        self.frame = Frame(self.master)
        self.butnew("Ausgangs-Rechnung schreiben", "rechnungSchreiben")
        self.butnew("Lieferanten-Rechnung einpflegen", "rechnungEinpflegen")
        Label(self.frame, text="--- Korrekturen ---", font=("Arial", 7)).pack(pady=0)
        self.butnew("Lieferanten-Rechnung löschen", "lieferantenFehlerBeheben")
        self.butnew("Zahlung Ausgangsrechnung", "zahlungsBelegHochladen")
        self.butnew("Ausgangs-Rechnung korrigieren", "rechnungKorrigieren")
        Label(self.frame, text="--- Auswertungen ---", font=("Arial", 7)).pack(pady=0)
        self.butnew("Auswertung", "Auswertung")
        Label(self.frame, text="--- Andere ---", font=("Arial", 7)).pack(pady=0)
        self.quit = Button(self.frame, text="Schließen", command=self.close_window).pack(pady=10)
        self.releaseNotes = Label(self.master, text="Version 1.0.0", font=("Arial", 7))
        self.releaseNotes.bind("<Button-1>", self.printReleaseNotes)
        self.releaseNotes.pack(side="bottom")
        self.frame.pack()

    def printReleaseNotes(self, event):
        print("Version 1.1.0 - Changes:")
        print("- Hinzufügen des Auswertungsbuttons")

    def butnew(self, text, _class):
        Button(self.frame, text=text, command=lambda: self.new_window(_class)).pack(pady=10)

    def new_window(self, _class):
        pass

    def close_window(self):
        self.master.destroy()


if __name__ == "__main__":
    root = Tk()
    root.tk.call('tk', 'scaling', 1.7)
    root.mainloop()