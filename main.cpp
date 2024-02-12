#include <iostream>
#include <vector>
#include <clocale>
#include "Persona.h"
#include "Calculadora.h"
using namespace std;

int ID = 0;
bool Impresion = false;

bool validarNumero(int Iteraciones);
void capturaProcesos();
void procesos(int Procesos, int Lotes);
void procesarLote(vector<Persona>&listaPersonas, vector<Calculadora>&listaCalculadoras, vector<long double>&Tiempos);
void imprimirLote(vector<Persona>&listaPersonas, vector<Calculadora>&listaCalculadoras, vector<long double>&Tiempos);
void costoTiempo(vector<long double>&Tiempos);

int main(){

    setlocale(LC_CTYPE, "Spanish");

    capturaProcesos();

    return 0;
}

bool validarNumero(int Iteraciones){

    if(Iteraciones <= 0){

            cout << "\nIntroduzca una digito valido.\n";
            return false;

    }

    return true;

}

void capturaProcesos(){

    int Iteraciones;
    int Lotes;
    bool Bandera = false;

    cout << "--- Programa 1 Procesamiento por Lotes -----\n";


    while(!Bandera){

        cout << "\nIntroduzca la cantidad de datos a ingresar: ";
        cin >> Iteraciones;

        Bandera = validarNumero(Iteraciones);

    }

    Lotes = Iteraciones / 4;

    if(Iteraciones % 4 > 0) Lotes++;

    procesos(Iteraciones, Lotes);

}


void procesos(int Procesos, int Lotes){

    vector<Persona>listaPersonas;
    vector<Calculadora>listaCalculadoras;
    vector<long double>Tiempos;


    for(int i = 0; i < Procesos; i++){

        if(Impresion) cout << "--- Programa 1 Procesamiento por Lotes -----\n";

        if(i % 4 == 0 && i != 0){

            cout << "\nInicio de un nuevo Lote\n";
            Lotes--;
        }

        cout << "\nLotes Pendientes: " << Lotes;
        cout<< endl;
        fflush(stdin);

        cout << "\n--- Proceso en Ejeccución ---\n";
        procesarLote(listaPersonas, listaCalculadoras, Tiempos);
        cout << "\n--- Proceso  Terminados ---\n";
        imprimirLote(listaPersonas, listaCalculadoras, Tiempos);

        if(i + 1 == Procesos) continue;

        system("pause");
        system("cls");

        Impresion = true;

    }

    costoTiempo(Tiempos);

}

void procesarLote(vector<Persona>&listaPersonas, vector<Calculadora>&listaCalculadoras, vector<long double>&Tiempos){

    string Auxiliar;
    long double Tiempo;
    long double Digitos;
    string Operacion;
    Persona CPersona;
    Calculadora CCalculadora;

    cout << "ID: " << ID;
    cout << "\nNombre del Programador: ";
    cin >> Auxiliar;
    CPersona.asignarNombre(Auxiliar);
    fflush(stdin);

    cout << "Operacion a realizar + - * / %: ";
    cin >> Operacion;
    CCalculadora.asignarMetodo(Operacion);
    fflush(stdin);

    cout << "Dato 1: ";
    cin >> Digitos;
    CCalculadora.asignarOperando(Digitos);
    fflush(stdin);

    cout << "Dato 2: ";
    cin >> Digitos;
    CCalculadora.asignarOperador(Digitos);
    fflush(stdin);

    cout << "Tiempo Ejecución (Segundos): ";
    cin >> Tiempo;
    fflush(stdin);

    CCalculadora.operar();

    listaPersonas.push_back(CPersona);
    listaCalculadoras.push_back(CCalculadora);
    Tiempos.push_back(Tiempo);
    ID++;
}

void imprimirLote(vector<Persona>&listaPersonas, vector<Calculadora>&listaCalculadoras, vector<long double>&Tiempos){

    cout << "ID \t| Operacion \t| Resultado \n";


    for (int i = 0; i < ID; i++){

        cout << i << "\t"
        << listaCalculadoras[i].obtenerOperando() << "    "
        << listaCalculadoras[i].obtenerMetodo() << "     "
        << listaCalculadoras[i].obtenerOperador() << "  = \t"
        << listaCalculadoras[i].obtenerResultado() << endl;

    }
}

void costoTiempo(vector<long double>&Tiempos){

    long double Auxiliar = 0;

    for(int i = 0; i < Tiempos.size(); i++) Auxiliar += Tiempos[i];

    cout << "\n\nLotes procesados, costo en unidades de tiempo:" << Auxiliar << endl;

}
