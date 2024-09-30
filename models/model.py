class Usuario:
    # Constructor completo con todos los atributos
    def __init__(self, nombre, apellido, tipo_sangre=None, correo=None, contrasena=None, sexo=None, fecha_nacimiento=None):
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_de_sangre = tipo_sangre
        self.correo = correo
        self.contrasena = contrasena
        self.sexo = sexo
        self.fecha_de_nacimiento = fecha_nacimiento

    # Constructor para registrar solo con nombre, apellido, correo y contraseña
    @classmethod
    def from_registro(cls, nombre, apellido, correo, contrasena):
        return cls(nombre=nombre, apellido=apellido, correo=correo, contrasena=contrasena)

    # Constructor que recibe solo nombre y apellido, útil si quieres ir agregando datos luego
    @classmethod
    def from_basico(cls, nombre, apellido):
        return cls(nombre=nombre, apellido=apellido)

    # Método para mostrar los datos del usuario (puedes personalizarlo según tus necesidades)
    def __str__(self):
        return f"Nombre: {self.nombre} {self.apellido}, Correo: {self.correo}, Sexo: {self.sexo}, Fecha de Nacimiento: {self.fecha_de_nacimiento}, Tipo de Sangre: {self.tipo_de_sangre}"
