# Ejecutando la práctica 3

### 1. Ejecutar los tests

Es posible que tengamos algún problema en le código, para comporbar si existe algún bug, se han de ejecutar los tests del fichero 'e3_aux/test'.

La ejecución es simple, en Pycharm se accede al fichero 'e3_aux/test/brickertest.py' y se pulsa en la flecha verde para ejecutar, como un programa normal, sin necesidad de argumentos.

### 2. Entregable3a

Esta parte del entregable se dedica a encontrar una solución, no siempre la mejor.

Para obtener una solución se utiliza el Backtrackingsolver con control de visitados donde almacenamos el estado de una solución parcial(PS). Este estado de la PS hemos decidido que sea las dos posiciones de los que componen el bloque, es decir la posición del Bloque.

### 3. Entregable3b

Esta parte del entregable se dedica a encontrar la mejor solución. En otras palabras, obtendrá todas las coluciones y las comparará entre ellas para obtener la solución que aporte menos pasos.

Para ello hace uso de la función f() que evalúa las PS donde debe devolver su puntuación. recordamos que estamos ante un problema de minimización, por lo tanto el BacktackingOptSolver compara dos PS y se queda con la que menor resultado de la función f().

*NOTA: El resto del algoritmo aparentemente es igual al apartado 3a. Podría mejorarse el tiempo de ejecución eligiendo qué PS hija crear primero.*

### 4. Ejecutar el visualizador Brickerviewer

Este visualizador tiene dos modos:

   1. ### Modo juego:

Para ejecutar el visualizador en modod juego basta con ejecutar el jar mediante línea de comandos, pasándole como parámetro únicamente el fichero de nivel:

<code>java -jar BrickerViewer.jar level1.txt</code>

Nos aparecerá una nueva ventana. Con las flechas del teclado se podrá jugar y la tecla Esc reiniciará la partida.

   2. ### Modo visualizador:

Para ejecutar este modo, tan solo hay que añadirle un parámetro más al comando anterior:

<code>java -jar BrickerViewer.jar level1.txt solution1.txt</code>

Le indicamos la solución, y el visualizador nos mostrará los pasos de la solución indicada.Para manejarnos en este modo, se utiliza la barra espaciadora para ir paso pos paso de la solución y la tecla Esc para reiniciarla.