from flask import Flask, render_template, request, redirect, url_for, session, flash

class Auto:
    autos = []

    def __init__(self, idTipoAuto, marca, modelo, descripcion, precio, cantidad, imagen):
        self.idTipoAuto = idTipoAuto
        self.marca = marca
        self.modelo = modelo
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad = cantidad
        self.imagen = imagen

    @classmethod
    def registrar_auto(cls, idTipoAuto, marca, modelo, descripcion, precio, cantidad, imagen):
        for auto in cls.autos:
            if auto.idTipoAuto == idTipoAuto:
                return False
        nuevo_auto = cls(idTipoAuto, marca, modelo, descripcion, precio, cantidad, imagen)
        cls.autos.append(nuevo_auto)
        return True

    @classmethod
    def eliminar_auto(cls, idTipoAuto):
        cls.autos = [auto for auto in cls.autos if int(auto.idTipoAuto) != idTipoAuto]

    @classmethod
    def obtener_autos(cls):
        return cls.autos

class Empleado:
    USUARIO = "empleado"
    PASSWORD = "$uper4utos#"

    @staticmethod
    def autenticar(usuario, password):
        return usuario == Empleado.USUARIO and password == Empleado.PASSWORD

app = Flask(__name__)
app.secret_key = "clave_secreta_para_sesiones"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    usuario = request.form['usuario']
    password = request.form['password']
    if Empleado.autenticar(usuario, password):
        session['empleado'] = usuario
        return redirect(url_for('home'))
    else:
        flash("Usuario o contraseña incorrectos", "error")
        return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'empleado' in session:
        return render_template('home.html', autos=Auto.obtener_autos())
    else:
        return redirect(url_for('login'))

@app.route('/auto')
def auto():
    if 'empleado' in session:
        return render_template('auto.html')
    else:
        return redirect(url_for('login'))

@app.route('/registrar_auto', methods=['POST'])
def registrar_auto():
    idTipoAuto = request.form['idTipoAuto']
    marca = request.form['marca']
    modelo = request.form['modelo']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    imagen = request.form['imagen']

    if not Auto.registrar_auto(idTipoAuto, marca, modelo, descripcion, precio, cantidad, imagen):
        flash("El auto con ese ID ya existe", "error")
        return redirect(url_for('home'))
    
    flash("Auto registrado exitosamente", "success")
    return redirect(url_for('home'))

@app.route('/eliminar_auto/<int:idTipoAuto>')
def eliminar_auto(idTipoAuto):
    Auto.eliminar_auto(idTipoAuto)
    flash("Auto eliminado correctamente", "success")
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('empleado', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
