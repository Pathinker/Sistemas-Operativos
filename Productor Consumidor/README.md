## **Productor Consumidor**

<p align="justify">
El programa productor consumidor asemeja el comportamiento de un servidor donde de igual manera es susceptible de tener varios productores y consumidores que accedan de manera simultánea a datos, productos o elementos requeridos, de igual manera es posible tener un único productor con varios consumidores y viceversa, aunque en los requisitos solo fue necesario simular el comportamiento más sencillo de un productor y un consumidor.
</p>

<p align="justify">
El lenguaje empleado es ensamblador debido a la simplicidad de requisitos y tiempo disponible, para la generación de los números aleatorios que condicionan el ingreso del consumidor y productor son obtenidos de los ticks del reloj del sistema y es dividido por la cantidad deseada en el caso del ingreso aleatorio del consumidor y productor es entre 2 generando como residuo únicamente dos números, lo mismo acontece con la cantidad a trabajar, aunque es divido entre 4 y sumado 4 para dar el rango deseado de 4 a 7 unidades, los bucles y acceso a memoria emplean etiquetas, comparaciones y los registros de 16 bits del procesador de intel 8086, en el entorno de desarrollo emu8086.
</p>

<p align="justify">
Para continuar el consumidor y productor desde su previa continuación declaró dos variables únicas que indican la última posición de lectura, además de una variable para verificar el espacio necesario, al terminar de trabajar correctamente los elementos o agotarse el espacio retorna, para ciclar la lectura evaluó si es excedido el número de elementos de mi array para resetear las variables de posición. En la detección de carácter se hace uso de una interrupción específica que permite la ejecución del programa sin la necesidad de detenerse, idéntico al kbhit de C.
</p>

## **Requerimientos**

- Contenedor 20 elementos circular.
  
- Exclusión mutua en memoria, solamente puede consumir o producir en un solo momento.
  
- Reanudar al productor o consumidor desde la localización previa.

## **Funcionamiento**

https://github.com/DarchoG/Sistemas-Operativos/assets/159450603/2cae9ef4-7a2c-4665-8338-bf1c03207549
