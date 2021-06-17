# DBP_PROYECTO

Nombre del Proyecto: Aplicación Web para el registro de ancianos con Covid en el albergue Gerovitalis

Integrantes:
- Francisco Magot
- Pedro Mori
- Sebastian Meza
- Luis David Torres
- Elizabeth Huamán

**Descripción del Proyecto:**
La pagina web sirve para para un geriatrioco en el cual se ecuentren pacientes covid. En la pagina es requerido tener un usuario para poder acceder a las funcionalidades de ver y registrar paciente.

**Misión:**
Queremos ser una pagina web utilizada por los geriatricos para poder tener un mejor control de los pacientes que se encuentran en la residencia.

**Visión:**
Ser la pagina web utilizada por diferentes geriatricos y clinicas para poder tener un registro de los pacientes, por parte de los doctores, pero tambien poder estar al tanto de los pacientes por parte de los familiares.

## **Tecnologías:**

- Front-End: Bootstrap, JavaScript

- Back-End: 
    - Framework:
    - Flask
    - Librerias:
        - Flask-Login
        - Flask-SQLAlchemy
        - Flask-Migrate

**Base de Datos:**
PostgreSQL

Script para iniciar la base de datos: El scripts para correr la base de datos es datos.py

- API's: API de RESTful

API's: API de RESTful

## **Forma de Auntenticación:**
El usuario necesita crear una cuenta para hacer uso de la funcionalidades. 
Usamos Flask-Login, para manejar las tareas de iniciar session, cerrar sesion y recordar las sesiones de los usuarios durante un periodo de tiempo.

Forma de Auntenticación:
El usuario necesita crear una cuenta para hacer uso de la funcionalidades. 
Usamos Flask-Login, para manejar las tareas de iniciar session, cerrar sesion y recordar las sesiones de los usuarios durante un periodo de tiempo

Manejo de Errores HTTP:
- 500
- 400
- 300
- 200
- 100

Deployment Scripts:
1. Correr el archivo app.py para crear las tablas en la base de datos
2. Correr el archivo datos.py para ingresar los elementos predeterminados a la base de datos
3. Correr el archivo app.py
