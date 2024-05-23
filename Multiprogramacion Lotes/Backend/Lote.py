import random

class Lote:

    def __init__(self, Numero):

        self.ID = Numero
        self.tiempoEstimado = random.randint(5, 18)
        self.tiempoEjecutado = 0
        self.primerOperando = random.randint(1, 10000)
        self.segundoOperando = random.randint(1, 10000)
        self.Operacion = self.obtenerOperando(random.randint(1, 5))
        self.Resultado = self.realizarOperacion(self.primerOperando, self.segundoOperando, self.Operacion)    

    def obtenerOperando(self, Numero):

        if(Numero == 1):
            
            return "+"
        
        elif(Numero == 2):

            return "-"
        
        elif(Numero == 3):

            return "*"
        
        elif(Numero == 4):

            return "/"
        
        elif(Numero == 5):

            return "%"
        
    def realizarOperacion(self, primerOperando, segundoOperando, Operador):

        if(Operador == "+"):

            return primerOperando + segundoOperando

        elif(Operador == "-"):

            return primerOperando - segundoOperando    
        
        elif(Operador == "*"):

            return primerOperando * segundoOperando
        
        elif(Operador == "/"):

            return primerOperando // segundoOperando
        
        elif(Operador == "%"):

            return primerOperando % segundoOperando
        
    def obtenerID(self):

        return self.ID    
        
    def obtenerTiempoEstimado(self):

        return self.tiempoEstimado

    def obtenerTiempoEjecutado(self):

        return self.tiempoEjecutado    

    def obtenerPrimerOperando(self):

        return self.primerOperando
    
    def obtenerSegundoOperando(self):

        return self.segundoOperando
    
    def obtenerOperacion(self):

        return self.Operacion
    
    def obtenerResultado(self):

        return self.Resultado
    
    def asignarTiempoEjecutado(self, Cantidad):

        self.ID = Cantidad

    def asignarTiempoEjecutado(self, Cantidad):

        self.tiempoEjecutado = Cantidad
