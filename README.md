# Biblioteca Democrática - Sistema de Votación de Libros

Una aplicación web simple para crear listas de libros y realizar votaciones democráticas con un sistema de puntos.

## Características

- **Panel de Administración**: Crear y gestionar listas de libros
- **Sistema de Votación**: Los usuarios pueden votar por sus 5 libros favoritos con puntos (5, 4, 3, 2, 1)
- **Resultados Visuales**: Visualización de resultados con gráficos
- **Interfaz Intuitiva**: Diseño responsive y fácil de usar

## Requisitos

- Python 3.6 o superior
- Flask y otras dependencias (ver `requirements.txt`)

## Instalación

1. Clona o descarga este repositorio
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:

```bash
python app.py
```

4. Abre tu navegador y ve a `http://localhost:5000`

## Uso

### Para Administradores

1. Inicia sesión marcando la casilla "Soy administrador"
2. Crea una nueva lista de libros
3. Añade libros a la lista
4. Activa o desactiva listas según sea necesario

### Para Usuarios

1. Inicia sesión con tu nombre
2. Selecciona una lista de libros disponible
3. Vota por tus 5 libros favoritos en orden de preferencia
4. Visualiza los resultados de la votación

## Despliegue en Railway

### Configuración con Railway Volumes

Para desplegar esta aplicación en Railway utilizando Volumes para almacenar la base de datos:

1. Crea un nuevo proyecto en Railway y conecta tu repositorio.

2. Agrega un volumen a tu servicio:
   - Ve a la pestaña "Volumes" en tu servicio.
   - Haz clic en "Add Volume".
   - Configura el punto de montaje como `/app/data` (o cualquier otra ruta).
   - Selecciona el tamaño adecuado para tu volumen.

3. Configura las variables de entorno:
   - `SECRET_KEY`: Una clave secreta para las sesiones (genera una clave segura).
   - `RAILWAY_VOLUME_MOUNT_PATH`: La ruta donde se montará el volumen (por ejemplo, `/app/data`).

4. Despliega la aplicación.

La aplicación detectará automáticamente el volumen y creará/utilizará la base de datos SQLite en esa ubicación.

### Migración de datos existentes

Si ya tienes una base de datos local y deseas migrarla al volumen:

1. Asegúrate de que la base de datos local esté en el repositorio (temporalmente).
2. Despliega la aplicación - el script `init_db.py` copiará automáticamente la base de datos local al volumen.
3. Una vez confirmado que funciona, elimina la base de datos del repositorio y actualiza el `.gitignore`.

## Estructura del Proyecto

- `app.py`: Archivo principal de la aplicación Flask
- `templates/`: Plantillas HTML
- `static/`: Archivos estáticos (CSS, JavaScript)
- `biblioteca.db`: Base de datos SQLite (se crea automáticamente)

## Sistema de Puntuación

- 1ª elección: 5 puntos
- 2ª elección: 4 puntos
- 3ª elección: 3 puntos
- 4ª elección: 2 puntos
- 5ª elección: 1 punto

Los resultados se ordenan por la suma total de puntos recibidos.

## Licencia

Este proyecto es de código abierto y está disponible para su uso y modificación.
