## **Algoritmo Planificación First Come First Serve 2**

<p align="justify">
Incorpora la tabla control de procesos donde agrupa toda la información relacionada con un proceso particular, persiste el uso del algoritmo FCFS para atender las peticiones, adicionalmente es incorporada una nueva función creadora de procesos.
</p>

## **Características Nuevas**

**Entradas del Teclado:**

- **B:** Muestra en una ventana aparte la tabla BCP (Bloque Control Proceso) con todos los tiempos disponibles al momento.

- **N:** Crea un nuevo proceso respetando la capacidad de memoria disponible y asignando a su estado correspondiente.

## **Características Previas**

En memoria solamente es posible alojar 4 procesos, un proceso es considerado en memoria si se encuentra en listo, ejecución o bloqueados.

**Estados en Memoria:**

- **Nuevo:** Espera la asignación de recursos.

- **Listo:** Espera la asignación en CPU

- **Ejecución:** Realización de la tarea.

- **Bloqueado:** Asemeja la espera de una interrupción de entrada o salida, vuelve a formar en listos al proceso ejecutado después de permanecer 8 segundos bloqueado.

- **Terminado:** Finalización de la tarea.

**Entradas del Teclado:**

- **E:** Interrupción de entrada y salida expulsa un proceso de ejecución a bloqueado.

- **W:** Error, termina la ejecución con un estado de error.

- **P:** Pausa, interrumpe totalmente la ejecución.

- **C:** Continuar, reanuda la ejecución de las instrucciones.

**Tiempos:**

- **Tiempo Llegada:** Hora en ingresó a memoria.

- **Tiempo Respuesta:** Primer ingreso a ejecución desde que se incorpora a memoria.

- **Tiempo Espera:** Agrupa todas las instancias en las que no se encuentra ejecutándose la petición.

- **Tiempo Servicio:** Lapso total en el procesador.

- **Tiempo Retorno:** Tiempo total transcurrido en memoria hasta su finalización.

- **Tiempo Finalización:** Hora de conclusión de la solicitud.

## **Funcionamiento**

https://github.com/DarchoG/Sistemas-Operativos/assets/159450603/ab3c0547-8473-4ec0-8f16-5c0ad8c0aaaf
