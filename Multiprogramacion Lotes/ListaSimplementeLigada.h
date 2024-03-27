#ifndef ListaSimplementeLigada_H
#define ListaSimplementeLigada_H

#include "Nodo.h"

template<typename T> class ListaSimplementeLigada{

    private:

        Nodo<T> *Cabeza; // Puntero del inicio de mi lista, solamente es posible recorrerla en un sentido.
        Nodo<T> *Ultimo; 
        

    public:

    ListaSimplementeLigada(){

        Cabeza = nullptr; // Inicializar mi cabeza en nullptr porque no tengo ningun dato almacenado aún

    }

    ~ListaSimplementeLigada(){

        Nodo<T>* Actual = Cabeza;

        while(Actual){

            Nodo<T>* Siguiente = Actual -> obtenerEnlace(); // Obtengo el enlace de la siguiente i

            delete Actual;

            Actual = Siguiente; // Borro el actual, como tengo cargado el siguiente enlace lo asigno como actual, el bucle termina cuando no tengo ningun elmento extra.


        }

    } 

    void insetarInicio(T Dato){

        Nodo<T>* nuevoNodo = new Nodo<T>(Dato); // Creo un nuevo nodo de la caracteristica T, el dato ingresado es el recibido por parametro
        nuevoNodo -> establecerEnlace(Cabeza); // Su dirección debe ser el primero de la lista, en este caso es el cabeza
        Cabeza = nuevoNodo;

    }   

    void eliminarInicio(){

        if(Cabeza){ 

            Nodo<T> Auxiliar = Cabeza;
            Cabeza = Cabeza -> Auxiliar; // El nuevo elemento de inicio es aquel siguiente
            delete Temporal; 
        }

        //else, no existe todavia algun elemento ingresado.
    
    }

    void insertarFinal(T Dato){

        Nodo<T>* nuevoNodo = new Nodo<T>(Dato);

        if(!Cabeza){

            Cabeza = nuevoNodo;
            Ultimo = nuevoNodo;
            
        }else{

            Ultimo -> establecerEnlace(nuevoNodo);
            Ultimo  = nuevoNodo;
    
        }
    }  

};
#endif
