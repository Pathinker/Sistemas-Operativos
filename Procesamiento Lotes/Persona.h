#include <string>
using namespace std;

class Persona{

    private:

        string Nombre;

    protected:

        void verificarNombre(string &N);

    public:

        void asignarNombre(string N);
        string obtenerNombre();


};
