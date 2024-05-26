from Backend import Proceso
from customtkinter import *
from CTkTable import *
import threading
import time

class Lotes:

    def __init__(self, Cantidad, frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameProcesos):

        self.cantidadProcesos = Cantidad
        self.procesosNuevos = [Proceso.Proceso(i) for i in range(Cantidad)]
        self.procesosListos = []
        self.procesosEjecucion = []
        self.procesosBloqueados = []
        self.procesosTerminados = []
        self.Tiempo = 0

        self.fondoAzul = "#1565C0"

        self.Tecla = ""
        self.Estado = True    

        self._stop_event = threading.Event()
        self.iniciar(frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameProcesos)

    def iniciar(self, frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameProcesos):  

        self.Contador = threading.Thread(target=self.ejecutar, daemon = True, args=(frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameProcesos))
        self.Contador.start()

    def detener(self):

        self._stop_event.set()
        self.Contador.join(timeout=0)      

    def ejecutar(self, frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameProcesos):

        self.recalcular(frameProcesos) # Carga los lotes en Listo y Ejecucion
        self.modificarNuevos(frameNuevos)
        self.modificarListos(frameListos)
        self.modificarEjecucion(frameEjecucion)
        self.modificarTerminados(frameTerminados)

        frameProcesos.configure(text = " Procesos Restantes: {} ".format(self.cantidadProcesos))

        while (not self._stop_event.is_set()):

            while(self.Estado):

                time.sleep(1)

                self.Tiempo += 1
                frameTiempo.configure(text=" Reloj: {} ".format(str(self.Tiempo)))

                self.procesosEjecucion[0].asignarTiempoEjecutado(self.procesosEjecucion[0].obtenerTiempoEjecutado() + 1)
                self.tablaEjecucion.insert(1,2,self.procesosEjecucion[0].obtenerTiempoEjecutado())

                #Al agotarse el tiempo de ejecucion hacer un swap mandar el ejecutado a terminado y uno de listo a ejecucion.

                if(self.procesosEjecucion[0].obtenerTiempoEjecutado() >= self.procesosEjecucion[0].obtenerTiempoEstimado()):

                    Estado = self.removerEjecutado(frameProcesos)

                    if(Estado): # Validar si el programa se acaba, en dado caso retorna verdadero

                        return
                    
                if(self.Tecla != None):

                    self.obtenerInput(self.Tecla, frameProcesos)

                    self.Tecla = None                                    

            if(self.Tecla != None):

                self.obtenerInput(self.Tecla, frameProcesos)

                self.Tecla = None                                    
                        
    def recalcular(self, frameProcesos):

       procesosDisponibles = len(self.procesosNuevos)
       memoriaDisponible = 4 - (len(self.procesosEjecucion) + len(self.procesosListos) + len(self.procesosBloqueados))
         
       # Cargar todos los nuevos procesos hasta que mi memoria sea llenada.

       for i in range(memoriaDisponible):
           
           if(procesosDisponibles > 0):
               
                self.procesosListos.append(self.procesosNuevos.pop(0))
                procesosDisponibles = len(self.procesosNuevos)
                self.cantidadProcesos -= 1

        # Introduzco un dato de la lista de listos a ejecución.

       if(len(self.procesosListos) > 0):

            self.procesosEjecucion.append(self.procesosListos.pop(0))
              
       frameProcesos.configure(text = " Proceos Retantes: {} ".format(self.cantidadProcesos))    

    def removerEjecutado(self, frameProcesos):

        # Sacar el proceso de ejcucion a terminados.

        self.agregarTerminados(self.procesosEjecucion.pop(0))

        # Meter otro proceso a ejecucion (siempre que exista)

        if(len(self.procesosListos) > 0):

            self.tablaListos.delete_row(1)
            self.procesosEjecucion.append(self.procesosListos.pop(0))
            datosTemporales = self.procesosEjecucion[0].obtenerEjecuccion()

            for i in range(len(datosTemporales)):

                self.tablaEjecucion.insert(1, i, datosTemporales[i])

        self.recalcular(frameProcesos)
        self.actualizarNuevos()
        self.agregarListos()
    
        '''

        else:   

            if(len(self.procesosListos) <= 0 and len(self.procesosNuevos) <= 0): # Fin

                self.tablaEjecucion.delete_row(1)
                return True    

        '''                    
        
    def intercambiar(self):

        if(len(self.procesosListos) > 0):

            #Agregar el dato en ejecucion a listos

            self.tablaListos.delete_row(1)
            datosTemporales = self.procesosEjecucion[0].obtenerEjecuccion()
            self.procesosListos.append(self.procesosEjecucion.pop(0))
            self.tablaListos.add_row(datosTemporales) 

            #Agregar el siguiente dato a ejecucion

            self.procesosEjecucion.append(self.procesosListos.pop(0))
            datosTemporales = self.procesosEjecucion[0].obtenerEjecuccion()

            for i in range(len(datosTemporales)):

                self.tablaEjecucion.insert(1, i, datosTemporales[i])

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

        self.tablaNuevos = CTkTable(master = Frame,
                         row = len(datosTabla),
                         column = len(datosTabla[0]),
                         header_color = self.fondoAzul,
                         values = datosTabla,
                         corner_radius = 0)
        
        self.tablaNuevos.grid(row = 0, column = 0, sticky = "nsew") 

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

        self.tablaListos = CTkTable(master = Frame,
                         row = len(datosTabla),
                         column = len(datosTabla[0]),
                         header_color = self.fondoAzul,
                         values = datosTabla,
                         corner_radius = 0)
        
        self.tablaListos.grid(row = 0, column = 0, sticky = "nsew", pady = (6,0), padx = (6, 0))    

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
                         header_color = self.fondoAzul,
                         values = datosTabla,
                         corner_radius = 0)
        
        self.tablaEjecucion.grid(row = 0, column = 0, sticky = "nsew", pady = (6,0), padx = (6, 0))    
       
    def modificarTerminados(self, Frame):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        datosTabla = [["ID", "T/ Est", "T/ Eje", "1°N", "Op", "2°N", "Res"]]

        self.tablaTerminados = CTkTable(master = Frame,
                         row = len(datosTabla),
                         column = len(datosTabla[0]),
                         header_color = self.fondoAzul,
                         values = datosTabla,
                         corner_radius = 0)
        
        self.tablaTerminados.grid(row = 0, column = 0, sticky = "nsew")   

    def agregarTerminados(self, Informacion):

        self.tablaTerminados.add_row(Informacion.obtenerTodo())

    def agregarListos(self):

        if(len(self.procesosNuevos) > 0):

            self.tablaListos.add_row(self.procesosListos[len(self.procesosListos) - 1].obtenerEjecuccion())

    def actualizarNuevos(self):

        if(len(self.procesosNuevos) > 0):

            self.tablaNuevos.delete_row(1)

    def actualizarEjecucion(self):

        self.tablaEjecucion.delete_row(1)
        self.tablaEjecucion.add_row(self.procesosEjecucion[0].obtenerEjecuccion())   

    def obtenerInput(self, Caracter, frameProcesos):

        Caracter = Caracter.upper()

        if(Caracter == "W" and self.Estado):
            
            self.procesosEjecucion[0].asignarResultado("ERROR")
            self.removerEjecutado(frameProcesos)

        elif(Caracter == "E"  and self.Estado):

            self.intercambiar()

        elif(Caracter == "P"):

            self.Estado = False

        elif(Caracter == "C"):   

            self.Estado = True

    def asignarTecla(self, Tecla):

        self.Tecla = Tecla
        print(self.Tecla)    
