# Servidor API con python

Vas a instalar un servidor API, que es un estándar de comunicación entre aplicaciones.
Existen muchas lenguajes de programación para implementarlo. Vas a usar python y a la librería FastAPI [enlace](https://fastapi.tiangolo.com/tutorial/first-steps/)

## 1. Instalación inicial

### 1.1. Entorno virtual

Por defecto tienes python instalado en tu sistema, pero es recomendable usar un entorno virtual para cada proyecto.

Esto es debido a que cada proyecto puede tener diferentes versiones de las librerías y versiones, y si las instalas globalmente pueden generar conflictos entre proyectos.

Crea un entorno virtual llamado `venv-api` con el siguiente comando:

```bash
python -m venv venv-api
```

Esto creará una carpeta llamada `venv-api` donde se instalarán las librerías del proyecto.
Indica en tu terminal que quieres usar el entorno virtual con el siguiente comando:

```bash
source venv-api/bin/activate
```

Puedes comprobar que estás usando el entorno virtual con el comando:

```bash
which python
```

### 1.2. Instalar librerías

Puedes comprobar que las librerías se han instalado correctamente con el siguiente comando (actualmente ninguna):

```bash
pip list
```

Crea el archivo `requirements.txt`, y escribe las librerías necesarias:

```
fastapi
uvicorn[standard]
```

Con el entorno virtual activado, instala las librerías del proyecto con el siguiente comando:

```bash
pip install -r requirements.txt
```

Ahora comprueba que están instaladas con `pip list`

## 2. Crear el servidor API

Crea la carpeta `src` para el código fuente: archivos `.py`. Ahí dentro crea el archivo `main.py`.
El resto de archivos como `Readme.md` y `requirements.txt` los puedes dejar en la raíz del proyecto.

En el archivo `main.py` escribe el siguiente código para crear un servidor API básico:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡Hola, soy...!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

```

### 2.1 Ejecutar el servidor API en local

Entra en la carpeta src `cd src`.

Para ejecutar el servidor API, usa el siguiente comando:

```bash
uvicorn main:app --reload --port 8000
```

El flag `--reload` es para que el servidor se recargue automáticamente cada vez que hagas cambios en el código.

El servidor API arrancará en `http://localhost:8000`. Accede a las siguientes rutas:

- `http://localhost:8000/` para ver el mensaje "¡Hola, mundo!"
- `http://localhost:8000/items/1` para ver el item con id
- `http://localhost:8000/docs` o `http://localhost:8000/redoc` para ver la documentación automática de la API.

## 3. Subir el proyecto a GitHub

- **Git** es un sistema de control de versiones que te permite llevar un historial de los cambios en tu código y colaborar con otros desarrolladores.
- **GitHub** es una plataforma de alojamiento en la nube de código que utiliza Git para gestionar los repositorios y sus versiones. Ampliamente utilizado como curriculum para mostrar tus proyectos a futuros empleadores.

### 3.1. Git

Asegurate de estar en la raíz del proyecto (NO en la carpeta `./src`).

Primero crea un archivo llamado `.gitignore` donde indicarémos que archivos o carpetas no vamos a guardar. Como son las librerías externas que podemos descargar.

```
venv-api/
```

Y ejecuta los siguientes comandos:

```bash
git init
```

`git init` inicializa un nuevo repositorio Git en tu proyecto. Solo se hace la primera vez. Crea la carpeta `.git` donde se guardarán todas tus versiones. Ejecuta `ls --all` para listar todas las carpetas, incluyendo los ocultos que empiezan por punto '.'

Ahora ejecuta `git status` para ver el estado de tus archivos. Hay 3 estados [enlace](https://velog.velcdn.com/images/silvercastle/post/e168e7f9-74aa-4c65-aeea-8216a19dabc8/image.png):
| Working Directory | staging | committed |
| --- | --- | --- |
| El archivo no está siendo trackeado por git. | El archivo está listo para ser committeado. | Guardado en el historial de versiones. |

`git add .` añade todos los archivos de la carpeta actual `.` al staging area, es decir, los prepara para ser committeados/guardados. Y revisa con `git status`.

```bash
git add .
```

Si son los archivos deseados, commitea/guarda la version actual con un mensaje descriptivo con el siguiente comando:

```bash
git commit -m "Initial commit"
```

Revisa con `git status` y mira el historial de versiones con:

```bash
git --no-pager log --oneline --graph --all --decorate
```

### 3.2. GitHub

Súbelo a github. Para ello primera crea un nuevo repositorio en GitHub con un nombre y configuración por defecto.

Luego vincula tu repositorio local con el remoto de GitHub (origin):

```bash
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
```

Finalmente sube los cambios (upload) a origin (GitHub) de tu local (main):

```bash
git push -u origin main
```

## 4. Despliegue en la nube

Antes de despliegue asegurate que el servidor lanza tu nombre.

El API se despliega en un servidor (no un hosting):

- Hosting: Aloja páginas web estáticas (HTML, CSS, JS). Pero el código (javascript) se ejecuta en el navegador del cliente.
- Servidor: Aloja aplicaciones web dinámicas (Python, Node.js, etc). El código se ejecuta en el servidor y el cliente solo recibe el resultado.

Para ello vas a usar Railway [enlace](https://railway.app/), que es una plataforma de despliegue en la nube.

1. Deberás registrarte usando tu cuenta de GitHub.
2. Crea un nuevo proyecto y selecciona "Deploy from GitHub repo" y selecciona el repositorio de tu proyecto.
3. Railway detectará automáticamente el proyecto y te pedirá que selecciones el comando de inicio. Selecciona `uvicorn main:app --reload --port 8000`.
4. Railway instalará las dependencias y desplegará el servidor API.
5. Una vez desplegado, podrás acceder a tu API desde la URL que te proporcionará Railway.
