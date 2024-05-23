from Backend import Lote

class Lotes:

    def __init__(self, Cantidad):

        self.cantidadLotes = Cantidad // 4 + 1
        self.Procesos = Lote[Cantidad]
        self.procesosBloqueados = []
        self.procesoEjecucion = []
        self.procesosTerminados = []
        self.Tiempo = 0    
        
        self.ejecutar()

    def ejecutar(self):  

        pass

    def obtenerInput(self, Lote, Caracter):

        if(Caracter == "W"):
            pass

        elif(Caracter == "E")
            pass

        elif(Caracter == "P"):
            pass

        elif(Caracter == "C"):   
            pass 
