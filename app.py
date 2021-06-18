from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_manager, login_user, login_required, logout_user, current_user
from flask.helpers import flash
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/proyecto"    #Editar para cada integrante la db respectiva con usuario y contrasenia
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hjklhklhlk'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(8), nullable=False)
    es_admin = db.Column(db.Boolean, nullable=False)
    personal = db.relationship('PersonalMedico', backref = 'usuario_personal', uselist = False, primaryjoin= "Usuario.user == foreign(PersonalMedico.usuario)")
    paciente = db.relationship('Paciente', backref = 'usuario_paciente', uselist = False, primaryjoin= "Usuario.user == foreign(Paciente.usuario)")

    def __repr__(self):
        return f'<Usuario: {self.id}, {self.user}, {self.password}, {self.es_admin}>'


class PersonalMedico(db.Model):
    __tablename__ = 'personal'
    dni = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80), nullable = False)
    apellido = db.Column(db.String(80), nullable = False)
    titulo = db.Column(db.String(80), nullable = False)
    especialidad = db.Column(db.String(80), nullable = False)
    usuario = db.Column(db.String(80), db.ForeignKey('usuario.user'))
    residencia = db.Column(db.Integer, db.ForeignKey('residencia.id'), nullable = False)

    def __repr__(self):
        return f'<PersonalMedico: {self.dni}, {self.nombre}, {self.apellido}, {self.titulo}, {self.especialidad}, {self.usuario},  {self.residencia}>'
    
class Residencia(db.Model):
    __tablename__ = 'residencia'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(20), nullable = False)
    direccion = db.Column(db.String(80), nullable = False)
    no_habitaciones = db.Column(db.Integer)
    director = db.Column(db.String(20), nullable = False)
    personal = db.relationship('PersonalMedico', backref = 'residencia_personal', lazy = "dynamic", primaryjoin = "Residencia.id == PersonalMedico.residencia")
    pacientes = db.relationship('Paciente', backref = 'residencia_paciente', lazy = "dynamic",  primaryjoin= "Residencia.id == Paciente.residencia")

    def __repr__(self):
        return f'<Residencia: {self.id}, {self.nombre}, {self.direccion}, {self.no_habitaciones}, {self.director}>'


class Paciente(db.Model):
    ___tablename__ = 'paciente'
    dni = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(80), nullable = False)
    apellido = db.Column(db.String(80), nullable = False)
    edad = db.Column(db.Integer, nullable = False)
    habitacion = db.Column(db.Integer, nullable = False)
    residencia = db.Column(db.Integer, db.ForeignKey('residencia.id'), nullable = False)
    usuario = db.Column(db.String(80), db.ForeignKey('usuario.user'))

    def __repr__(self):
        return f'<Paciente : {self.dni}, {self.nombre}, {self.apellido}, {self.edad}, f{self.residencia}, {self.usuario}>'

    
login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

@app.errorhandler(Exception)
def handle_500(e):
    if isinstance(e, HTTPException):
        return e
    return render_template('500.html', e=e), 500

@app.route('/')
def index():
    return render_template('home.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
    return render_template('login.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/pacientes/<paciente_dni>/editar', methods = ['GET', 'POST'])
def editar_paciente_by_dni(paciente_dni):
    error = False
    response = {}
    try:
        dni = request.get_json()['dni']
        persona = Paciente.query.get(dni)
        res = request.get_json()['residencia_id']
        residencia = Residencia.query.get(res)
        persona.nombre = request.get_json()['nombre']
        persona.apellido = request.get_json()['apellido']
        persona.edad = request.get_json()['edad']
        persona.habitacion = request.get_json()['habitacion']
        persona.residencia_paciente = residencia
        db.session.commit()
        response['message'] = 'Paciente editado correctamente'
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        response['message'] = 'Error en BE'
    
    response['error'] = error
    return jsonify(response)


@app.route('/editar-paciente/<paciente_dni>', methods = ['GET'])
def editar_paciente(paciente_dni):
    paciente = Paciente.query.get(paciente_dni)
    return render_template('editar_paciente.html', user=current_user, paciente = paciente)

@app.route('/usuarios/<user>/registrar', methods = ['GET', 'POST'])
def registrar_usuario_by_id(user):
    error = False
    response = {}
    try:
        usuario = request.get_json()['user']
        password = request.get_json()['password']
        es_admin = request.get_json()['es_admin']
        dni = request.get_json()['dni']
        personal = PersonalMedico.query.get(dni)
        persona = Paciente.query.get(dni)
        if es_admin == '1':
            admin = True
        else:
            admin = False
        if len(dni) != 8:
            response['message'] = 'DNI inválido'
        elif len(password) > 5:
            response['message'] = 'La contraseña debe tener por lo menos 5 carateres'
        else:
            if admin:
                if (persona == None and personal == None):
                    user = Usuario.query.filter_by(user=usuario).first()
                    if user:
                        response['message'] = 'Usuario ya existe'
                    else:
                        nombre = request.get_json()['nombre']
                        apellido = request.get_json()['apellido']
                        titulo = request.get_json()['titulo']
                        especialidad = request.get_json()['especialidad']
                        res = request.get_json()['residencia_id']
                        residencia = Residencia.query.get(res)
                        nuevoUsuario = Usuario(user=usuario, password=password, es_admin=admin)
                        nuevoPersonal = PersonalMedico(dni = dni, nombre=nombre, apellido=apellido, titulo=titulo, especialidad=especialidad,residencia_personal=residencia,usuario_personal=nuevoUsuario)
                        db.session.add(nuevoUsuario)
                        db.session.add(nuevoPersonal)
                        db.session.commit()
                        print(nuevoPersonal)
                        response['message'] = 'Usuario creado correctamente'
            else:
                if (persona):
                    if (persona.usuario == None):
                        user = Usuario.query.filter_by(user=usuario).first()
                        if user:
                            response['message'] = 'Usuario ya existe'
                        else:
                            nuevoUsuario = Usuario(user=usuario, password=password, es_admin=admin)
                            persona.usuario_paciente = nuevoUsuario
                            db.session.add(nuevoUsuario)
                            db.session.commit()
                            response['message'] = 'Usuario creado correctamente'
                    else:
                        response['message'] = 'Paciente ya tiene cuenta registrada'
                else:
                    response['message'] = 'DNI de paciente no existe'
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        response['message'] = 'Error en el BE'
    
    response['error'] = error

    return jsonify(response)

@app.route('/registro_usuario', methods=['GET', 'POST'] )
def registro_usuario():
    return render_template('registro_usuario.html', user=current_user)

@app.route('/registro_paciente', methods=['GET', 'POST'])
@login_required
def registro_paciente():
    #error = False
    #response = {}
    if request.method == 'POST':
        dni = request.get_json()['dni']
        persona = Paciente.query.get(dni)
        if persona:
            flash('Persona con este DNI ya ha sido registrada', category = 'error')
        else:
            nombre = request.get_json()['nombre']
            apellido = request.get_json()['apellido']
            edad = request.get_json()['edad']
            habitacion = request.get_json()['habitacion']
            res = request.get_json()['residencia']
            residencia = Residencia.query.get(res)
            paciente = Paciente(dni=dni, nombre=nombre, apellido=apellido, edad=edad, habitacion=habitacion, residencia_paciente=residencia)
            db.session.add(paciente)
            db.session.commit()
            flash('Paciente registrado correctamente', category = 'success')
    '''
    except:
        #error = True
        db.session.rollback()
        print(sys.exc_info)
    finally:
        db.session.close()
    '''
    return render_template('registro_paciente.html', user = current_user)

@app.route('/pacientes/<paciente_id>/registrar', methods = ['GET', 'POST'])
@login_required
def registrar_paciente_by_id(paciente_id):
    error = False
    response = {}
    persona = Paciente.query.get(paciente_id)

    try:
        if len(paciente_id) != 8:
            response['message'] = 'DNI inválido'
        elif persona:
            response['message'] = 'Persona con este DNI ya ha sido registrada'
            response['category'] = 'error'
        else:
            nombre = request.get_json()['nombre']
            apellido = request.get_json()['apellido']
            edad = request.get_json()['edad']
            habitacion = request.get_json()['habitacion']
            res = request.get_json()['residencia_id']
            residencia = Residencia.query.get(res)
            paciente = Paciente(dni=paciente_id, nombre=nombre, apellido=apellido, edad=edad, habitacion=habitacion, residencia_paciente=residencia)
            db.session.add(paciente)
            db.session.commit()
            response['message'] = 'Paciente registrado correctamente'
            response['category'] = 'success'
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    
    if error:
        response['message'] = 'Error en el BE'

    response['error'] = error
    return jsonify(response)

@app.route('/pacientes')
@login_required
def ver_pacientes():
    return render_template('ver_pacientes.html', pacientes = Paciente.query.all(), user = current_user)

@app.route('/pacientes/<paciente_dni>/delete-paciente', methods = ['DELETE'])
@login_required
def delete_paciente_by_id(paciente_dni):
    response = {}
    paciente = Paciente.query.get(paciente_dni)
    user = paciente.usuario_paciente
    if paciente is None:
        response['message'] = 'No existe paciente'
    else:
        response['message'] = 'Paciente eliminado con exito'
        db.session.delete(paciente)
        if user:
            usuario = Usuario.query.get(user.id)
            db.session.delete(usuario)
        db.session.commit()

    return jsonify(response)

    

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5002, debug = True)
