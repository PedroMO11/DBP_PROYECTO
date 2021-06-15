from app import *

sanjuan = Residencia("San Juan", "Surco", 21, "Carmen Durant")
losportales = Residencia("Los Portales", "La Molina", 23, "Erika Guillen")

db.session.add_all([sanjuan, losportales])
db.session.commit()

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

db.session.add_all([usuario1, usuario2, usuario3, usuario4, usuario5, usuario6, 
usuario7, usuario8, usuario9, usuario10])
db.session.commit()

medico1 = PersonalMedico(71284499, "Santiago", "Gutierrez", "Doctor", "Neurólogía", "sgutierrez", "San Juan")
medico2 = PersonalMedico(84909223, "Fabricio", "Santos", "Doctor", "Cardiólogía", "fsantos", "San Juan")
medico3 = PersonalMedico(83919223, "Esteban", "Gambirazio", "Doctor", "Traumatólogía", "egambirazio", "Los Portales")
medico4 = PersonalMedico(72876544, "Romario", "Vega", "Doctor", "Neurólogía", "rvega", "Los Portales")
medico5 = PersonalMedico(62345678, "Luis", "Rodriguez", "Doctor", "Endocrinología", "lrodriguez", "Los Portales")
enfermera1 = PersonalMedico(10278990, "Fátima", "Novoa", "Enfermera", "Geriatría", "fnovoa", "San Juan")
enfermera2 = PersonalMedico(10278991, "Micaela", "Chavez", "Enfermera", "Geriatría", "mchavez", "San Juan")
enfermera3 = PersonalMedico(10278992, "Luciana", "Balta", "Enfermera", "Geriatría", "lbalta", "San Juan")
enfermera4 = PersonalMedico(10278993, "Haydi", "Durand", "Enfermera", "Geriatría", "hdurand", "Los Portales")
enfermera5 = PersonalMedico(10278994, "Daniela", "Tafur", "Enfermera", "Geriatría", "dtafur", "Los Portales")

db.session.add_all( [medico1, medico2, medico3, medico4, medico5, enfermera1, 
enfermera2, enfermera3, enfermera4, enfermera5])
db.session.commit()