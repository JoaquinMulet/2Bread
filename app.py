from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

# Configuración de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave_secreta_para_sesiones')

# Configuración de la base de datos para Railway Volumes
volume_path = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH', '')
if volume_path:
    # Si estamos en Railway con un volumen montado
    db_path = os.path.join(volume_path, 'biblioteca.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
else:
    # Configuración local o fallback
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///biblioteca.db')

# Convertir postgres:// a postgresql:// si es necesario
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Modelos de la base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    votos = db.relationship('Voto', backref='votante', lazy=True)

class ListaLibros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activa = db.Column(db.Boolean, default=True)
    libros = db.relationship('Libro', backref='lista', lazy=True)

class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100))
    lista_id = db.Column(db.Integer, db.ForeignKey('lista_libros.id'), nullable=False)
    votos = db.relationship('Voto', backref='libro', lazy=True)
    
    @property
    def puntos_totales(self):
        return sum(voto.puntos for voto in self.votos)

class Voto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    libro_id = db.Column(db.Integer, db.ForeignKey('libro.id'), nullable=False)
    lista_id = db.Column(db.Integer, db.ForeignKey('lista_libros.id'), nullable=False)
    puntos = db.Column(db.Integer, nullable=False)  # 5, 4, 3, 2, 1 según prioridad
    
    __table_args__ = (
        db.UniqueConstraint('usuario_id', 'libro_id', 'lista_id', name='uq_voto_usuario_libro_lista'),
    )

# Rutas
@app.route('/')
def index():
    listas = ListaLibros.query.filter_by(activa=True).all()
    return render_template('index.html', listas=listas)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        es_admin = 'es_admin' in request.form
        
        # Buscar si el usuario ya existe
        usuario = Usuario.query.filter_by(nombre=nombre).first()
        
        if not usuario:
            # Crear nuevo usuario
            usuario = Usuario(nombre=nombre, es_admin=es_admin)
            db.session.add(usuario)
            db.session.commit()
        
        session['usuario_id'] = usuario.id
        session['es_admin'] = usuario.es_admin
        session['nombre'] = usuario.nombre
        
        if usuario.es_admin:
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if not session.get('es_admin'):
        flash('No tienes permisos de administrador')
        return redirect(url_for('index'))
    
    listas = ListaLibros.query.all()
    return render_template('admin.html', listas=listas)

@app.route('/admin/lista/nueva', methods=['POST'])
def nueva_lista():
    if not session.get('es_admin'):
        return jsonify({'error': 'No autorizado'}), 403
    
    nombre = request.form.get('nombre')
    if not nombre:
        flash('El nombre de la lista es obligatorio')
        return redirect(url_for('admin'))
    
    lista = ListaLibros(nombre=nombre)
    db.session.add(lista)
    db.session.commit()
    
    flash(f'Lista "{nombre}" creada correctamente')
    return redirect(url_for('admin'))

@app.route('/admin/lista/<int:lista_id>')
def editar_lista(lista_id):
    if not session.get('es_admin'):
        flash('No tienes permisos de administrador')
        return redirect(url_for('index'))
    
    lista = ListaLibros.query.get_or_404(lista_id)
    return render_template('editar_lista.html', lista=lista)

@app.route('/admin/lista/<int:lista_id>/libro/nuevo', methods=['POST'])
def nuevo_libro(lista_id):
    if not session.get('es_admin'):
        return jsonify({'error': 'No autorizado'}), 403
    
    titulo = request.form.get('titulo')
    autor = request.form.get('autor', '')
    
    if not titulo:
        flash('El título del libro es obligatorio')
        return redirect(url_for('editar_lista', lista_id=lista_id))
    
    libro = Libro(titulo=titulo, autor=autor, lista_id=lista_id)
    db.session.add(libro)
    db.session.commit()
    
    flash(f'Libro "{titulo}" añadido correctamente')
    return redirect(url_for('editar_lista', lista_id=lista_id))

@app.route('/admin/lista/<int:lista_id>/toggle', methods=['POST'])
def toggle_lista(lista_id):
    if not session.get('es_admin'):
        return jsonify({'error': 'No autorizado'}), 403
    
    lista = ListaLibros.query.get_or_404(lista_id)
    lista.activa = not lista.activa
    db.session.commit()
    
    estado = "activada" if lista.activa else "desactivada"
    flash(f'Lista "{lista.nombre}" {estado} correctamente')
    return redirect(url_for('admin'))

@app.route('/lista/<int:lista_id>')
def ver_lista(lista_id):
    lista = ListaLibros.query.get_or_404(lista_id)
    libros = Libro.query.filter_by(lista_id=lista_id).all()
    
    # Verificar si el usuario ha votado en esta lista
    usuario_id = session.get('usuario_id')
    ha_votado = False
    votos_usuario = []
    
    if usuario_id:
        votos_usuario = Voto.query.filter_by(usuario_id=usuario_id, lista_id=lista_id).all()
        ha_votado = len(votos_usuario) > 0
    
    return render_template('lista.html', lista=lista, libros=libros, ha_votado=ha_votado, votos_usuario=votos_usuario)

@app.route('/lista/<int:lista_id>/votar', methods=['POST'])
def votar(lista_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Debes iniciar sesión para votar')
        return redirect(url_for('login'))
    
    lista = ListaLibros.query.get_or_404(lista_id)
    if not lista.activa:
        flash('Esta lista no está activa para votación')
        return redirect(url_for('index'))
    
    # Verificar si el usuario ya ha votado en esta lista
    votos_existentes = Voto.query.filter_by(usuario_id=usuario_id, lista_id=lista_id).all()
    if votos_existentes:
        flash('Ya has votado en esta lista')
        return redirect(url_for('ver_lista', lista_id=lista_id))
    
    # Procesar los votos (5, 4, 3, 2, 1 puntos)
    votos_registrados = 0
    for i in range(1, 6):
        libro_id = request.form.get(f'libro_{i}')
        if libro_id:
            puntos = 6 - i  # 5, 4, 3, 2, 1
            voto = Voto(usuario_id=usuario_id, libro_id=libro_id, lista_id=lista_id, puntos=puntos)
            db.session.add(voto)
            votos_registrados += 1
    
    if votos_registrados == 0:
        flash('Debes seleccionar al menos un libro para votar')
        return redirect(url_for('ver_lista', lista_id=lista_id))
    
    db.session.commit()
    flash(f'Tu voto ha sido registrado correctamente. Has votado por {votos_registrados} libro(s).')
    return redirect(url_for('resultados', lista_id=lista_id))

@app.route('/lista/<int:lista_id>/resultados')
def resultados(lista_id):
    lista = ListaLibros.query.get_or_404(lista_id)
    libros = Libro.query.filter_by(lista_id=lista_id).all()
    
    # Calcular puntos totales para cada libro
    resultados = []
    for libro in libros:
        puntos = sum(voto.puntos for voto in libro.votos)
        resultados.append({
            'libro': libro,
            'puntos': puntos,
            'votos': len(libro.votos)
        })
    
    # Ordenar por puntos (de mayor a menor)
    resultados.sort(key=lambda x: x['puntos'], reverse=True)
    
    return render_template('resultados.html', lista=lista, resultados=resultados)

# Inicializar la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Importar aquí para evitar importaciones circulares
    from init_db import init_db
    init_db()
    app.run(debug=True)
