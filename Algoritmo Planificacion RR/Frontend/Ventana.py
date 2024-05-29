from customtkinter import *
from CTkTable import *
from PIL import Image

from Backend import RR

class Ventana:

    def __init__(self):

        self.app = CTk()
        self.ventanaAncho = self.obtenerAncho(self.app, 70)
        self.ventanaLargo = self.obtenerLargo(self.app, 70)
        self.app.after(201, lambda : self.app.iconbitmap("Frontend/Imagenes/Icono.ico"))
        self.app.title("Algoritmo Planificación RR")

        self.app.geometry(f"{self.ventanaAncho}x{self.ventanaLargo}")

        #Duracion Quantum RR

        self.Quantum = None

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

            self.Servicio.detener()

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
        cantidadFrameLargo = self.obtenerEscala(largoContenido, 60)

        botonFrameAncho = self.obtenerEscala(anchoContenido, 100)
        botonFrameLargo = self.obtenerEscala(largoContenido, 40)

        texto = CTkLabel(master = contenidoFrame,
                         width = self.obtenerEscala(anchoContenido, 100),
                         height = self.obtenerEscala(largoContenido, 20),
                         text = "Algoritmo Planificación RR",
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
        #cantidadFrame.rowconfigure(1, weight  = 1)
        cantidadFrame.columnconfigure(0, weight = 1)

        botonFrame.rowconfigure(0, weight = 1)
        botonFrame.columnconfigure(0, weight = 1)

        cantidad = CTkEntry(master = cantidadFrame,
                            width =self.obtenerEscala(50, cantidadFrameAncho),
                            height = self.obtenerEscala(20,  cantidadFrameLargo),
                            placeholder_text = "Cantidad Procesos",
                            font = ("Helvetica", 16),
                            corner_radius = 0)
        
        quantum = CTkEntry(master = cantidadFrame,
                            width =self.obtenerEscala(50, cantidadFrameAncho),
                            height = self.obtenerEscala(20,  cantidadFrameLargo),
                            placeholder_text = "Duracion Quantum",
                            font = ("Helvetica", 16),
                            corner_radius = 0)
        
        boton = CTkButton(master = botonFrame,
                           width = self.obtenerEscala(botonFrameAncho, 50),
                           height = self.obtenerEscala(botonFrameLargo, 40),
                           fg_color = self.fondoAzul,
                           text = "Crear",
                           font =("Helvetica", 16),
                           command = lambda : self.continuar(cantidad, quantum),
                           corner_radius = 0)

        cantidad.grid(row = 0, column = 0, sticky = "s", pady = (0, 15))
        quantum.grid(row = 1, column = 0, sticky = "s", pady = (0, 15))
        boton.grid(row = 0, column = 0, sticky = "n")

    def continuar(self, Cantidad, Quantum):

        valorCantidad = int(Cantidad.get())
        quantumCantidad = int(Quantum.get())

        if(valorCantidad <= 0 or quantumCantidad <= 0):

            return
        
        self.Quantum = quantumCantidad

        for widget in self.app.winfo_children():

            widget.destroy() 

        self.generarFrames(self.app)

        self.Servicio = RR.sistemOperativo(self.app,
                                             valorCantidad,
                                             quantumCantidad,
                                             self.nuevosContenedor,
                                             self.listosContenedor,
                                             self.ejecucionContenedor,
                                             self.bloqueadosContenedor,
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

        nuevosAncho = self.obtenerEscala(Ancho, 33)
        nuevosLargo = self.obtenerEscala(Largo, 100)

        pendientesAncho = self.obtenerEscala(Ancho, 33)
        pendientesLargo = self.obtenerEscala(Largo, 100)

        contenedoresAncho = self.obtenerEscala(Ancho, 33)
        contenedoresLargo = self.obtenerEscala(Largo, 100)

        Nuevos = CTkFrame(master = Frame,
                       width = nuevosAncho,
                       height = nuevosLargo,
                       fg_color = self.colorFondo
                       )
        
        Pendientes = CTkFrame(master = Frame,
                              width = pendientesAncho,
                              height = pendientesLargo,
                              fg_color = "#2B2B2B")

        Terminados = CTkFrame(master = Frame,
                              width = contenedoresAncho,
                              height = contenedoresLargo,
                              fg_color = self.colorFondo
                              )
        
        Nuevos.grid(row = 0, column = 0, sticky = "nsew")
        Pendientes.grid(row = 0, column = 1, sticky = "nsew", padx = 20)
        Terminados.grid(row = 0, column = 2, sticky = "nsew")

        self.generarNuevos(Nuevos, nuevosAncho, nuevosLargo)
        self.generarPendientes(Pendientes, pendientesAncho, pendientesLargo)
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

        #Modificar el contenedor encabezado para contener los procesos restantes.

        encabezado.rowconfigure(0, weight = 1)
        encabezado.columnconfigure(0, weight = 1)
        encabezado.columnconfigure(1, weight = 1)

        tituloNuevoAncho = self.obtenerEscala(encabezadoAncho, 30)
        tituloNuevoLargo = self.obtenerEscala(encabezadoLargo, 100)

        tituloProcesosAncho = self.obtenerEscala(encabezadoAncho, 70)
        tituloProcesosLargo = self.obtenerEscala(encabezadoLargo, 100)

        imagenNuevos = CTkImage(light_image = Image.open("Frontend/Imagenes/Nuevos.png"),
                          dark_image = Image.open("Frontend/Imagenes/Nuevos.png"),
                          size = (16, 16))
        
        tituloNuevo = CTkLabel(master = encabezado,
                          width = tituloNuevoAncho,
                          height = tituloNuevoLargo,
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
                          width = tituloProcesosAncho,
                          height = tituloProcesosLargo,
                          fg_color = self.primerGris,
                          text = " Procesos Restantes: ",
                          font = ("Helvetica", 14),
                          anchor = "e",
                          image = imagenRestantes,
                          compound = "left")
        
        tituloNuevo.grid(row = 0, column = 0, sticky = "nsew")    
        self.tituloPendientes.grid(row = 0, column = 1, sticky = "nsew")        

    def generarPendientes(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 1)
        Frame.rowconfigure(1, weight = 1)
        Frame.rowconfigure(2, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        listosAncho = self.obtenerEscala(Ancho, 100)
        listosLargo = self.obtenerEscala(Largo, 33)

        ejecucionAncho = self.obtenerEscala(Ancho, 100)
        ejecucionLargo = self.obtenerEscala(Largo, 33)

        bloqueadoAncho = self.obtenerEscala(Ancho, 100)
        bloqueadoLargo = self.obtenerEscala(Largo, 33)

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
        
        Bloqueados = CTkFrame(master = Frame,
                              width = bloqueadoAncho,
                              height = bloqueadoLargo,
                              corner_radius = 0)
        
        Listos.grid(row = 0, column = 0, sticky = "nsew", pady = (0, 5))
        Ejecucion.grid(row = 1, column = 0, sticky = "nsew")
        Bloqueados.grid(row = 2, column = 0, sticky = "nsew", pady =(5, 0))

        self.generarListos(Listos, listosAncho, listosLargo)
        self.generarEjecucion(Ejecucion, ejecucionAncho, ejecucionLargo)
        self.generarBloqueados(Bloqueados, bloqueadoAncho, bloqueadoLargo)

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

        #Modificar el contenedor encabezado para contener los procesos restantes.

        encabezado.rowconfigure(0, weight = 1)
        encabezado.columnconfigure(0, weight = 1)
        encabezado.columnconfigure(1, weight = 1)

        tituloEjecucionAncho = self.obtenerEscala(encabezadoAncho, 50)
        tituloEjecucionLargo = self.obtenerEscala(encabezadoLargo, 100)

        tituloQuantumAncho = self.obtenerEscala(encabezadoAncho, 50)
        tituloQuantumLargo = self.obtenerEscala(encabezadoLargo, 100)

        imagenEjecucion = CTkImage(light_image = Image.open("Frontend/Imagenes/Ejecucion.png"),
                          dark_image = Image.open("Frontend/Imagenes/Ejecucion.png"),
                          size = (16, 16))
        
        tituloEjecucion = CTkLabel(master = encabezado,
                          width = tituloEjecucionAncho,
                          height = tituloEjecucionLargo,
                          fg_color = self.primerGris,
                          text = " Ejecucion",
                          font = ("Helvetica", 14),
                          anchor = "w",
                          image = imagenEjecucion,
                          compound = "left")
        
        imagenQuantum = CTkImage(light_image = Image.open("Frontend/Imagenes/RR.png"),
                                 dark_image = Image.open("Frontend/Imagenes/RR.png"),
                                 size = (16, 16))
        
        tituloQuantum = CTkLabel(master = encabezado,
                          width = tituloQuantumAncho,
                          height = tituloQuantumLargo,
                          fg_color = self.primerGris,
                          text = " Quantum: {} ".format(self.Quantum),
                          font = ("Helvetica", 14),
                          anchor = "e",
                          image = imagenQuantum,
                          compound = "left")        
        
        tituloEjecucion.grid(row = 0, column = 0, sticky = "nsew")
        tituloQuantum.grid(row = 0, column = 1, sticky = "nsew")  

    def generarBloqueados(self, Frame, Ancho, Largo):

        Frame.rowconfigure(0, weight = 0)
        Frame.rowconfigure(1, weight = 1)
        Frame.columnconfigure(0, weight = 1)    

        encabezadoAncho = self.obtenerEscala(Ancho, 100)
        encabezadoLargo = self.obtenerEscala(Largo, 5)

        bloqueadosAncho = self.obtenerEscala(Ancho, 100)
        bloqueadosLargo = self.obtenerEscala(Largo, 95)

        encabezado = CTkFrame(master = Frame,
                          width = encabezadoAncho,
                          height = encabezadoLargo,
                          corner_radius = 0)
        
        self.bloqueadosContenedor = CTkScrollableFrame(master = Frame,
                                              width = bloqueadosAncho,
                                              height = bloqueadosLargo,
                                              fg_color = self.colorFondo,
                                              corner_radius = 0)
        
        encabezado.grid(row = 0, column = 0, sticky = "nsew")
        self.bloqueadosContenedor.grid(row = 1, column = 0, sticky = "nsew")

        #Modificar el contenedor encabezado para contener los procesos restantes.

        encabezado.rowconfigure(0, weight = 1)
        encabezado.columnconfigure(0, weight = 1)

        tituloAncho = self.obtenerEscala(encabezadoAncho, 100)
        tituloLargo = self.obtenerEscala(encabezadoLargo, 100)

        imagenEjecucion = CTkImage(light_image = Image.open("Frontend/Imagenes/Bloqueados.png"),
                          dark_image = Image.open("Frontend/Imagenes/Bloqueados.png"),
                          size = (16, 16))
        
        tituloEjecucion = CTkLabel(master = encabezado,
                          width = tituloAncho,
                          height = tituloLargo,
                          fg_color = self.primerGris,
                          text = " Bloqueados",
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
        Contenido.insert("7.0", "N: Nuevo\n\n")
        Contenido.insert("8.0", "B: Tabla Control Procesos\n\n")

        Contenido.bind("<KeyPress>", lambda event: self.Enter(event.char))

        Titulo.grid(row = 0, column = 0, sticky = "nsew")
        Contenido.grid(row = 1, column = 0, sticky = "nsew")    

    def Enter(self, Caracter):

        #Opciones del Backend

        self.Servicio.asignarTecla(Caracter) 
