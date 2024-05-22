from customtkinter import *
from PIL import Image

class Ventana:

    def __init__(self):

        self.app = CTk()
        self.ventanaAncho = self.obtenerAncho(self.app, 70)
        self.ventanaLargo = self.obtenerLargo(self.app, 70)
        #self.app.afeter(201, lambda : self.app.iconbitmap("Frontend/Icono.ico"))

        self.app.geometry(f"{self.ventanaAncho}x{self.ventanaLargo}")
        self.app.mainloop()

        self.generarFrames(self.app)
        
    def obtenerAncho(self, Ventana, Proporcion):

        Ancho = Ventana.winfo_screenwidth()

        return Ancho * Proporcion // 100

    def obtenerLargo(self, Ventana, Proporcion):

        Largo = Ventana.winfo_screenheight()

        return Largo * Proporcion // 100
    
    def obtenerEscala(self, Ventana, Longitud):

        return Ventana * Longitud // 100

    def generarFrames(self, Ventana):

        Ventana.rowconfigure(0, weight = 1)
        Ventana.rowconfigure(1, weight = 1)
        Ventana.columnconfigure(0, weight = 1)

        primerFrameAncho = self.obtenerEscala(self.ventanaAncho, 100) 
        primerFrameLargo = self.obtenerEscala(self.ventanaLargo, 66)

        segundoFrameAncho = self.obtenerEscala(self.ventanaAncho, 100)
        segundoFrameLargo = self.obtenerEscala(self.ventanaLargo, 33)

        primerFrame = CTkFrame(master = Ventana,
                               width = primerFrameAncho,
                               height = primerFrameLargo)

        segundoFrame = CTkFrame(master = Ventana,
                                width = segundoFrameAncho,
                                height = segundoFrameLargo)
        
        primerFrame.grid(row = 0, column = 0, sticky = "nsew")
        segundoFrame.grid(row = 1, column = 0, sticky = "nsew")
        
        self.generarContenido(primerFrame, primerFrameAncho, primerFrameLargo)
        self.cajaTexto(segundoFrame, segundoFrameAncho, segundoFrameLargo)

    def generarContenido(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)
        Frame.columnconfigure(1, weight = 1)
        Frame.columnconfigure(1, weight = 1)

        contenedoresAncho = self.obtenerEscala(Ancho, 33)
        contenedoresLargo = self.obtenerEscala(Largo, 100)

        Nuevos = CTkScrollableFrame(master = Frame,
                                    width = contenedoresAncho,
                                    height = contenedoresLargo
                                    )
        
        Pendientes = CTkFrame(master = Frame,
                              width = contenedoresAncho,
                              height = contenedoresLargo)

        Terminados = CTkScrollableFrame(master = Frame,
                                    width = contenedoresAncho,
                                    height = contenedoresLargo
                                    )
        
        Nuevos.grid(row = 0, column = 0, sticky = "nsew")
        Pendientes.grid(row = 1, column = 0, sticky = "nsew", padx = 20)
        Terminados.grid(row = 2, column = 0, sticky = "nsew")

        self.generarPendientes(Pendientes, Ancho, Largo)

    def generarPendientes(Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 1)
        Frame.rowconfigure(1, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        #Listos = CTkFrame     

    def cajaTexto(Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        Contenido = CTkTextbox(master = Frame,
                               width = Ancho,
                               height = Largo)

        Contenido.grid(row = 0, column = 0, sticky = "nsew")    
