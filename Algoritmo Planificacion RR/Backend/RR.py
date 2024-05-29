from Backend import Proceso
from customtkinter import *
from CTkTable import *
import threading
import time

from Frontend import BCP

class sistemOperativo:

    def __init__(self, Ventana, Cantidad, Quantum, frameNuevos, frameListos, frameEjecucion,frameBloqueados, frameTerminados, frameTiempo, frameProcesos):

        self.idProceso = Cantidad - 1
        self.cantidadProcesos = Cantidad
        self.procesosNuevos = []

        self.procesosListos = []
        self.procesosEjecucion = []
        self.procesosBloqueados = []
        self.procesosTerminados = []
        self.Tiempo = 0
        self.Quantum = Quantum

        for i in range(Cantidad): #Es incorporado para establecer un ID ascendente a los próximos procesos creados.

            Solicitud = Proceso.Proceso(i, self.Tiempo, Quantum)
            self.procesosNuevos.append(Solicitud)

        self.fondoAzul = "#1565C0"

        self.Tecla = ""
        self.Estado = [True]    

        self._stop_event = threading.Event()
        self.iniciar(Ventana, Quantum, frameNuevos, frameListos, frameEjecucion,frameBloqueados, frameTerminados, frameTiempo, frameProcesos)

    def iniciar(self, Ventana, Quantum, frameNuevos, frameListos, frameEjecucion, frameBloqueados, frameTerminados, frameTiempo, frameProcesos):  

        self.Contador = threading.Thread(target=self.ejecutar, daemon = True, args=(Ventana, Quantum, frameNuevos, frameListos, frameEjecucion, frameBloqueados, frameTerminados, frameTiempo, frameProcesos))
        self.Contador.start()

    def detener(self):

        self._stop_event.set()
        self.Contador.join(timeout=0)      

    def ejecutar(self, Ventana, Quantum, frameNuevos, frameListos, frameEjecucion, frameBloqueados, frameTerminados, frameTiempo, frameProcesos):

        self.recalcular(frameProcesos) # Carga los lotes en Listo y Ejecucion
        self.modificarNuevos(frameNuevos)
        self.modificarListos(frameListos)
        self.modificarEjecucion(frameEjecucion)
        self.modificarBloqueados(frameBloqueados)
        self.modificarTerminados(frameTerminados)

        frameProcesos.configure(text = " Procesos Restantes: {} ".format(self.cantidadProcesos))

        while (not self._stop_event.is_set()):

            while(self.Estado[0]):

                if(len(self.procesosEjecucion) > 0): #Validar que no tenga todos bloqueados

                    if(self.procesosEjecucion[0].obtenerTiempoRespuesta() == None): #Tiempo Respuesta
                        
                        self.procesosEjecucion[0].calcularRespuesta(self.Tiempo)                  

                time.sleep(1)

                self.Tiempo += 1
                frameTiempo.configure(text=" Reloj: {} ".format(str(self.Tiempo)))     

                if(len(self.procesosEjecucion) > 0): #Validar que no tenga todos bloqueados              

                    self.procesosEjecucion[0].asignarTiempoEjecutado(self.procesosEjecucion[0].obtenerTiempoEjecutado() + 1)
                    self.procesosEjecucion[0].asignarTiempoQuantum(self.procesosEjecucion[0].obtenerTiempoQuantum() + 1)
                    self.tablaEjecucion.insert(1,2,self.procesosEjecucion[0].obtenerTiempoEjecutado())
                    self.tablaEjecucion.insert(1,3,self.procesosEjecucion[0].obtenerTiempoQuantum())
                
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
        
                    #Es posible de ejectar un proceso y no tener otros, por lo tanto tengo que vovler a validar si tengo uno disponible en ejecución, para continuar el programa

                    if(len(self.procesosEjecucion) > 0 and self.procesosEjecucion[0].obtenerTiempoQuantum() >=  self.procesosEjecucion[0].obtenerQuantum()):

                        self.roundRobin()     
                        
                if(self.Tecla != None):

                    self.obtenerInput(Ventana, self.Tecla, frameProcesos)

                    self.Tecla = None                                    

            if(self.Tecla != None):

                self.obtenerInput(Ventana, self.Tecla, frameProcesos)

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

    def removerEjecutado(self, frameProcesos, Error = None):

        # Sacar el proceso de ejecucion a terminados.

        self.procesosEjecucion[0].asignarTiempoFinalizacion(self.Tiempo) # Tiempo Finalizacion
        self.procesosEjecucion[0].calcularTiempoRetorno() # Tiempo Retorno
        self.procesosEjecucion[0].calcularTiempoServicio() # Tiempo Servicio
        self.procesosEjecucion[0].calcularTiempoEspera() # Tiempo Espera

        if(Error == None):

            self.procesosEjecucion[0].realizarOperacion() #Obtener el resultado si no salio con error.
            
        self.agregarTerminados(self.procesosEjecucion.pop(0))

        # Meter otro proceso a ejecucion (siempre que exista)
        self.tablaListos.delete_row(1)
    
        #Detener al ya no tener mas procesos pendientes

        if(len(self.procesosListos) <= 0 and len(self.procesosEjecucion) <= 0 and len(self.procesosBloqueados) <= 0): # Permitir que se siga ejecutando por la posibilidad de agregar nuevos

            self.tablaEjecucion.delete_row(1)         

        if(len(self.procesosListos) > 0 or len(self.procesosBloqueados) > 0):

            self.tablaEjecucion.delete_row(1)
            self.actualizarNuevos()
            self.recalcular(frameProcesos, 1)

            if(len(self.procesosEjecucion) > 0): #En caso de tener todos bloqueados y ninguno proceso mas pendiente de entrar
        
                datosTemporales = self.procesosEjecucion[0].obtenerEjecuccion()
                self.tablaEjecucion.add_row(datosTemporales)
        
    def intercambiar(self):

        self.procesosEjecucion[0].asignarTiempoQuantum(0) # Resetear el tiempo del Quantum
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
        datosTabla = [["ID", "T/ Est", "T/ Eje", "T/ Qua", "1°N", "Op", "2°N"]]

        for i in  Valores:

            Datos = []

            Datos.append(i.obtenerID())
            Datos.append(i.obtenerTiempoEstimado())
            Datos.append(i.obtenerTiempoEjecutado())
            Datos.append(i.obtenerTiempoQuantum())
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
        
        self.tablaBloqueados.grid(row = 0, column = 0, sticky = "nsew", pady = (6,0), padx = (6, 0))   

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

    def agregarNuevos(self):

        if(len(self.procesosNuevos) > 0):

            self.tablaNuevos.add_row(self.procesosNuevos[len(self.procesosNuevos) - 1].obtenerNuevo())

    def agregarListos(self):

        if(len(self.procesosListos) > 0):

            self.tablaListos.add_row(self.procesosListos[len(self.procesosListos) - 1].obtenerListo())

    def agregarEjecucion(self):

        self.tablaEjecucion.add_row(self.procesosEjecucion[len(self.procesosEjecucion) - 1].obtenerEjecuccion())
        
    def agregarTerminados(self, Informacion):

        self.procesosTerminados.append(Informacion)

        self.tablaTerminados.add_row(Informacion.obtenerTerminados())

    def actualizarNuevos(self):

        if(len(self.procesosNuevos) > 0):

            self.tablaNuevos.delete_row(1)

    def actualizarListos(self):

        self.tablaListos.delete_row(1)
        self.tablaListos.add_row(self.procesosListos[len(self.procesosListos) - 1].obtenerListo()) 

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

    def agregarNuevoProceso(self, frameProcesos):

        self.idProceso += 1
        nuevoProceso = Proceso.Proceso(self.idProceso, self.Tiempo, self.Quantum)

        if(len(self.procesosBloqueados) + len(self.procesosListos) + len(self.procesosEjecucion) >= 4): # Memoria Llena

            self.procesosNuevos.append(nuevoProceso)
            self.cantidadProcesos += 1
            frameProcesos.configure(text = " Procesos Restantes: {} ".format(self.cantidadProcesos))
            self.agregarNuevos()

        elif(len(self.procesosEjecucion) > 0):   # Si tengo uno ejecutandose entonces agregarlo en listos 

            nuevoProceso.asignarTiempoLlegada(self.Tiempo)
            self.procesosListos.append(nuevoProceso)
            self.agregarListos()

        else: # Entonces significa que no tengo la memoria llena y tampoco en ejecución, por lo tanto lo incorporo en ejecución:

            nuevoProceso.asignarTiempoLlegada(self.Tiempo)
            self.procesosEjecucion.append(nuevoProceso)
            self.agregarEjecucion()

    def roundRobin(self):

        self.procesosEjecucion[0].asignarTiempoQuantum(0)

        if(len(self.procesosListos) > 0): # Si existen procesos en listo entonces lo movemos ahi.

            self.procesosListos.append(self.procesosEjecucion.pop(0))
            self.actualizarListos()
            self.procesosEjecucion.append(self.procesosListos.pop(0))
            self.actualizarEjecucion()
            
        else: #En caso contrario lo dejamos en memoria, pero le resetemoas el quantum

            return

    def obtenerInput(self, Ventana, Caracter, frameProcesos):

        Caracter = Caracter.upper()
        procesoActivo = len(self.procesosEjecucion)

        if(Caracter == "W" and self.Estado[0] and procesoActivo > 0):
            
            self.procesosEjecucion[0].asignarResultado("ERROR")
            self.removerEjecutado(frameProcesos, 1)

        elif(Caracter == "E"  and self.Estado[0] and procesoActivo > 0):

            self.intercambiar()

        elif(Caracter == "P"):

            self.Estado[0] = False

        elif(Caracter == "C"):   

            self.Estado[0] = True

        elif(Caracter == "N" and self.Estado[0]):

            self.agregarNuevoProceso(frameProcesos)  

        elif(Caracter == "B"):

            self.Estado[0] = False
            BCP.BCP(Ventana, self.procesosNuevos, self.procesosListos, self.procesosEjecucion, self.procesosBloqueados, self.procesosTerminados, self.Estado, self.Tiempo)

    def asignarTecla(self, Tecla):

        self.Tecla = Tecla
