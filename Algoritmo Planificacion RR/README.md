## **Algoritmo Planificación Round Robin**

<p align="justify">
Es desarrollado el algoritmo de planificación Round Robbin, los procesos son atendidos de igual manera como en first come first served conforme son creados, no obstante son atendidos por un lapso de tiempo denominado quantum, el cual determina la cantidad de tiempo destinada en cada ciclo, al finalizarse procede a atender el siguiente proceso y vuelve a formar el proceso en listos para completar el trabajo restante. Es considerado como uno de los algoritmos más justos al no presentar inanición y apropiativo por la capacidad de interrumpir la ejecución de una solicitud.
</p>

## **Características Nuevas**

Nuevo dato de entrada para condicionar el lapso de trabajo en cada iteración del nuevo algoritmo planificador Round Robin.

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

- **B:** Muestra en una ventana aparte la tabla BCP (Bloque Control Proceso) con todos los tiempos disponibles al momento.

- **N:** Crea un nuevo proceso respetando la capacidad de memoria disponible y asignando a su estado correspondiente.

**Tiempos:**

- **Tiempo Llegada:** Hora en ingresó a memoria.

- **Tiempo Respuesta:** Primer ingreso a ejecución desde que se incorpora a memoria.

- **Tiempo Espera:** Agrupa todas las instancias en las que no se encuentra ejecutándose la petición.

- **Tiempo Servicio:** Lapso total en el procesador.

- **Tiempo Retorno:** Tiempo total transcurrido en memoria hasta su finalización.

- **Tiempo Finalización:** Hora de conclusión de la solicitud.

## **Funcionamiento**

https://github.com/DarchoG/Sistemas-Operativos/assets/159450603/05c30b0d-cd56-4749-841b-3358a182d9ef
