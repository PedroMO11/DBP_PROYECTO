from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/proyecto'    #Editar para cada integrante la db respectiva con usuario y contrasenia
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    user = db.Column(db.String(80), primary_key = True)
    password = db.Column(db.String(80), nullable=False)
    es_admin = db.Column(db.Boolean, nullable=False)
    personal = db.relationship('PersonalMedico', backref = 'usuario_personal', uselist = False, primaryjoin= "Usuario.user == foreign(PersonalMedico.usuario)")
    paciente = db.relationship('Paciente', backref = 'usuario_paciente', uselist = False, primaryjoin= "Usuario.user == foreign(Paciente.usuario)")

    def __repr__(self):
        return f'<Usuario: {self.user}, {self.password}, {self.es_admin}>'

    def __init__(self, user, password, es_admin):
        self.user = user
        self.password = password
        self.es_admin = es_admin

class PersonalMedico(db.Model):
    __tablename__ = 'personal'
    dni = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80), nullable = False)
    apellido = db.Column(db.String(80), nullable = False)
    titulo = db.Column(db.String(80), nullable = False)
    especialidad = db.Column(db.String(80), nullable = False)
    usuario = db.Column(db.String(80), db.ForeignKey('usuario.user'), nullable = False)
    residencia = db.Column(db.String(80), db.ForeignKey('residencia.nombre'), nullable = False)
    
    def __repr__(self):
        return f'<Usuario: {self.dni}, {self.nombre}, {self.apellido}, {self.titulo}, {self.especialidad}, {self.usuario}>'
    
    def __init__(self, dni, nombre, apellido, titulo, especialidad, usuario, residencia):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.titulo = titulo
        self.especialidad = especialidad
        self.usuario = usuario
        self.residencia = residencia

class Residencia(db.Model):
    __tablename__ = 'residencia'
    nombre = db.Column(db.String(20), primary_key = True)
    direccion = db.Column(db.String(80), nullable = False)
    no_habitaciones = db.Column(db.Integer)
    director = db.Column(db.String(20), nullable = False)
    personal = db.relationship('PersonalMedico', backref = 'residencia_personal', lazy = "dynamic", primaryjoin = "Residencia.nombre == PersonalMedico.residencia")
    pacientes = db.relationship('Paciente', backref = 'residencia_paciente', lazy = "dynamic",  primaryjoin= "Residencia.nombre == Paciente.residencia")

    def __repr__(self):
        return f'<Residencia: {self.id}, {self.nombre}, {self.direccion}, {self.no_habitaciones}, {self.director}>'

    def __init__(self, nombre, direccion, no_habitaciones, director):
        self.nombre = nombre
        self.direccion = direccion
        self.no_habitaciones = no_habitaciones
        self.director = director


class Paciente(db.Model):
    ___tablename__ = 'paciente'
    dni = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80), nullable = False)
    apellido = db.Column(db.String(80), nullable = False)
    titulo = db.Column(db.String(80), nullable = False)
    especialidad = db.Column(db.String(80), nullable = False)
    residencia = db.Column(db.String(20), db.ForeignKey('residencia.nombre'), nullable = False)
    usuario = db.Column(db.String(80), db.ForeignKey('usuario.user'), nullable = False)

    def __repr__(self):
        return f'<Paciente : {self.dni}, {self.nombre}, {self.apellido}, {self.especialidad}, {self.residencia}, {self.usuario}>'

    def __init__(self, dni, nombre, apellido, titulo, especialidad, residencia, usuario):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.titulo = titulo
        self.especialidad = especialidad
        self.residencia = residencia
        self.usuario = usuario

@app.route('/')
def index():
    return "<h1> Hola </h1>"

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5002, debug = True)
