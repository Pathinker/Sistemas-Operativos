from Backend import Lote
from customtkinter import *
from CTkTable import *
import threading
import time

class Lotes:

    def __init__(self, Cantidad, frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameLotes):

        self.cantidadLotes = Cantidad // 4 + 1
        self.procesosNuevos = [Lote.Lote(i) for i in range(Cantidad)]
        self.procesosListos = []
        self.procesosEjecucion = []
        self.procesosBloqueados = []
        self.procesosTerminados = []
        self.Tiempo = 0    

        self._stop_event = threading.Event()
        self.iniciar(frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameLotes)

    def iniciar(self, frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameLotes):  

        self.Contador = threading.Thread(target=self.ejecutar, args=(frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameLotes))
        self.Contador.start()

    def detener(self):

        self._stop_event.set()
        self.Contador.join()      

    def ejecutar(self, frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameLotes):

        self.calcularInicio()
        self.modificarNuevos(frameNuevos)
        self.modificarListos(frameListos)
        self.modificarEjecucion(frameEjecucion)
        self.modificarTerminados(frameTerminados)

        frameLotes.configure(text = " Lotes Retantes: {} ".format(self.cantidadLotes))

        while not self._stop_event.is_set():

            time.sleep(1)

            self.Tiempo += 1
            frameTiempo.configure(text=" Reloj: {} ".format(str(self.Tiempo)))

            self.procesosEjecucion[0].asignarTiempoEjecutado(self.procesosEjecucion[0].obtenerTiempoEjecutado() + 1)
            self.tablaEjecucion.insert(1,2,self.procesosEjecucion[0].obtenerTiempoEjecutado())

    def calcularInicio(self):

       procesosDisponibles = len(self.procesosNuevos)

       if(procesosDisponibles >= 4): #Caso Especial de que tengo menos de 4 procesos.

            for i in range (4):

                self.procesosListos.append(self.procesosNuevos.pop(0))

            self.procesosEjecucion.append(self.procesosListos.pop(0))

       else:

            for i in range(procesosDisponibles):

                self.procesosListos.append(self.procesosNuevos.pop(0))

            self.procesosEjecucion.append(self.procesosListos.pop(0)) 

    def modificarNuevos(self, Frame):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        Valores = self.procesosNuevos
        datosTabla = [["ID", "T/ Estimado", "T/ Ejecutado"]]

        for i in  Valores:

            Datos = []

            Datos.append(i.obtenerID())
            Datos.append(i.obtenerTiempoEstimado())
            Datos.append(i.obtenerTiempoEjecutado())

            datosTabla.append(Datos)

        tabla = CTkTable(master = Frame,
                         row = len(datosTabla),
                         column = len(datosTabla[0]),
                         values = datosTabla,
                         corner_radius = 0)
        
        tabla.grid(row = 0, column = 0, sticky = "nsew") 

    def modificarListos(self, Frame):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        Valores = self.procesosListos
        datosTabla = [["ID", "T/ Est", "T/ Eje", "1°N", "Op", "2°N"]]

        for i in  Valores:

            Datos = []

            Datos.append(i.obtenerID())
            Datos.append(i.obtenerTiempoEstimado())
            Datos.append(i.obtenerTiempoEjecutado())
            Datos.append(i.obtenerPrimerOperando())
            Datos.append(i.obtenerOperacion())
            Datos.append(i.obtenerSegundoOperando())

            datosTabla.append(Datos)

        tabla = CTkTable(master = Frame,
                         row = len(datosTabla),
                         column = len(datosTabla[0]),
                         values = datosTabla,
                         corner_radius = 0)
        
        tabla.grid(row = 0, column = 0, sticky = "nsew")    

    def modificarEjecucion(self, Frame):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        Valores = self.procesosEjecucion
        datosTabla = [["ID", "T/ Est", "T/ Eje", "1°N", "Op", "2°N"]]

        for i in  Valores:

            Datos = []

            Datos.append(i.obtenerID())
            Datos.append(i.obtenerTiempoEstimado())
            Datos.append(i.obtenerTiempoEjecutado())
            Datos.append(i.obtenerPrimerOperando())
            Datos.append(i.obtenerOperacion())
            Datos.append(i.obtenerSegundoOperando())

            datosTabla.append(Datos)

        self.tablaEjecucion = CTkTable(master = Frame,
                         row = len(datosTabla),
                         column = len(datosTabla[0]),
                         values = datosTabla,
                         corner_radius = 0)
        
        self.tablaEjecucion.grid(row = 0, column = 0, sticky = "nsew")    
       
    def modificarTerminados(self, Frame):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        datosTabla = [["ID", "T/ Est", "T/ Eje", "1°N", "Op", "2°N", "Res"]]

        tabla = CTkTable(master = Frame,
                         row = len(datosTabla),
                         column = len(datosTabla[0]),
                         values = datosTabla,
                         corner_radius = 0)
        
        tabla.grid(row = 0, column = 0, sticky = "nsew")    

    def obtenerInput(self, Lote, Caracter):

        if(Caracter == "W"):
            pass

        elif(Caracter == "E"):
            pass

        elif(Caracter == "P"):
            pass

        elif(Caracter == "C"):   
            pass 
