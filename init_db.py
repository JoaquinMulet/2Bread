import os
import shutil
from app import app, db

def init_db():
    """
    Inicializa la base de datos en el volumen de Railway si es necesario.
    También copia la base de datos local al volumen si existe y el volumen está vacío.
    """
    with app.app_context():
        # Verificar si estamos usando un volumen
        volume_path = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH', '')
        if volume_path:
            print(f"Usando volumen en: {volume_path}")
            
            # Asegurarse de que el directorio existe
            os.makedirs(volume_path, exist_ok=True)
            
            # Ruta de la base de datos en el volumen
            db_path = os.path.join(volume_path, 'biblioteca.db')
            
            # Verificar si la base de datos ya existe en el volumen
            if not os.path.exists(db_path):
                print("La base de datos no existe en el volumen.")
                
                # Verificar si existe una base de datos local para copiar
                local_db = 'biblioteca.db'
                if os.path.exists(local_db):
                    print(f"Copiando base de datos local a {db_path}")
                    shutil.copy2(local_db, db_path)
                else:
                    print("Creando nueva base de datos en el volumen")
            
            # Crear todas las tablas si no existen
            db.create_all()
            print("Base de datos inicializada correctamente")
        else:
            print("No se detectó volumen de Railway, usando configuración local")
            db.create_all()

if __name__ == "__main__":
    init_db()
