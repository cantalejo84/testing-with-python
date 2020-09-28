# testing-with-python

**Paso 1**  
Con el virtualenv activado instalamos Tox

```bash
    $ pip install tox
```
**Paso 2**  
En la raiz creamos un fichero de dependencias para Testing, "test_requirements.txt"

El contenido será el siguiente:

````
pytest==5.3.5
pytest-cov==2.8.1
mock==4.0.2
pytest-mock==3.2.0
bandit==1.6.2
moto==1.3.16
````

*pytest*: Herramienta para poder ejecutar tests  
*pytest-cov*: Herramienta para comprobar la cobertura de nuestro código  
*mock*: Framework para el mockeo de componentes externos  
*pytest-mock*: Integración de mock con pytest  
*bandit*: Herramienta para comprobar la seguridad de nuestro código
*moto*: Libreria que permite testear mockeando servicios de AWS 

**Paso 3**  
TOX  
Tox es una herramienta de linea de comandos de gestión de virualenvs y tests, se puede usar para:    
- Comprobar que su paquete se instala correctamente con diferentes versiones e intérpretes de Python  
- Ejecuntar pruebas en cada uno de los entorne con la herramienta de test de su elección (pytest, unittest, etc.)
- Actuando como un frontend para los servidores de CI, y fusionando las pruebas de CI y las basadas en shell.  
Tox se configura en un archivo llamado *tox.ini en la raiz del proyecto, a continuación un ejemplo.
````
[tox]
envlist = py3
skipsdist = True

[testenv]
deps =
    -r{toxinidir}/requirements.txt
    -r{toxinidir}/test_requirements.txt

commands =
    pytest  --cov-report xml --cov-report html --junitxml xunit-report.xml --cov src.main
    bandit -r src/ -f json -o reports/bandit.json

[pytest]
testpaths = tests
junit_family = xunit1
````


Explicación contenido del fichero *tox.ini*

- `envlist = py3`: Define los entornos en los que ejecutaremos nuestros tests. Si quisiéramos ejecutar los tests en varias versiones de python, valdría con modificar la propiedad y ponerle como valor py37, py38  
- `skypdist = True`: Nos ahorra tener que generar un fichero setup.py  
- `testenv:pytests`: Contiene la configuración para la ejeucicón de los tests. Por un lado, las dependencias (deps) y por otro, el comando que se ejecutará. En nuestro caso, ejecutaremos el propio pytest con los siguientes argumentos:  
    - `--junitxml xunit.xml`: Fichero donde se dejarán los reportes de ejecución de los tests
    - `--cov-report xml --cov`: Generar fichero coverage.xml con informe de cobertura de los tests
- `testenv:bandit`: Contiene la configuración para la ejecución de bandit (análisis de seguridad). Por un lado, las dependencias *(deps)* y por otro, el comando que se ejecutará. En nuestro caso, ejecutaremos *bandit* con los siguientes parámetros:
    - `-r`: recursividad en la carpeta de código
    - `-f json`: salida en formato JSON
    - `-o reports/bandit.json`: reporte al fichero reports/bandit.json.

 
Gracias a esta configuración podemos ejecutar directamente Tox en nuestro terminal para que se ejecuten los test de unidad, se genere el informe de cobertura y tambien el informe de seguridad
 
**Paso 4**  
Instalar PyLint  
Pylint es es un verificador de código fuente, errores y calidad para el lenguaje de programación Python.  
(PyLint no se puede integrar con Tox en este momento. Por ello, es necesario ejecutarlo por separado)

```bash
    $ pip install pylint
```

Se ejecuta con el siguiente comando:

```bash
    $ pylint -r y -s y -f json --exit-zero <SOURCE_CODE_PATH> > reports/pylint.json
```

**Paso 5**  
Analisis con Sonar.  
A continuación se muestra ejemplo de fichero *sonar-project.properties* donde configuraremos la forma en la que Sonar va a analizar nuestro código:


````
sonar.projectKey=<PROJECT_KEY>                          # codigo del proyecto con formato datalake:project:module
sonar.projectName=<PROJECT_NAME>                        # Nombre del proyecto que aparecerá en Sonar
sonar.projectVersion=1.1.0                              # Versión de analisis del proyecto

sonar.sources=src                                       # Carpeta donde se encuentran las fuentes
sonar.tests=tests                                       # Carpeta donde se localizan los tests

sonar.inclusions=src/**/*.py                            # Ficheros fuente a incluir en el analisis
sonar.test.inclusions=tests/**/*.py                     # Ficheros de tests a incluir en el análisis

sonar.sourceEncoding=UTF-8                              # Codificación de las fuentes
sonar.language=py                                       # Lenguaje por defecto del proyecto

sonar.python.xunit.reportPaths=xunit-*.xml              # Fichero de reporte de los test unitarios
sonar.python.xunit.skipDetails=false

sonar.python.coverage.reportPaths=coverage.xml          # Fichero de reporting de cobertura
sonar.python.codeCoveragePlugin=cobertura               # Plugin que utilizará sonar para la cobertura

sonar.python.bandit.reportPaths=reports/bandit.json     # Localización reporting de bandit
sonar.python.pylint.reportPath=reports/pylint.json      # Localización reporting de pylint
```` 

**Paso 6**  
Preparando estructura del proyecto.

````
src/
| - __init__.py
| - [RESTO CÓDIGO]
tests/
| - [FICHEROS DE TEST]
    | 
test_requirements.txt
tox.ini
````

*Ficheros de test deben tener el prefijo test_ en su nombre*

**Paso 7**  
Fichero conftest.py

Las "fixtures" de Pytest son el uso habitual de conftest.py. Las "fixture" que se definan se compartirán entre todos los tests.  
En este caso se utiliza para definir recursos de AWS que serán utilizados durante los tests

