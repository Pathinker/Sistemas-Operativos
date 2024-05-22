from customtkinter import *
from PIL import Image

class Ventana:

    def __init__(self):

        self.app = CTk()
        self.ventanaAncho = self.obtenerAnchoPantalla(self.app, 70)
        self.ventanaLargo = self.obtenerLargoPantalla(self.app, 70)
        #self.app.afeter(201, lambda : self.app.iconbitmap("Frontend/Icono.ico"))

        self.app.geometry(f"{self.ventanaAncho}x{self.ventanaLargo}")
        self.app.mainloop()
        
    def obtenerAnchoPantalla(self, Ventana, Proporcion):

        Ancho = Ventana.winfo_screenwidth()

        return Ancho * Proporcion // 100

    def obtenerLargoPantalla(self, Ventana, Proporcion):

        Largo = Ventana.winfo_screenheight()

        return Largo * Proporcion // 100
    
    def obtenerAncho(self, Ventana, Ancho):

        return Ventana * Ancho // 100
    
    def obtenrLargo(self, Ventana, Largo):

        return Ventana * Largo // 100
