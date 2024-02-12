#include "Persona.h"
#include <iostream>
using namespace std;

void Persona::asignarNombre(string N){

    verificarNombre(N);
    Nombre = N;
}

void Persona::verificarNombre(string &N){

    bool Bandera = false;

    while(!Bandera){

        if(N.length() == 0){

            cout <<"\nNombre invalido, introduzca algun carácter: ";
            fflush(stdin);
            cin >> N;

        }else Bandera = true;

    }

}

string Persona::obtenerNombre(){

    return Nombre;

}
