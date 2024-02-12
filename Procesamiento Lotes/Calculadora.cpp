#include "Calculadora.h"
#include <iostream>
#include <string>
#include <cmath>
using namespace std;

Calculadora::Calculadora(long double N,  long double M){

    asignarOperando(N);
    asignarOperador(M);

}

void Calculadora::operar(){

    switch(obtenerMetodo()){

        case '+':
            sumar();
            break;
        case '-':
            restar();
            break;
        case '*':
            multiplicar();
            break;
        case '/':
            dividir();
            break;
        case '%':
            residuo();
            break;
    }
}

void Calculadora::validarDivision(){

    bool Bandera = false;
    long double M = obtenerOperador();

    while(!Bandera){

        if(M == 0){

            cout <<"\n No es posible dividir por 0, cambie el divisor: ";
            fflush(stdin);
            cin >> M;

        }else Bandera = true;
    }

    asignarOperador(M);
}

void Calculadora::validarMetodo(string &N){

    bool Bandera = false;
     //N.at(0) Permitir evaluar en un char, evita sobrecarga;

    while(!Bandera){

        if(N.at(0) == '+' || N.at(0) == '-' || N.at(0) == '*' || N.at(0) ==  '/' || N.at(0) == '%'){

            Bandera = true;
            return;
        }
        else{

            cout <<"\nIngrese un caracter valido: ";
            fflush(stdin);
            cin >> N;
        }
    }
}

void Calculadora::sumar(){

    long double N = obtenerOperando();
    long double M = obtenerOperador();

    asignarResultado(N + M);

}

void Calculadora::restar(){

    long double N = obtenerOperando();
    long double M = obtenerOperador();

     asignarResultado(N - M);

}

void Calculadora::multiplicar(){

    long double N = obtenerOperando();
    long double M = obtenerOperador();
    long double Solucion = N * M;

    asignarResultado(Solucion);

}

void Calculadora::dividir(){

    validarDivision();

    long double N = obtenerOperando();
    long double M = obtenerOperador();

     asignarResultado(N / M);

}

void Calculadora:: residuo(){

    validarDivision();

    long double N = obtenerOperando();
    long double M = obtenerOperador();

    asignarResultado(fmod(N, M));

}

void Calculadora::asignarOperando(long double N){

    Operando = N;

}

void Calculadora::asignarOperador(long double N){

    Operador = N;

}

void Calculadora::asignarResultado(long double N){

    Resultado = N;

}

void Calculadora::asignarMetodo(string N){

    validarMetodo(N);
    const char* Cadena = N.c_str();
    char Resultado = Cadena[0];
    Metodo = Resultado ;

}

long double Calculadora::obtenerOperando(){

    return Operando;
}

long double Calculadora::obtenerOperador(){

    return Operador;
}

long double Calculadora::obtenerResultado(){

    return Resultado;
}

char Calculadora::obtenerMetodo(){

    return Metodo;
}
