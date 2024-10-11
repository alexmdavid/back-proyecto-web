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
            user='root',  
            password=''   
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
        
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']
        # Hasheando la contraseña y guardando el usuario
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
       
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
                    session['username'] = username  # Aquí guardamos el nombre de usuario en la sesión
                    return redirect(url_for('perfil'))  # Redirigimos a la vista de perfil
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


@app.route('/perfil')
def perfil():
    if 'username' not in session:
        flash("Por favor, inicia sesión primero.")
        return redirect(url_for('login_usuario'))

    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT nombre, apellido, correo FROM usuarios WHERE nombre = %s", (session['username'],))
            usuario = cursor.fetchone()
            if usuario:
                return render_template('perfil.html', usuario=usuario)
            else:
                flash("Error al cargar el perfil.")
                return redirect(url_for('index'))
        except Error as e:
            flash(f"Error al cargar el perfil: {e}")
        finally:
            cursor.close()
            conexion.close()
    return redirect(url_for('index'))

#ruta para ver perfil
@app.route('/ver perfil')
def verPerfil():
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT nombre, apellido, correo FROM usuarios WHERE nombre = %s", (session['username'],))
            usuario = cursor.fetchone()
            if usuario:
                return render_template('verperfil.html', usuario=usuario)
            else:
                flash("Error al cargar el perfil.")
                return redirect(url_for('index'))
        except Error as e:
            flash(f"Error al cargar el perfil: {e}")
        finally:
            cursor.close()
            conexion.close()
    return redirect(url_for('index'))

@app.route('/usuarios')
def mostrar_usuarios():
    usuarios = []
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT idusuario, nombre, apellido, correo FROM usuarios")
        usuarios = cursor.fetchall()
        print(usuarios) 
    else:
        flash(f'error')
        
    # Imprime los datos para verificar

    return render_template('usuarios.html', usuarios=usuarios)

# Ruta para eliminar un usuario
@app.route('/eliminar_usuario/<int:idusuario>')
def eliminar_usuario(idusuario):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Eliminar el usuario de la base de datos
            cursor.execute("DELETE FROM usuarios WHERE idusuario = %s", (idusuario,))
            conexion.commit()
            flash("Usuario eliminado exitosamente.")
        except Error as e:
            flash(f"Error al eliminar usuario: {e}")
        finally:
            cursor.close()
            conexion.close()
    return redirect(url_for('mostrar_usuarios'))



@app.route('/editar_usuario/<int:idusuario>', methods=['GET', 'POST'])
def editar_usuario(idusuario):
    conexion = conectar_db()
    if request.method == 'POST':
        # Recibir los nuevos datos desde el formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']

        if conexion:
            cursor = conexion.cursor()
            try:
                # Actualizar los datos del usuario
                cursor.execute("""
                    UPDATE usuarios 
                    SET nombre = %s, apellido = %s, correo = %s 
                    WHERE idusuario = %s
                """, (nombre, apellido, email, idusuario))
                conexion.commit()
                flash("Usuario actualizado exitosamente.")
                return redirect(url_for('mostrar_usuarios'))
            except Error as e:
                flash(f"Error al actualizar usuario: {e}")
            finally:
                cursor.close()
                conexion.close()

    else:
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            try:
                # Obtener los datos del usuario
                cursor.execute("SELECT * FROM usuarios WHERE idusuario = %s", (idusuario,))
                usuario = cursor.fetchone()
                if usuario:
                    return render_template('editar.html', usuario=usuario)
                else:
                    flash("Usuario no encontrado.")
                    return redirect(url_for('mostrar_usuarios'))
            except Error as e:
                flash(f"Error al cargar datos del usuario: {e}")
            finally:
                cursor.close()
                conexion.close()
    return redirect(url_for('mostrar_usuarios'))





if __name__ == '__main__':
    app.run(debug=True)
