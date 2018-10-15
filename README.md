# Problemas a la hora de utilizar PyCharm

### 1. Ejecutar el test del primer entregable
  
Es posible que en windows tengamos problemas a la hora de poder ejecutar los tests delos entregables.
Para resolver esto, partiremos de la explicación de uso que nos ofrece el profesor en el primer entregable:
  
1. La jerarquía de ficheros de nuestro espacio de trabajo debe seguir la forma que se expresa en la siguiente imagen:
![jerarquia.png](images/jerarquiaFicherosEnt1.png)

2. Siguiendo la guía, en windows deberemos ejecutar el siguiente comando:<br>

    <pre>
    c:\Python37\python3.exe comprueba.py -na "c:\Python37\python3.exe entregable1_solucion.py" pruebas
    </pre>

    Vamos a explicarlo en en detalle, en la primera parte:  
      <pre>
      c:\Python37\python3.exe comprueba.py
      </pre> 
      se ejecuta el programa `python3.exe` ubicado en la ruta`c:\Python37\` y con ese programa en funcionamiento se le pasa como parámetro el programa a ejecutar `comprueba.py`.
      En la segunda parte tenemos los argumentos del programa de python `comprueba.py`: 
      <pre>
      -na "c:\Python37\python3.exe entregable1_solucion.py" pruebas
      </pre>
      donde `-na` son flags del programa y `"c:\Python37\python3.exe entregable1_solucion.py"` es lo mismo que explicamos en el   apartado anterior, es decir que se ejecuta el programa de python `entregable1_solucion.py` dentro del otro programa de python `comprueba.py`.
      Y como os podréis imaginar, `pruebas` es el parámetro que se le pasa al segundo programa.
      
      Cabe destacar que esto no es absoluto, es decir, cada uno puede tener python3 en una ubicación diferente, normalmente, en windows, la carpeta de python se ubica en el directorio `C:`, en mi caso, se me instaló en el directorio `C:\Program Files`. Hay que tener cuidado con los nombres de los directorios con espacios en blanco, por ello copié esta carpeta al directorio superor `C:`.
      He de añadir que el supuesto archivo `python3.exe` en mi caso se llama `python.exe`. Hemos de tener cuidado y fijarnos en el PATH de este programa.
      
      ![python37path.png](images/python37Path.png)
      ![python.png](images/python.png)
      
      Como habrán visto en la primera imagen, mi supuesto programa `entregable1_solucion.py` se llama `entregable1.py`, por lo que el comando que habremos de ejecutar (en mi caso) sería el siguiente:
      
    <pre>
    c:\Python37\python.exe comprueba.py -na "c:\Python37\python.exe entregable1.py" pruebas
    </pre>
      
  Si lo queremos ejecutar edentro del entorno de PyCharm, debemos seguir la siguiente configuración:
  1. Hacemos click derecho en la flecha verde que aparece en la primera línea del código, y a continuación en el tercer campo, `add parameters`.
  2. Dentro de la configuración de ejecución que se ha abierto, en el campo `parameters` añadimos los parámetros del programaa ejecutar (como se ve en la siguiente imagen) que en mi caso es: 
  <pre>
    na "c:\Python37\python.exe entregable1.py" pruebas
  </pre>
  ![configuracion.png](images/configuracion.png)
  3. Le damos a aplicar, y OK
  4. a partir de ahora los parámetros que se pasarán al programa al ejecutarse serán los indicados.
