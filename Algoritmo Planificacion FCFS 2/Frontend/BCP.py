from customtkinter import *
from CTkTable import *
from PIL import Image

from Backend import Proceso

class BCP:

    def __init__(self, Ventana, procesosNuevos, procesosListos, procesosEjecucion, procesosBloqueados, procesosTerminados, Estado, Tiempo):

        self.app = CTkToplevel(Ventana)
        self.ventanaAncho = self.obtenerAncho(self.app, 70)
        self.ventanaLargo = self.obtenerLargo(self.app, 70)
        self.app.after(201, lambda : self.app.iconbitmap("Frontend/Imagenes/Icono.ico"))
        self.app.title("Bloque Control Del Proceso")

        self.app.geometry(f"{self.ventanaAncho}x{self.ventanaLargo}")
        self.app.protocol("WM_DELETE_WINDOW", lambda: self.cerrarVentana(Estado))

        #Paleta Colores

        self.colorFondo = '#373739'
        self.primerGris = "#19191a"
        self.segundoGris = "#4A4A4D"
        self.textoGris = "#c6c6c6"
        
        self.fondoAzul = "#1565C0"    

        self.procesosNuevos = procesosNuevos.copy()
        self.procesosListos = procesosListos.copy()
        self.procesosEjecucion = procesosEjecucion.copy()
        self.procesosBloqueados = procesosBloqueados.copy()
        self.procesosTerminados = procesosTerminados.copy()
        self.Tiempo = Tiempo    

        self.generarFrames(self.app, Estado)

    def cerrarVentana(self, Estado):

        Estado[0] = True
        self.app.destroy()

    def obtenerAncho(self, Ventana, Proporcion):

        Ancho = Ventana.winfo_screenwidth()

        return Ancho * Proporcion // 100

    def obtenerLargo(self, Ventana, Proporcion):

        Largo = Ventana.winfo_screenheight()

        return Largo * Proporcion // 100
    
    def obtenerEscala(self, Ventana, Longitud):

        return Ventana * Longitud // 100  
    
    def generarFrames(self, Ventana, Estado):

        Ventana.rowconfigure(0, weight = 1)
        Ventana.rowconfigure(1, weight = 1)
        Ventana.columnconfigure(0, weight = 1)

        primerFrameAncho = self.obtenerEscala(self.ventanaAncho, 100) 
        primerFrameLargo = self.obtenerEscala(self.ventanaLargo, 70)

        segundoFrameAncho = self.obtenerEscala(self.ventanaAncho, 100)
        segundoFrameLargo = self.obtenerEscala(self.ventanaLargo, 30)

        primerFrame = CTkFrame(master = Ventana,
                               width = primerFrameAncho,
                               height = primerFrameLargo)

        segundoFrame = CTkFrame(master = Ventana,
                                width = segundoFrameAncho,
                                height = segundoFrameLargo)
        
        primerFrame.grid(row = 0, column = 0, sticky = "nsew", padx = 10, pady = 5)
        segundoFrame.grid(row = 1, column = 0, sticky = "nsew", padx = 10, pady = 5)
        
        self.generarContenido(primerFrame, primerFrameAncho, primerFrameLargo)
        self.cajaTexto(segundoFrame, segundoFrameAncho, segundoFrameLargo, Estado)

    def generarContenido(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 0)
        Frame.rowconfigure(1, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        encabezadoAncho = self.obtenerEscala(Ancho, 100)
        encabezadoLargo = self.obtenerEscala(Largo, 5)

        contenedorAncho = self.obtenerEscala(Ancho, 100)
        contenedorLargo = self.obtenerEscala(Largo, 95)

        Encabezado = CTkFrame(master = Frame,
                              width = encabezadoAncho,
                              height = encabezadoLargo)

        Contenedor = CTkScrollableFrame(master = Frame,
                                        width = contenedorAncho,
                                        height = contenedorLargo,
                                        corner_radius = 0,
                                        fg_color = self.colorFondo 
                                        )
        

        Encabezado.grid(row = 0, column = 0, sticky = "nsew")
        Contenedor.grid(row = 1, column = 0, sticky = "nsew")

        self.establecerTitulo(Encabezado, encabezadoAncho, encabezadoLargo)
        self.establecerTabla(Contenedor, contenedorAncho, contenedorLargo)

    def establecerTitulo(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        Imagen = CTkImage(light_image = Image.open("Frontend/Imagenes/BCP.png"),
                          dark_image = Image.open("Frontend/Imagenes/BCP.png"),
                          size = (16, 16))

        Titulo = CTkLabel(master = Frame,
                          width = Ancho,
                          height = Largo,
                          text = " Bloque Control Del Proceso",
                          font = ("Helvetica", 14),
                          anchor = "w",
                          image = Imagen,
                          compound = "left",
                          fg_color = self.primerGris)
        
        Titulo.grid(row = 0, column = 0, sticky = "nsew")

    def establecerTabla(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        datosTabla = [["ID", "T/ Est", "T/ Eje", "1°N", "Op", "2°N", "Res", "T/Lle" , "T/Fin", "T/Ret", "T/Res", "T/Esp", "T/Ser", "T/Blo Res", "T/Eje Res"]]

        for i in range(len(self.procesosTerminados)):

            Temporal = self.procesosTerminados[i].obtenerBCP()
            datosTabla.append(Temporal)

        for i in range(len(self.procesosEjecucion)):

            self.procesosEjecucion[i].asignarResultado(None)
            self.procesosEjecucion[i].asignarTiempoFinalizacion(None)
            self.procesosEjecucion[i].asignarTiempoRetorno(None)
            self.procesosEjecucion[i].asignarTiempoEspera(self.Tiempo - self.procesosEjecucion[i].obtenerTiempoInicio())  

            Temporal = self.procesosEjecucion[i].obtenerBCP()  

            datosTabla.append(Temporal)

        for i in range(len(self.procesosBloqueados)):

            self.procesosBloqueados[i].asignarResultado(None)
            self.procesosBloqueados[i].asignarTiempoFinalizacion(None)
            self.procesosBloqueados[i].asignarTiempoRetorno(None)
            self.procesosBloqueados[i].asignarTiempoEspera(self.Tiempo - self.procesosBloqueados[i].obtenerTiempoInicio())  

            Temporal = self.procesosBloqueados[i].obtenerBCP()  

            datosTabla.append(Temporal)              
    
        for i in range(len(self.procesosListos)):   

            self.procesosListos[i].asignarResultado(None)
            self.procesosListos[i].asignarTiempoFinalizacion(None)
            self.procesosListos[i].asignarTiempoRetorno(None)
            self.procesosListos[i].asignarTiempoEspera(self.Tiempo - self.procesosListos[i].obtenerTiempoInicio())  

            Temporal = self.procesosListos[i].obtenerBCP()  

            datosTabla.append(Temporal)
    
        for i in range(len(self.procesosNuevos)):

            self.procesosNuevos[i].asignarResultado(None)
            self.procesosNuevos[i].asignarTiempoLlegada(None)
            self.procesosNuevos[i].asignarTiempoFinalizacion(None)
            self.procesosNuevos[i].asignarTiempoRetorno(None)
            self.procesosNuevos[i].asignarTiempoEspera(self.Tiempo -  self.procesosNuevos[i].obtenerTiempoInicio())            

            Temporal = self.procesosNuevos[i].obtenerBCP()

            datosTabla.append(Temporal)

        self.tablaTerminados = CTkTable(master = Frame,
                         row = len(datosTabla),
                         column = len(datosTabla[0]),
                         header_color = self.fondoAzul,
                         values = datosTabla,
                         corner_radius = 0)
        
        self.tablaTerminados.grid(row = 0, column = 0, sticky = "nsew")       
    
    def cajaTexto(self, Frame, Ancho, Largo, Estado):

        Frame.rowconfigure(0, weight = 0)
        Frame.rowconfigure(1, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        tituloAncho = self.obtenerEscala(Ancho, 100)
        tituloLargo = self.obtenerEscala(Largo, 10)

        contenidoAncho = self.obtenerEscala(Ancho, 100)
        contenidoLargo = self.obtenerEscala(Largo, 90)

        Imagen = CTkImage(light_image = Image.open("Frontend/Imagenes/Terminal.png"),
                          dark_image = Image.open("Frontend/Imagenes/Terminal.png"),
                          size = (16, 16))

        Titulo = CTkLabel(master = Frame,
                          width = tituloAncho,
                          height = tituloLargo,
                          text = " Terminal",
                          font = ("Helvetica", 14),
                          fg_color = self.primerGris,
                          anchor = "w",
                          image = Imagen,
                          compound = "left")

        Contenido = CTkTextbox(master = Frame,
                               width = contenidoAncho,
                               height = contenidoLargo,
                               fg_color = self.colorFondo,
                               text_color = "White",
                               corner_radius = 0,
                               font=("Consolas", 16))
        
        Contenido.insert("1.0", "Escriba Teclas Entrada\n\n")
        Contenido.insert("3.0", "C: Continuar\n\n")

        Contenido.bind("<KeyPress>", lambda event: self.Enter(event.char, Estado))

        Titulo.grid(row = 0, column = 0, sticky = "nsew")
        Contenido.grid(row = 1, column = 0, sticky = "nsew")    
        
    def Enter(self, Caracter, Estado):

        Caracter = Caracter.upper()

        if(Caracter == "C"):

            self.cerrarVentana(Estado)  
