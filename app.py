from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/proyecto'    #Editar para cada integrante la db respectiva con usuario y contrasenia
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    user = db.Column(db.String(80), primary_key = True)
    password = db.Column(db.String(80), nullable=False)
    es_admin = db.Column(db.Boolean, nullable=False)
    #personal = db.relationship('PersonalMedico', backref = 'usuario', uselist = False)
    #paciente = db.relationship('Usuario', backref = 'usuario', uselist = False)

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
    
    def __repr__(self):
        return f'<Usuario: {self.dni}, {self.nombre}, {self.apellido}, {self.titulo}, {self.especialidad}, {self.usuario}>'
    def __init__(self, dni, nombre, apellido, titulo, especialidad, usuario):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.titulo = titulo
        self.especialidad = especialidad
        self.usuario = usuario

class Residencia(db.Model):
    __tablename__ = 'residencia'
    nombre = db.Column(db.String(20), primary_key = True)
    direccion = db.Column(db.String(80), nullable = False)
    no_habitaciones = db.Column(db.Integer)
    director = db.Column(db.String(20), nullable = False)
    #personal = db.relationship('PersonalMedico', backref = 'residencia')
    #pacientes = db.relationship('Paciente', backref = 'residencia')

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

db.create_all()

sanjuan = Residencia("San Juan", "Surco", 21, "Carmen Durant")
losportales = Residencia("Los Portales", "La Molina", 23, "Erika Guillen")

usuario1 = Usuario("sgutierrez", "1234", False)
usuario2 = Usuario("fsantos", "1234", False)
usuario3 = Usuario("egambirazio", "1234", False)
usuario4 = Usuario("rvega", "1234", False)
usuario5 = Usuario("lrodriguez", "1234", False)
usuario6 = Usuario("fnovoa", "1234", False)
usuario7 = Usuario("mchavez", "1234", False)
usuario8 = Usuario("lbalta", "1234", False)
usuario9 = Usuario("hdurand", "1234", False)
usuario10 = Usuario("dtafur", "1234", False)

db.session.add_all( [sanjuan, losportales, usuario1, usuario2, usuario3, usuario4, usuario5, usuario6, 
usuario7, usuario8, usuario9, usuario10])
db.session.commit()

medico1 = PersonalMedico(71284499, "Santiago", "Gutierrez", "Doctor", "Neurólogía", "sgutierrez")
medico2 = PersonalMedico(84909223, "Fabricio", "Santos", "Doctor", "Cardiólogía", "fsantos")
medico3 = PersonalMedico(83919223, "Esteban", "Gambirazio", "Doctor", "Traumatólogía", "egambirazio")
medico4 = PersonalMedico(72876544, "Romario", "Vega", "Doctor", "Neurólogía", "rvega")
medico5 = PersonalMedico(62345678, "Luis", "Rodriguez", "Doctor", "Endocrinología", "lrodriguez")
enfermera1 = PersonalMedico(10278990, "Fátima", "Novoa", "Enfermera", "Geriatría", "fnovoa")
enfermera2 = PersonalMedico(10278991, "Micaela", "Chavez", "Enfermera", "Geriatría", "mchavez")
enfermera3 = PersonalMedico(10278992, "Luciana", "Balta", "Enfermera", "Geriatría", "lbalta")
enfermera4 = PersonalMedico(10278993, "Haydi", "Durand", "Enfermera", "Geriatría", "hdurand")
enfermera5 = PersonalMedico(10278994, "Daniela", "Tafur", "Enfermera", "Geriatría", "dtafur")

db.session.add_all( [medico1, medico2, medico3, medico4, medico5, enfermera1, 
enfermera2, enfermera3, enfermera4, enfermera5]
)
db.session.commit()

@app.route('/')
def index():
    return "<h1> April la más fea </h1>"

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5002, debug = True)
