#include <string>
using namespace std;

class Calculadora{

    private:

         long double Operando;
         long double Operador;
         long double Resultado;
         char Metodo;

    protected:

        void validarDivision();
        void validarMetodo(string &N);

    public:

        void operar();
        void sumar();
        void restar();
        void multiplicar();
        void dividir();
        void residuo();

        Calculadora(long double N,  long double M);
        Calculadora(){};

        void asignarOperando(long double N);
        long double obtenerOperando();

        void asignarOperador(long double N);
        long double obtenerOperador();

        void asignarResultado(long double N);
        long double obtenerResultado();

        void asignarMetodo(string N);
        char obtenerMetodo();

};
