## **Algoritmo Planificación First Come First Serve**

<p align="justify">
Método de planificación para atender a las solicitudes conforme arriban al procesador otros métodos basan su métrica en longitud de trabajo o prioridad no obstante son susceptibles de generar inanición sobre todo en algoritmos susceptibles de ser apropiativos y expedir de ejecución los procesos en memoria.
</p>

## **Características Nuevas**

El programa actual incorpora la adición de los tiempos transcurridos en cada una de las fases de un proceso, las cuales son mostradas cada vez que finaliza, los tiempos designados son los siguientes:

- **Tiempo Llegada:** Hora en ingresó a memoria.

- **Tiempo Respuesta:** Primer ingreso a ejecución desde que se incorpora a memoria.

- **Tiempo Espera:** Agrupa todas las instancias en las que no se encuentra ejecutándose la petición.

- **Tiempo Servicio:** Lapso total en el procesador.

- **Tiempo Retorno:** Tiempo total transcurrido en memoria hasta su finalización.

- **Tiempo Finalización:** Hora de conclusión de la solicitud.

**Entradas del Teclado:**

- **E:** Interrupción de entrada y salida expulsa un proceso de ejecución a bloqueado.

**Estados en Memoria:**

- **Bloqueado:** Asemeja la espera de una interrupción de entrada o salida, vuelve a formar en listos al proceso ejecutado después de permanecer 8 segundos bloqueado.

Adicionalmente los lotes son sustituidos por procesos, alojando en memoria de igual manera 4 procesos, puede ingresar uno nuevo al ser expedido otro. 

## **Características Previas**

**Estados en Memoria:**

- **Nuevo:** Espera la asignación de recursos.

- **Listo:** Espera la asignación en CPU

- **Ejecución:** Realización de la tarea.

- **Terminado:** Finalización de la tarea.

**Entradas del Teclado:**

- **E:** Interrupción de entrada y salida, vuelve a formar en listos al proceso ejecutado.

- **W:** Error, termina la ejecución con un estado de error.

- **P:** Pausa, interrumpe totalmente la ejecución.

- **C:** Continuar, reanuda la ejecución de las instrucciones.

## **Funcionamiento**

https://github.com/DarchoG/Sistemas-Operativos/assets/159450603/c6d514a0-5781-4ac6-89f6-10895264d73d
