from app import *

sanjuan = Residencia(id = 1, nombre = "San Juan", direccion = "Surco", no_habitaciones = 21, director = "Carmen Durant")
losportales = Residencia(id = 2, nombre = "Los Portales", direccion = "La Molina", no_habitaciones = 23, director = "Erika Guillen")

db.session.add_all([sanjuan, losportales])
db.session.commit()

usuario1 = Usuario(user = "sgutierrez", password = "1234", es_admin = 1)
usuario2 = Usuario(user= "fsantos",password =  "1234", es_admin = 1)
usuario3 = Usuario(user = "egambirazio", password = "1234",es_admin = 1)
usuario4 = Usuario(user = "rvega", password ="1234", es_admin = 1)
usuario5 = Usuario(user = "lrodriguez", password = "1234", es_admin = 1)
usuario6 = Usuario(user = "fnovoa", password = "1234", es_admin = 1)
usuario7 = Usuario(user = "mchavez", password = "1234", es_admin = 1)
usuario8 = Usuario(user = "lbalta", password = "1234", es_admin = 1)
usuario9 = Usuario(user = "hdurand", password = "1234" ,es_admin = 1)
usuario10 = Usuario(user = "dtafur", password = "1234", es_admin = 1)
usuario11 = Usuario(user = "panchomb", password = "1234", es_admin = 0)

db.session.add_all([usuario1, usuario2, usuario3, usuario4, usuario5,usuario6, usuario7, usuario8, usuario9, usuario10, usuario11])
db.session.commit()

medico1 = PersonalMedico(dni = 71284499, nombre = "Santiago", apellido =  "Gutierrez",titulo =  "Doctor", especialidad =  "Neurología", residencia_personal = sanjuan, usuario_personal = usuario1)
medico2 = PersonalMedico(dni = 84909223, nombre =  "Fabricio", apellido = "Santos", titulo = "Doctor", especialidad = "Cardiologia", residencia_personal = sanjuan,usuario_personal = usuario2)
medico3 = PersonalMedico(dni = 17864008, nombre = "Esteban", apellido = "Gambirazio", titulo = "Doctor", especialidad = "Traumatologia", residencia_personal = sanjuan,usuario_personal = usuario3)
medico4 = PersonalMedico(dni = 72876544, nombre = "Romario", apellido = "Vega", titulo = "Doctor", especialidad =  "Neurologia", residencia_personal = losportales, usuario_personal = usuario4)
medico5 = PersonalMedico(dni = 62345678, nombre = "Luis", apellido = "Rodriguez", titulo = "Doctor", especialidad = "Endocrinologia", residencia_personal = sanjuan, usuario_personal = usuario5)
enfermera1 = PersonalMedico(dni = 73940772, nombre = "Fátima", apellido = "Novoa", titulo = "Enfermera", especialidad = "Geriatria", residencia_personal = sanjuan, usuario_personal = usuario6)
enfermera2 = PersonalMedico(dni = 10395847, nombre = "Micaela", apellido = "Chavez", titulo = "Enfermera", especialidad ="Geriatria", residencia_personal = losportales, usuario_personal = usuario7)
enfermera3 = PersonalMedico(dni = 10282084, nombre = "Luciana", apellido = "Balta", titulo = "Enfermera", especialidad = "Geriatria", residencia_personal = sanjuan, usuario_personal = usuario8)
enfermera4 = PersonalMedico(dni = 17820483, nombre = "Haydi", apellido = "Durand", titulo = "Enfermera", especialidad ="Geriatria", residencia_personal = losportales, usuario_personal = usuario9)
enfermera5 = PersonalMedico(dni = 93049588, nombre = "Daniela", apellido = "Tafur", titulo = "Enfermera", especialidad = "Geriatria", residencia_personal = losportales, usuario_personal = usuario10)

db.session.add_all([medico1, medico2, medico3, medico4, medico5, enfermera1, enfermera2, enfermera3, enfermera4, enfermera5])
db.session.commit()

paciente =  Paciente(dni = 73363673, nombre = "Francisco", apellido = "Magot", edad = 19, habitacion = 301, residencia_paciente = losportales, usuario_paciente = usuario11)

db.session.add(paciente)
db.session.commit()