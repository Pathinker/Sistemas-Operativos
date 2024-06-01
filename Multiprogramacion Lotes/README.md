## **Multiprogramación Lotes**

<p align="justify">
Los programas disponen de interrupciones o segmentos donde es inhabilitado el procesador temporalmente, la multiprogramación aprovecha estas brechas en el tiempo de ejecución del procesador para encomendar la realización de otra tarea, con el refinamiento de esta tarea se consolidan lo sistemas actuales y la programación concurrente donde dos o más hilos, comprendidos como una seria de instrucciones relacionadas se ejecutan al mismo tiempo pero no avanzan de manera simultánea al carecer de tareas paralelas en núcleos extras.
</p>

## **Características Nuevas**

La práctica actual recibe aloja instrucciones agrupadas en lotes, donde se alternan entre tres posibles estados:

- **Nuevo:** Espera la asignación de recursos.

- **Listo:** Espera la asignación en CPU

- **Ejecución:** Realización de la tarea.

- **Terminado:** Finalización de la tarea.

La multiprogramación es aplicada al ser susceptible de recibir inputs del teclado que ejecutan las siguientes operaciones:

- **E:** Interrupción de entrada y salida, vuelve a formar en listos al proceso ejecutado.

- **W:** Error, termina la ejecución con un estado de error.

- **P:** Pausa, interrumpe totalmente la ejecución.

- **C:** Continuar, reanuda la ejecución de las instrucciones.

## **Características Previas**

- En memoria solamente es posible procesar un solo lote, ejecuta el siguiente hasta finalizar el previo.
