#ifndef NODO_H
#define NODO_H

class template<typename T>Nodo{

    private:

        T Dato; // Dato que quiero almacenar de caracter template, a fin de que pueda almancer lo que yo quiera.
        Nodo* Enlace; // Almacena una dirección de memoria de la clase nodo, a fin de usarla para posterior en una lista simplemente ligada

    public:

        Nodo(T d) : dato(d), siguiente(nullptr) {}

};

#endif
