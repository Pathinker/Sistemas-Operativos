from Backend import Lote
import threading
import time

class Lotes:

    def __init__(self, Cantidad):

        self.cantidadLotes = Cantidad // 4 + 1
        self.Procesos = [Lote.Lote(i) for i in range(Cantidad)]
        self.procesosBloqueados = []
        self.procesoListos = []
        self.procesoEjecucion = []
        self.procesosTerminados = []
        self.Tiempo = 0    

        self._stop_event = threading.Event()

    def contador(self, Frame):  

        self.Contador = threading.Thread(target=self.ejecutar, args=(Frame,))
        self.Contador.start()

    def detener(self):

        self._stop_event.set()
        self.Contador.join()      

    def ejecutar(self, Frame):

        for i in range(4):

            try:
                    
                self.procesoListos.append(self.Procesos[i])    

            except:

                print("Sin lotes dispoinibles")

        self.procesoEjecucion.append(self.procesoListos.pop(0))            

        while not self._stop_event.is_set():
            
            self.Tiempo += 1
            Frame.configure(text=" Reloj: {} ".format(str(self.Tiempo)))

            time.sleep(1)

    def obtenerInput(self, Lote, Caracter):

        if(Caracter == "W"):
            pass

        elif(Caracter == "E"):
            pass

        elif(Caracter == "P"):
            pass

        elif(Caracter == "C"):   
            pass 

    def obtenerProcesos(self):

        return self.Procesos    
