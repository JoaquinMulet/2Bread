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
