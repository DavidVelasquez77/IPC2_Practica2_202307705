from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "clave_secreta_para_sesiones"

# Datos de inicio de sesión del empleado
EMPLEADO_USUARIO = "empleado"
EMPLEADO_PASSWORD = "$uper4utos#"

# Almacenamiento en memoria de los autos
autos = []

# Página de inicio de sesión
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    usuario = request.form['usuario']
    password = request.form['password']
    if usuario == EMPLEADO_USUARIO and password == EMPLEADO_PASSWORD:
        session['empleado'] = usuario
        return redirect(url_for('home'))
    else:
        flash("Usuario o contraseña incorrectos", "error")
        return redirect(url_for('login'))

# Página de inicio después de iniciar sesión
@app.route('/home')
def home():
    if 'empleado' in session:
        return render_template('home.html', autos=autos)
    else:
        return redirect(url_for('login'))

# Página para agregar un nuevo auto
@app.route('/auto')
def auto():
    if 'empleado' in session:
        return render_template('auto.html')
    else:
        return redirect(url_for('login'))

# Registrar un auto
@app.route('/registrar_auto', methods=['POST'])
def registrar_auto():
    idTipoAuto = request.form['idTipoAuto']
    marca = request.form['marca']
    modelo = request.form['modelo']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    imagen = request.form['imagen']

    # Verificar si el auto ya existe por idTipoAuto
    for auto in autos:
        if auto['idTipoAuto'] == idTipoAuto:
            flash("El auto con ese ID ya existe", "error")
            return redirect(url_for('home'))

    # Crear el nuevo auto
    nuevo_auto = {
        'idTipoAuto': idTipoAuto,
        'marca': marca,
        'modelo': modelo,
        'descripcion': descripcion,
        'precio': precio,
        'cantidad': cantidad,
        'imagen': imagen
    }
    
    # Agregar el auto a la lista en memoria
    autos.append(nuevo_auto)
    flash("Auto registrado exitosamente", "success")
    return redirect(url_for('home'))

# Eliminar un auto por su ID
@app.route('/eliminar_auto/<int:idTipoAuto>')
def eliminar_auto(idTipoAuto):
    global autos
    autos = [auto for auto in autos if int(auto['idTipoAuto']) != idTipoAuto]
    flash("Auto eliminado correctamente", "success")
    return redirect(url_for('home'))

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('empleado', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
