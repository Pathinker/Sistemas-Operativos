#ifndef NODO_H
#define NODO_H

template<typename T>  class Nodo{// Quiero que sea template, para poder almacenar el tipo de dato que yo quiera, en este caso voy a almacenar la clase calculadora

    private:

        T Dato; // Dato que quiero almacenar de caracter template, a fin de que pueda almancer lo que yo quiera.
        Nodo* Enlace; // Almacena una dirección de memoria de la clase nodo, a fin de usarla para posterior en una lista simplemente ligada

    public:

        Nodo(T d){ // Constructor

            Dato = d;
            Enlace = nullptr
        }

        void establecerDato(T Informacion){

            Dato = Informacion;
        }   

        void establecerEnlace(Nodo* Direccion){

            Enlace = Direccion;

        }

};

#endif
