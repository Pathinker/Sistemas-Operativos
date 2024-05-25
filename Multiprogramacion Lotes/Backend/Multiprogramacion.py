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

        self.Tecla = ""
        self.Estado = True    

        self._stop_event = threading.Event()
        self.iniciar(frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameLotes)

    def iniciar(self, frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameLotes):  

        self.Contador = threading.Thread(target=self.ejecutar, daemon = True, args=(frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameLotes))
        self.Contador.start()

    def detener(self):

        self._stop_event.set()
        self.Contador.join()      

    def ejecutar(self, frameNuevos, frameListos, frameEjecucion, frameTerminados, frameTiempo, frameLotes):

        self.recalcular(frameLotes) # Carga los lotes en Listo y Ejecucion
        self.modificarNuevos(frameNuevos)
        self.modificarListos(frameListos)
        self.modificarEjecucion(frameEjecucion)
        self.modificarTerminados(frameTerminados)

        frameLotes.configure(text = " Lotes Retantes: {} ".format(self.cantidadLotes))

        while (not self._stop_event.is_set()):

            while(self.Estado):

                time.sleep(1)

                self.Tiempo += 1
                frameTiempo.configure(text=" Reloj: {} ".format(str(self.Tiempo)))

                self.procesosEjecucion[0].asignarTiempoEjecutado(self.procesosEjecucion[0].obtenerTiempoEjecutado() + 1)
                self.tablaEjecucion.insert(1,2,self.procesosEjecucion[0].obtenerTiempoEjecutado())

                #Al agotarse el tiempo de ejecucion hacer un swap mandar el ejecutado a terminado y uno de listo a ejecucion.

                if(self.procesosEjecucion[0].obtenerTiempoEjecutado() >= self.procesosEjecucion[0].obtenerTiempoEstimado()):

                    Estado = self.removerEjecutado(frameLotes)

                    if(Estado): # Validar si el programa se acaba, en dado caso retorna verdadero

                        return
                    
                if(self.Tecla != None):

                    self.obtenerInput(self.Tecla, frameLotes)

                    self.Tecla == None                                    

            if(self.Tecla != None):

                self.obtenerInput(self.Tecla, frameLotes)

                self.Tecla == None                                    
                        
    def recalcular(self, frameLotes):

       procesosDisponibles = len(self.procesosNuevos)

       self.cantidadLotes -= 1

       frameLotes.configure(text = " Lotes Retantes: {} ".format(self.cantidadLotes))

       if(procesosDisponibles >= 4): #Caso Especial de que tengo menos de 4 procesos.

            for i in range (4):

                self.procesosListos.append(self.procesosNuevos.pop(0))

            self.procesosEjecucion.append(self.procesosListos.pop(0))

       else:

            for i in range(procesosDisponibles):

                self.procesosListos.append(self.procesosNuevos.pop(0))

            self.procesosEjecucion.append(self.procesosListos.pop(0)) 

    def removerEjecutado(self, frameLotes):
    
        self.agregarTerminados(self.procesosEjecucion.pop(0))

        if(len(self.procesosListos) > 0):

            self.tablaListos.delete_row(1)
            self.procesosEjecucion.append(self.procesosListos.pop(0))
            datosTemporales = self.procesosEjecucion[0].obtenerEjecuccion()

            for i in range(len(datosTemporales)):

                self.tablaEjecucion.insert(1, i, datosTemporales[i])

        else:

            if(len(self.procesosListos) <= 0 and len(self.procesosNuevos) <= 0): # Fin

                self.tablaEjecucion.delete_row(1)
                return True                
                    
            self.recalcular(frameLotes)
            self.actualizarNuevos()
            self.agregarListos()
            self.actualizarEjecucion()  

    def intercambiar(self):

        if(len(self.procesosListos) > 0):

            self.tablaListos.delete_row(1)
            self.procesosEjecucion.append(self.procesosListos.pop(0))
            datosTemporales = self.procesosEjecucion[0].obtenerEjecuccion()

            for i in range(len(datosTemporales)):

                self.tablaEjecucion.insert(1, i, datosTemporales[i])

            datosTemporales = self.procesosEjecucion[0].obtenerEjecuccion()
            self.tablaListos.add_row(datosTemporales) 

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
                         values = datosTabla,
                         corner_radius = 0)
        
        '''
        
        for i in range(len(datosTabla)):

            Color = None
            Fila = i + 1

            if((Fila // 4) % 2 == 0):

                Color = "Blue"

            else:    

                Color = "Red"

            for j in range(len(datosTabla[0])):

               self.tablaNuevos.insert(row = Fila, column = j, value = self.tablaNuevos.get(Fila, j), fg_color = Color)

        '''        

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
                         values = datosTabla,
                         corner_radius = 0)
        
        self.tablaListos.grid(row = 0, column = 0, sticky = "nsew")    

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

        self.tablaTerminados = CTkTable(master = Frame,
                         row = len(datosTabla),
                         column = len(datosTabla[0]),
                         values = datosTabla,
                         corner_radius = 0)
        
        self.tablaTerminados.grid(row = 0, column = 0, sticky = "nsew")   

    def agregarTerminados(self, Informacion):

        self.tablaTerminados.add_row(Informacion.obtenerTodo())

    def agregarListos(self):

        for i in range(len(self.procesosListos)):

            self.tablaListos.add_row(self.procesosListos[i].obtenerEjecuccion())

    def actualizarNuevos(self):

        cantidadIngresada = len(self.procesosListos) + len(self.procesosEjecucion)

        for i in range(cantidadIngresada):

            self.tablaNuevos.delete_row(1)

    def actualizarEjecucion(self):

        self.tablaEjecucion.delete_row(1)
        self.tablaEjecucion.add_row(self.procesosEjecucion[0].obtenerEjecuccion())   

    def estadoError(self):

        pass

    def obtenerInput(self, Caracter, frameLotes):

        Caracter = Caracter.upper()

        if(Caracter == "W" and self.Estado):
            
            self.procesosEjecucion[0].asignarResultado("ERROR")
            self.removerEjecutado(frameLotes)

        elif(Caracter == "E"  and self.Estado):

            self.intercambiar()

        elif(Caracter == "P"):

            self.Estado = False

        elif(Caracter == "C"):   

            self.Estado = True

    def asignarTecla(self, Tecla):

        self.Tecla = Tecla
        print(self.Tecla)    
