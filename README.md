# Proyecto de HPC grupo A2

## Descripción

Este proyecto implementa un algoritmo de Computación de Alta Performance (HPC) utilizando C++ y MPI para procesar y enviar datos de manera eficiente en un entorno distribuido. El flujo del proyecto implica que el maestro instancia scripts de en Python que procesan información de un archivo CSV, luego realiza una division de dominio segun la cantidad de esclavos y envíe partes de la información a los esclavos para su procesamiento paralelo, y finalmente, unifiqua y reorganiza las respuestas de los esclavos.

## Requisitos

- C++
- MPI 
- Python 3.x
- Bibliotecas de Python: `pandas`, `tqdm`


## Compilación

### En las PCs de la Facultad de Ingeniería

1. Carga el módulo MPI necesario:
    ```bash
    module load mpi/mpich-x86_64
    ```

2. Compila el archivo `master.cpp`:
    ```bash
    mpic++ -I ~/local/include -o master c++/src/master.cpp
    ```

3. Compila el archivo `slave.cpp`:
    ```bash
    mpic++ -I ~/local/include -o slave c++/src/slave.cpp
    ```

## Creación del Entorno Python

1. Crea un entorno virtual de Python y actívalo:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Instala las bibliotecas necesarias:
    ```bash
    pip install pandas tqdm
    ```

## Ejecución

1. Asegúrate de tener un archivo `hostfile` con los hosts que participarán en la ejecución.

2. Ejecuta el maestro y los esclavos usando `mpirun`:
    ```bash
    mpirun -hostfile hostfile -np 1 ./master 12 : -np 12 ./slave
    ```
   - En este comando, `-np 1` indica que se ejecutará 1 proceso maestro y `-np 12` indica que se ejecutarán 12 procesos esclavos.
   - El primer argumento del maestro es la cantidad de esclavos para la partición de dominio.

## Scripts de Python

1. `mapa.py`: Genera un mapa de calor basado en los resultados del algoritmo paralelo.
    - **Descripción:** Este script lee un archivo .json que es el resultado del algoritmo paralelo. Toma como entrada un código de variante y un código de parada, y devuelve un archivo HTML con el mapa de calor asociado al recorrido de esa variante.
    - **Ejecución:**
    ```bash
    python python/mapa.py <CODIGO_DE_VARIANTE> <CODIGO_PARADA_ORIGEN>
    ```

## Contribuciones

Las contribuciones son bienvenidas.