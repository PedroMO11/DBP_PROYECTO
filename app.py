from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_manager, login_user, login_required, logout_user, current_user
from flask.helpers import flash
#import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/proyecto'    #Editar para cada integrante la db respectiva con usuario y contrasenia
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hjklhklhlk'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    user = db.Column(db.String(80), primary_key = True)
    password = db.Column(db.String(8), nullable=False)
    es_admin = db.Column(db.Boolean, nullable=False)
    personal = db.relationship('PersonalMedico', backref = 'usuario_personal', uselist = False, primaryjoin= "Usuario.user == foreign(PersonalMedico.usuario)")
    paciente = db.relationship('Paciente', backref = 'usuario_paciente', uselist = False, primaryjoin= "Usuario.user == foreign(Paciente.usuario)")

class PersonalMedico(db.Model):
    __tablename__ = 'personal'
    dni = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80), nullable = False)
    apellido = db.Column(db.String(80), nullable = False)
    titulo = db.Column(db.String(80), nullable = False)
    especialidad = db.Column(db.String(80), nullable = False)
    usuario = db.Column(db.String(80), db.ForeignKey('usuario.user'), nullable = False)
    residencia = db.Column(db.Integer, db.ForeignKey('residencia.id'), nullable = False)
    
class Residencia(db.Model):
    __tablename__ = 'residencia'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(20), nullable = False)
    direccion = db.Column(db.String(80), nullable = False)
    no_habitaciones = db.Column(db.Integer)
    director = db.Column(db.String(20), nullable = False)
    personal = db.relationship('PersonalMedico', backref = 'residencia_personal', lazy = "dynamic", primaryjoin = "Residencia.id == PersonalMedico.residencia")
    pacientes = db.relationship('Paciente', backref = 'residencia_paciente', lazy = "dynamic",  primaryjoin= "Residencia.id == Paciente.residencia")

class Paciente(db.Model):
    ___tablename__ = 'paciente'
    dni = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80), nullable = False)
    apellido = db.Column(db.String(80), nullable = False)
    edad = db.Column(db.Integer, nullable = False)
    habitacion = db.Column(db.Integer, nullable = False)
    residencia = db.Column(db.Integer, db.ForeignKey('residencia.id'), nullable = False)
    usuario = db.Column(db.String(80), db.ForeignKey('usuario.user'))
    
login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user):
    return Usuario.query.get(user)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form.get('user')
    contraseña = request.form.get('password')
    user = Usuario.query.filter_by(user=usuario).first()
    if user:
        if user.password == contraseña:
            flash('Correcto inicio sesion', category='success')
            login_user(user, remember=True) #min 1:50:30
            return redirect('/')
        else:
            flash('Contraseña incorrecta', category='error')
    else:
        flash('Usuario no existe', category='error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user
    return redirect(url_for('login'))


@app.route('/registro_usuario', methods=['POST'] )
def registro_usuario():
    usuario = request.form.get('user1')
    password = request.form.get('password1')
    rol = request.form.get('rol')

    user = Usuario.query.filter_by(user=usuario).first()
    if user:
        flash('El usuario ya existe', category='error')
    elif len(usuario) < 5:
        flash('El usuario tiene pocos caracteres', category='error')
    elif len(password) < 5:
        flash('La contraseña es muy corta', category='error')
    elif len(rol) <5:
        flash('Rol no valido', category='error')
        print(rol)
    else:
        nuevoUsuario = Usuario(user=usuario, password=password, rol=rol)
        db.session.add(nuevoUsuario)
        db.session.commit()
        login_user(user, remember=True)
        flash('Usuario creado correctamente', category='success')
        return redirect('/')
    return render_template("registro_usuario.html")

@app.route('/registro_paciente', methods=['POST'])
@login_required
def registro_paciente():
    #error = False
    #response = {}
    
    dni = request.form.get('dni')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    edad = request.form.get('edad')
    habitacion = request.form.get('habitacion')
    residencia = request.form.get('residencia')
    paciente = Paciente(dni, nombre, apellido, edad, habitacion, residencia)
    db.session.add(paciente)
    db.session.commit()
    '''
    except:
        #error = True
        db.session.rollback()
        print(sys.exc_info)
    finally:
        db.session.close()
    '''
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5002, debug = True)
