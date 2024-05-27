from Backend import Proceso
from customtkinter import *
from CTkTable import *
import threading
import time

class sistemOperativo:

    def __init__(self, Cantidad, frameNuevos, frameListos, frameEjecucion,frameBloqueados, frameTerminados, frameTiempo, frameProcesos):

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
        self.iniciar(frameNuevos, frameListos, frameEjecucion,frameBloqueados, frameTerminados, frameTiempo, frameProcesos)

    def iniciar(self, frameNuevos, frameListos, frameEjecucion, frameBloqueados, frameTerminados, frameTiempo, frameProcesos):  

        self.Contador = threading.Thread(target=self.ejecutar, daemon = True, args=(frameNuevos, frameListos, frameEjecucion, frameBloqueados, frameTerminados, frameTiempo, frameProcesos))
        self.Contador.start()

    def detener(self):

        self._stop_event.set()
        self.Contador.join(timeout=0)      

    def ejecutar(self, frameNuevos, frameListos, frameEjecucion, frameBloqueados, frameTerminados, frameTiempo, frameProcesos):

        self.recalcular(frameProcesos) # Carga los lotes en Listo y Ejecucion
        self.modificarNuevos(frameNuevos)
        self.modificarListos(frameListos)
        self.modificarEjecucion(frameEjecucion)
        self.modificarBloqueados(frameBloqueados)
        self.modificarTerminados(frameTerminados)

        frameProcesos.configure(text = " Procesos Restantes: {} ".format(self.cantidadProcesos))

        while (not self._stop_event.is_set()):

            while(self.Estado):

                if(len(self.procesosEjecucion) > 0): #Validar que no tenga todos bloqueados

                    if(self.procesosEjecucion[0].obtenerTiempoRespuesta() == None): #Tiempo Respuesta
                        
                        self.procesosEjecucion[0].calcularRespuesta(self.Tiempo)                

                time.sleep(1)

                self.Tiempo += 1
                frameTiempo.configure(text=" Reloj: {} ".format(str(self.Tiempo)))     

                if(len(self.procesosEjecucion) > 0): #Validar que no tenga todos bloqueados              

                    self.procesosEjecucion[0].asignarTiempoEjecutado(self.procesosEjecucion[0].obtenerTiempoEjecutado() + 1)
                    self.tablaEjecucion.insert(1,2,self.procesosEjecucion[0].obtenerTiempoEjecutado())

                #Actualizar el tiempo de bloqueo si es que existen

                if(len(self.procesosBloqueados) > 0 ):

                    indices = []

                    for i in range(len(self.procesosBloqueados)):

                        tiempoTranscurrido = self.procesosBloqueados[i].obtenerTiempoBloqueado()
                        tiempoTranscurrido += 1

                        self.procesosBloqueados[i].asignarTiempoBloqueado(tiempoTranscurrido)
                        self.tablaBloqueados.insert(i + 1, 1, self.procesosBloqueados[i].obtenerTiempoBloqueado())

                        if(self.procesosBloqueados[i].obtenerTiempoBloqueado() >= 8):

                            indices.append(i)
                            self.procesosBloqueados[i].asignarTiempoBloqueado(0)    

                    #Se ejecuta unicamente si esxisten procesos bloqueados susceptibles de ser retornados.

                    for i in range(len(indices)):

                        self.moverListos(indices)

                #Al agotarse el tiempo de ejecucion hacer un swap mandar el ejecutado a terminado y uno de listo a ejecucion.

                if(len(self.procesosEjecucion) > 0): #Validar que no tenga todos bloqueados     

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
                        
    def recalcular(self, frameProcesos, modificarListos = None ):

       procesosDisponibles = len(self.procesosNuevos)
       memoriaDisponible = 4 - (len(self.procesosEjecucion) + len(self.procesosListos) + len(self.procesosBloqueados))
         
       # Cargar todos los nuevos procesos hasta que mi memoria sea llenada.

       for i in range(memoriaDisponible):
           
           if(procesosDisponibles > 0):

                self.procesosNuevos[0].asignarTiempoLlegada(self.Tiempo) # Tiempo Llegada
                self.procesosListos.append(self.procesosNuevos.pop(0))
                procesosDisponibles = len(self.procesosNuevos)
                self.cantidadProcesos -= 1

                if(modificarListos == 1):
                    
                    self.agregarListos()

                    if(len(self.procesosBloqueados) > 2):# Significa que puede ingresar otro a memoria porque tengo todos bloqueados
                            
                            self.tablaListos.delete_row(1)

        # Introduzco un dato de la lista de listos a ejecución.

       if(len(self.procesosListos) > 0):

            self.procesosEjecucion.append(self.procesosListos.pop(0))
              
       frameProcesos.configure(text = " Proceos Retantes: {} ".format(self.cantidadProcesos))    

    def removerEjecutado(self, frameProcesos):

        # Sacar el proceso de ejcucion a terminados.

        self.procesosEjecucion[0].asignarTiempoFinalizacion(self.Tiempo) # Tiempo Finalizacion
        self.procesosEjecucion[0].calcularTiempoRetorno() # Tiempo Retorno
        self.procesosEjecucion[0].calcularTiempoServicio() # Tiempo Servicio
        self.procesosEjecucion[0].calcularTiempoEspera() # Tiempo Espera
        self.agregarTerminados(self.procesosEjecucion.pop(0))

        # Meter otro proceso a ejecucion (siempre que exista)
        self.tablaListos.delete_row(1)
    
        #Detener al ya no tener mas procesos pendientes

        if(len(self.procesosListos) <= 0 and len(self.procesosEjecucion) <= 0 and len(self.procesosBloqueados) <= 0): # Fin

            self.tablaEjecucion.delete_row(1)
            return True            

        if(len(self.procesosListos) > 0 or len(self.procesosBloqueados) > 0):

            self.tablaEjecucion.delete_row(1)
            self.actualizarNuevos()
            self.recalcular(frameProcesos, 1)

            if(len(self.procesosEjecucion) > 0): #En caso de tener todos bloqueados y ninguno proceso mas pendiente de entrar
        
                datosTemporales = self.procesosEjecucion[0].obtenerEjecuccion()
                self.tablaEjecucion.add_row(datosTemporales)
        
    def intercambiar(self):

        self.procesosBloqueados.append(self.procesosEjecucion.pop(0))
        self.tablaEjecucion.delete_row(1)

        self.actualizarBloqueado()

        if(len(self.procesosListos) > 0):

            #Actualizo mi tabla

            self.tablaListos.delete_row(1)

            #Agregar el siguiente dato a ejecucion

            self.procesosEjecucion.append(self.procesosListos.pop(0))
            datosTemporales = self.procesosEjecucion[0].obtenerEjecuccion()

            self.tablaEjecucion.add_row(datosTemporales)

    def modificarNuevos(self, Frame):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        Valores = self.procesosNuevos
        datosTabla = [["ID", "T/ Est", "T/ Eje"]]

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

    def modificarBloqueados(self, Frame):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        datosTabla = [["ID", "Tiempo Bloqueado"]]

        self.tablaBloqueados = CTkTable(master = Frame,
                         row = len(datosTabla),
                         column = len(datosTabla[0]),
                         header_color = self.fondoAzul,
                         values = datosTabla,
                         corner_radius = 0)
        
        self.tablaBloqueados.grid(row = 0, column = 0, sticky = "nsew")   

    def modificarTerminados(self, Frame):

        Frame.rowconfigure(0, weight = 1)
        Frame.columnconfigure(0, weight = 1)

        datosTabla = [["ID", "T/ Est", "T/ Eje", "1°N", "Op", "2°N", "Res", "T/Lle" , "T/Fin", "T/Ret", "T/Res", "T/Esp", "T/Ser" ]]

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

        if(len(self.procesosListos) > 0):

            self.tablaListos.add_row(self.procesosListos[len(self.procesosListos) - 1].obtenerEjecuccion())

    def actualizarNuevos(self):

        if(len(self.procesosNuevos) > 0):

            self.tablaNuevos.delete_row(1)

    def actualizarEjecucion(self):

        self.tablaEjecucion.delete_row(1)
        self.tablaEjecucion.add_row(self.procesosEjecucion[0].obtenerEjecuccion())   

    def actualizarBloqueado(self):

        datosTemporales = self.procesosBloqueados[len(self.procesosBloqueados) - 1].obtenerBloqueado()

        self.tablaBloqueados.add_row(datosTemporales)

    def moverListos(self, indices):

        for i in range(len(indices)):

            if(len(self.procesosEjecucion) <= 0):

                self.procesosEjecucion.append(self.procesosBloqueados.pop(0))
                self.tablaEjecucion.add_row(self.procesosEjecucion[0].obtenerEjecuccion())     

            else:    

                self.procesosListos.append(self.procesosBloqueados.pop(0))
                self.tablaListos.add_row(self.procesosListos[len(self.procesosListos)-1].obtenerEjecuccion()) 

            self.tablaBloqueados.delete_row(1)       

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
