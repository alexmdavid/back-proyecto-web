from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.model import Usuario
import mysql.connector
from mysql.connector import Error
import hashlib



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar 'flash' en mensajes

# Conectar con la base de datos
def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='user_auth',
            user='root',  # Cambiar si tienes un usuario diferente
            password=''   # Agrega la contraseña de tu base de datos
        )
        if conexion.is_connected():
            print("Conectado a MySQL")
        return conexion
    except Error as e:
        print(f"Error conectando a MySQL: {e}")
        return None

# Ruta para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

#ruta para registrar usuario
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Lógica para manejar el registro
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']
        # Hasheando la contraseña y guardando el usuario
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Aquí puedes usar el modelo Usuario
        usuario = Usuario.from_registro(nombre, apellido, email, hashed_password)
        
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            try:
                # Verificar si el usuario ya existe
                cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (email,))
                result = cursor.fetchone()
                if result:
                    flash("El usuario ya existe.")
                else:
                    # Insertar nuevo usuario
                    cursor.execute("INSERT INTO usuarios (nombre, apellido, correo, contrasena) VALUES (%s, %s, %s, %s)", 
                                   (usuario.nombre, usuario.apellido, usuario.correo, usuario.contrasena))
                    conexion.commit()
                    flash("Usuario registrado exitosamente.")
                    return redirect(url_for('login_usuario'))
            except Error as e:
                flash(f"Error al registrar usuario: {e}")
            finally:
                cursor.close()
                conexion.close()
    return render_template('registro.html')


    



# Ruta para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login_usuario():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            try:
                # Verificar credenciales
                cursor.execute("SELECT * FROM usuarios WHERE nombre = %s AND contrasena = %s", (username, hashed_password))
                result = cursor.fetchone()
                if result:
                    flash("Login exitoso. ¡Bienvenido!")
                    return redirect(url_for('index'))
                else:
                    flash("Usuario o contraseña incorrectos.")
            except Error as e:
                flash(f"Error al iniciar sesión: {e}")
            finally:
                cursor.close()
                conexion.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Has cerrado sesión.")
    return redirect(url_for('login_usuario'))


if __name__ == '__main__':
    app.run(debug=True)
