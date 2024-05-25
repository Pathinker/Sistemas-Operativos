from customtkinter import *
from CTkTable import *
from PIL import Image
import time

from Backend import Multiprogramacion

class Ventana:

    def __init__(self):

        self.app = CTk()
        self.ventanaAncho = self.obtenerAncho(self.app, 70)
        self.ventanaLargo = self.obtenerLargo(self.app, 70)
        self.app.after(201, lambda : self.app.iconbitmap("Frontend/Imagenes/Icono.ico"))
        self.app.title("Multiprogramación Lotes")

        self.app.geometry(f"{self.ventanaAncho}x{self.ventanaLargo}")

        #Paleta Colores

        self.colorFondo = '#373739'
        self.primerGris = "#19191a"
        self.segundoGris = "#4A4A4D"
        self.textoGris = "#c6c6c6"
        
        self.fondoAzul = "#1565C0"

        self.app.protocol("WM_DELETE_WINDOW", self.cerrarVentana)
    
        self.pantallaInicio(self.app)
                 
        self.app.mainloop()

    def cerrarVentana(self):

        try:

            self.Multiprogramacion.detener()

        except:

            pass

        self.app.destroy()    
    
    def obtenerAncho(self, Ventana, Proporcion):

        Ancho = Ventana.winfo_screenwidth()

        return Ancho * Proporcion // 100

    def obtenerLargo(self, Ventana, Proporcion):

        Largo = Ventana.winfo_screenheight()

        return Largo * Proporcion // 100
    
    def obtenerEscala(self, Ventana, Longitud):

        return Ventana * Longitud // 100
    
    def pantallaInicio(self, Frame):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        anchoFrame = self.obtenerEscala(self.ventanaAncho, 100)
        largoFrame = self.obtenerEscala(self.ventanaLargo, 100)

        Fondo = CTkFrame(master = Frame,
                         width = anchoFrame,
                         height = largoFrame,
                         fg_color = self.fondoAzul,
                         corner_radius = 0)
        
        Fondo.grid(row = 0, column = 0, sticky = "nsew")

        Fondo.rowconfigure(0, weight = 1)
        Fondo.columnconfigure(0, weight = 1)

        anchoContenido = self.obtenerEscala(anchoFrame, 40)
        largoContenido = self.obtenerEscala(largoFrame, 40)

        contenidoFrame = CTkFrame(master = Fondo,
                                  width = anchoContenido,
                                  height = largoContenido,
                                  fg_color = self.primerGris,
                                  corner_radius = 0)
        
        contenidoFrame.grid(row = 0, column = 0)

        contenidoFrame.rowconfigure(0, weight = 1)
        contenidoFrame.rowconfigure(1, weight = 1)
        contenidoFrame.rowconfigure(2, weight = 1)
        contenidoFrame.columnconfigure(0, weight = 1)

        cantidadFrameAncho = self.obtenerEscala(anchoContenido, 100)
        cantidadFrameLargo = self.obtenerEscala(largoContenido, 40)

        botonFrameAncho = self.obtenerEscala(anchoContenido, 100)
        botonFrameLargo = self.obtenerEscala(largoContenido, 40)

        texto = CTkLabel(master = contenidoFrame,
                         width = self.obtenerEscala(anchoContenido, 100),
                         height = self.obtenerEscala(largoContenido, 20),
                         text = "Multiprogramación Lotes",
                         font = ("Helvetica", 32))
        
        cantidadFrame = CTkFrame(master = contenidoFrame,
                                 width = cantidadFrameAncho,
                                 height = cantidadFrameLargo,
                                 corner_radius = 0
                                 )
        
        botonFrame = CTkFrame(master = contenidoFrame,
                              width = botonFrameAncho,
                              height = botonFrameLargo,
                              corner_radius = 0)
        
        cantidadFrame.grid_propagate(False)
        botonFrame.grid_propagate(False)
        
        texto.grid(row = 0, column = 0, sticky = "nsew")
        cantidadFrame.grid(row = 1, column = 0, sticky = "nsew")
        botonFrame.grid(row = 2, column = 0, sticky = "nsew")
        
        cantidadFrame.rowconfigure(0, weight = 1)
        cantidadFrame.columnconfigure(0, weight = 1)

        botonFrame.rowconfigure(0, weight = 1)
        botonFrame.columnconfigure(0, weight = 1)

        cantidad = CTkEntry(master = cantidadFrame,
                            width =self.obtenerEscala(50, cantidadFrameAncho),
                            height = self.obtenerEscala(20,  cantidadFrameLargo),
                            placeholder_text = "Cantidad Procesos",
                            font = ("Helvetica", 16),
                            corner_radius = 0)
        
        boton = CTkButton(master = botonFrame,
                           width = self.obtenerEscala(botonFrameAncho, 50),
                           height = self.obtenerEscala(botonFrameLargo, 40),
                           fg_color = self.fondoAzul,
                           text = "Crear",
                           font =("Helvetica", 16),
                           command = lambda : self.continuar(cantidad),
                           corner_radius = 0)

        cantidad.grid(row = 0, column = 0, sticky = "s", pady = (10,10))
        boton.grid(row = 0, column = 0, sticky = "n", pady = (10, 10))

    def continuar(self, Widget):

        valor = int(Widget.get())

        if(valor <= 0):

            return

        for widget in self.app.winfo_children():

            widget.destroy() 

        self.generarFrames(self.app)

        self.Multiprogramacion = Multiprogramacion.Lotes(valor, 
                                                         self.nuevosContenedor,
                                                         self.listosContenedor,
                                                         self.ejecucionContenedor,
                                                         self.terminadosContenedor,
                                                         self.tituloReloj,
                                                         self.tituloPendientes)
                                                
    def generarFrames(self, Ventana):

        Ventana.rowconfigure(0, weight = 1)
        Ventana.rowconfigure(1, weight = 1)
        Ventana.columnconfigure(0, weight = 1)

        primerFrameAncho = self.obtenerEscala(self.ventanaAncho, 100) 
        primerFrameLargo = self.obtenerEscala(self.ventanaLargo, 60)

        segundoFrameAncho = self.obtenerEscala(self.ventanaAncho, 100)
        segundoFrameLargo = self.obtenerEscala(self.ventanaLargo, 40)

        primerFrame = CTkFrame(master = Ventana,
                               width = primerFrameAncho,
                               height = primerFrameLargo)

        segundoFrame = CTkFrame(master = Ventana,
                                width = segundoFrameAncho,
                                height = segundoFrameLargo)
        
        primerFrame.grid(row = 0, column = 0, sticky = "nsew", padx = 10, pady = 5)
        segundoFrame.grid(row = 1, column = 0, sticky = "nsew", padx = 10, pady = 5)
        
        self.generarContenido(primerFrame, primerFrameAncho, primerFrameLargo)
        self.cajaTexto(segundoFrame, segundoFrameAncho, segundoFrameLargo)

    def generarContenido(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)
        Frame.columnconfigure(1, weight = 1)
        Frame.columnconfigure(2, weight = 1)

        contenedoresAncho = self.obtenerEscala(Ancho, 33)
        contenedoresLargo = self.obtenerEscala(Largo, 100)

        Nuevos = CTkFrame(master = Frame,
                       width = contenedoresAncho,
                       height = contenedoresLargo,
                       fg_color = self.colorFondo
                       )
        
        Pendientes = CTkFrame(master = Frame,
                              width = contenedoresAncho,
                              height = contenedoresLargo,
                              fg_color = "#2B2B2B")

        Terminados = CTkFrame(master = Frame,
                              width = contenedoresAncho,
                              height = contenedoresLargo,
                              fg_color = self.colorFondo
                              )
        
        Nuevos.grid(row = 0, column = 0, sticky = "nsew")
        Pendientes.grid(row = 0, column = 1, sticky = "nsew", padx = 20)
        Terminados.grid(row = 0, column = 2, sticky = "nsew")

        self.generarNuevos(Nuevos, contenedoresAncho, contenedoresLargo)
        self.generarPendientes(Pendientes, contenedoresAncho, contenedoresLargo)
        self.generarTerminados(Terminados, contenedoresAncho, contenedoresLargo)

    def generarNuevos(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 0)
        Frame.rowconfigure(1, weight = 1)
        Frame.columnconfigure(0, weight = 1)    

        encabezadoAncho = self.obtenerEscala(Ancho, 100)
        encabezadoLargo = self.obtenerEscala(Largo, 5)

        nuevosAncho = self.obtenerEscala(Ancho, 100)
        nuevosLargo = self.obtenerEscala(Largo, 95)
        
        encabezado = CTkFrame(master = Frame,
                          width = encabezadoAncho,
                          height = encabezadoLargo)
        
        self.nuevosContenedor = CTkScrollableFrame(master = Frame,
                                              width = nuevosAncho,
                                              height = nuevosLargo,
                                              fg_color = self.colorFondo)
        
        encabezado.grid(row = 0, column = 0, sticky = "nsew")
        self.nuevosContenedor.grid(row = 1, column = 0, sticky = "nsew")

        #Modificar el contenedor encabezado para contener los lotes restantes.

        encabezado.rowconfigure(0, weight = 1)
        encabezado.columnconfigure(0, weight = 1)
        encabezado.columnconfigure(1, weight = 1)

        tituloAncho = self.obtenerEscala(encabezadoAncho, 50)
        tituloLargo = self.obtenerEscala(encabezadoLargo, 100)

        imagenNuevos = CTkImage(light_image = Image.open("Frontend/Imagenes/Nuevos.png"),
                          dark_image = Image.open("Frontend/Imagenes/Nuevos.png"),
                          size = (16, 16))
        
        tituloNuevo = CTkLabel(master = encabezado,
                          width = tituloAncho,
                          height = tituloLargo,
                          fg_color = self.primerGris,
                          text = " Nuevos",
                          font = ("Helvetica", 14),
                          anchor = "w",
                          image = imagenNuevos,
                          compound = "left")

        imagenRestantes = CTkImage(light_image = Image.open("Frontend/Imagenes/Restantes.png"),
                          dark_image = Image.open("Frontend/Imagenes/Restantes.png"),
                          size = (16, 16))
        
        self.tituloPendientes = CTkLabel(master = encabezado,
                          width = tituloAncho,
                          height = tituloLargo,
                          fg_color = self.primerGris,
                          text = " Lotes Retantes: ",
                          font = ("Helvetica", 14),
                          anchor = "e",
                          image = imagenRestantes,
                          compound = "left")
        
        tituloNuevo.grid(row = 0, column = 0, sticky = "nsew")    
        self.tituloPendientes.grid(row = 0, column = 1, sticky = "nsew")        

    def generarPendientes(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 1)
        Frame.rowconfigure(1, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        listosAncho = self.obtenerEscala(Ancho, 100)
        listosLargo = self.obtenerEscala(Largo, 60)

        ejecucionAncho = self.obtenerEscala(Ancho, 100)
        ejecucionLargo = self.obtenerEscala(Largo, 40)

        Listos = CTkFrame(master = Frame,
                          width = listosAncho,
                          height = listosLargo,
                          corner_radius = 0
                          ) 
        
        Ejecucion = CTkFrame(master = Frame,
                             width = ejecucionAncho,
                             height = ejecucionLargo,
                             corner_radius = 0
                             )
        
        Listos.grid(row = 0, column = 0, sticky = "nsew", pady = (0, 5))
        Ejecucion.grid(row = 1, column = 0, sticky = "nsew")

        self.generarListos(Listos, listosAncho, listosLargo)
        self.generarEjecucion(Ejecucion, ejecucionAncho, ejecucionLargo)

    def generarListos(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 0)
        Frame.rowconfigure(1, weight = 1)
        Frame.columnconfigure(0, weight = 1)    

        encabezadoAncho = self.obtenerEscala(Ancho, 100)
        encabezadoLargo = self.obtenerEscala(Largo, 5)

        listoAncho = self.obtenerEscala(Ancho, 100)
        listosLargo = self.obtenerEscala(Largo, 95)

        encabezado = CTkFrame(master = Frame,
                          width = encabezadoAncho,
                          height = encabezadoLargo,
                          corner_radius = 0)
        
        self.listosContenedor = CTkScrollableFrame(master = Frame,
                                              width = listoAncho,
                                              height = listosLargo,
                                              fg_color = self.colorFondo,
                                              corner_radius = 0)
        
        encabezado.grid(row = 0, column = 0, sticky = "nsew")
        self.listosContenedor.grid(row = 1, column = 0, sticky = "nsew")

        #Modificar el contenedor encabezado para contener los lotes restantes.

        encabezado.rowconfigure(0, weight = 1)
        encabezado.columnconfigure(0, weight = 1)

        tituloAncho = self.obtenerEscala(encabezadoAncho, 100)
        tituloLargo = self.obtenerEscala(encabezadoLargo, 100)

        imagenNuevos = CTkImage(light_image = Image.open("Frontend/Imagenes/Listos.png"),
                          dark_image = Image.open("Frontend/Imagenes/Listos.png"),
                          size = (16, 16))
        
        tituloNuevo = CTkLabel(master = encabezado,
                          width = tituloAncho,
                          height = tituloLargo,
                          fg_color = self.primerGris,
                          text = " Listos",
                          font = ("Helvetica", 14),
                          anchor = "w",
                          image = imagenNuevos,
                          compound = "left")
        
        tituloNuevo.grid(row = 0, column = 0, sticky = "nsew")  
        
    def generarEjecucion(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 0)
        Frame.rowconfigure(1, weight = 1)
        Frame.columnconfigure(0, weight = 1)    

        encabezadoAncho = self.obtenerEscala(Ancho, 100)
        encabezadoLargo = self.obtenerEscala(Largo, 5)

        ejecucionAncho = self.obtenerEscala(Ancho, 100)
        ejecucionLargo = self.obtenerEscala(Largo, 95)

        encabezado = CTkFrame(master = Frame,
                          width = encabezadoAncho,
                          height = encabezadoLargo,
                          corner_radius = 0)
        
        self.ejecucionContenedor = CTkScrollableFrame(master = Frame,
                                              width = ejecucionAncho,
                                              height = ejecucionLargo,
                                              fg_color = self.colorFondo,
                                              corner_radius = 0)
        
        encabezado.grid(row = 0, column = 0, sticky = "nsew")
        self.ejecucionContenedor.grid(row = 1, column = 0, sticky = "nsew")

        #Modificar el contenedor encabezado para contener los lotes restantes.

        encabezado.rowconfigure(0, weight = 1)
        encabezado.columnconfigure(0, weight = 1)

        tituloAncho = self.obtenerEscala(encabezadoAncho, 100)
        tituloLargo = self.obtenerEscala(encabezadoLargo, 100)

        imagenEjecucion = CTkImage(light_image = Image.open("Frontend/Imagenes/Ejecucion.png"),
                          dark_image = Image.open("Frontend/Imagenes/Ejecucion.png"),
                          size = (16, 16))
        
        tituloEjecucion = CTkLabel(master = encabezado,
                          width = tituloAncho,
                          height = tituloLargo,
                          fg_color = self.primerGris,
                          text = " Ejecucion",
                          font = ("Helvetica", 14),
                          anchor = "w",
                          image = imagenEjecucion,
                          compound = "left")
        
        tituloEjecucion.grid(row = 0, column = 0, sticky = "nsew")    

    def generarTerminados(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 0)
        Frame.rowconfigure(1, weight = 1)
        Frame.columnconfigure(0, weight = 1)    

        encabezadoAncho = self.obtenerEscala(Ancho, 100)
        encabezadoLargo = self.obtenerEscala(Largo, 5)

        terminadosAncho = self.obtenerEscala(Ancho, 100)
        terminadosLargo = self.obtenerEscala(Largo, 95)
        
        encabezado = CTkFrame(master = Frame,
                          width = encabezadoAncho,
                          height = encabezadoLargo)
        
        self.terminadosContenedor = CTkScrollableFrame(master = Frame,
                                              width = terminadosAncho,
                                              height = terminadosLargo,
                                              fg_color = self.colorFondo)
        
        encabezado.grid(row = 0, column = 0, sticky = "nsew")
        self.terminadosContenedor.grid(row = 1, column = 0, sticky = "nsew")

        encabezado.rowconfigure(0, weight = 1)
        encabezado.columnconfigure(0, weight = 1)
        encabezado.columnconfigure(1, weight = 1)

        tituloAncho = self.obtenerEscala(encabezadoAncho, 50)
        tituloLargo = self.obtenerEscala(encabezadoLargo, 100)

        imagenTerminados = CTkImage(light_image = Image.open("Frontend/Imagenes/Terminados.png"),
                          dark_image = Image.open("Frontend/Imagenes/Terminados.png"),
                          size = (16, 16))
        
        tituloTerminados = CTkLabel(master = encabezado,
                          width = tituloAncho,
                          height = tituloLargo,
                          fg_color = self.primerGris,
                          text = " Terminados",
                          font = ("Helvetica", 14),
                          anchor = "w",
                          image = imagenTerminados,
                          compound = "left")

        imagenRestantes = CTkImage(light_image = Image.open("Frontend/Imagenes/Reloj.png"),
                          dark_image = Image.open("Frontend/Imagenes/Reloj.png"),
                          size = (16, 16))
        
        self.tituloReloj = CTkLabel(master = encabezado,
                          width = tituloAncho,
                          height = tituloLargo,
                          fg_color = self.primerGris,
                          text = " Reloj: ",
                          font = ("Helvetica", 14),
                          anchor = "e",
                          image = imagenRestantes,
                          compound = "left")
        
        tituloTerminados.grid(row = 0, column = 0, sticky = "nsew")    
        self.tituloReloj.grid(row = 0, column = 1, sticky = "nsew")           
        
    def cajaTexto(self, Frame, Ancho, Largo):

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
        Contenido.insert("3.0", "E: Interrupcion Entrada/Salida\n")
        Contenido.insert("4.0", "W: Error\n")
        Contenido.insert("5.0", "P: Pausa\n")
        Contenido.insert("6.0", "C: Continuar\n\n")
        #Contenido.insert("8.0", "Las teclas seran detectadas al presionar [Enter]\n\n")

        Contenido.bind("<KeyPress>", lambda event: self.Enter(event.char))

        Titulo.grid(row = 0, column = 0, sticky = "nsew")
        Contenido.grid(row = 1, column = 0, sticky = "nsew")    

    def Enter(self, Caracter):

        #Opciones del Backend

        self.Multiprogramacion.asignarTecla(Caracter) 
