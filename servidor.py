from flask import Flask, render_template, request, redirect, session, jsonify, flash
from config import *
from datetime import datetime
import re
from flask_sqlalchemy import SQLAlchemy

today = datetime.now()
año = today.year
mes = today.month
dia = today.day
fecha = f'{año}-{mes}-{dia}'

db = SQLAlchemy()

app = Flask('Administrado de ventas')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{ruta}/database.db'
app.secret_key = secret_key

db.init_app(app)


class Proyeccion:
    def __init__(self, producto, cantidad, porciones, ganancias, inversion, porcentaje, datos, inventario):
        self.producto = producto
        self.cantidad = cantidad
        self.porciones = porciones
        self.ganancias = ganancias
        self.inversion = inversion
        self.porcentaje = porcentaje
        self.datos = datos
        self.inventario = inventario

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String, nullable=False)
    nombre = db.Column(db.String, nullable = False)
    sexo = db.Column(db.String, nullable=False)
    clave = db.Column(db.String, nullable=False)
    ventas = db.Column(db.Integer, nullable=False)
    cargo = db.Column(db.String, nullable=False)

class Ventas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String, nullable=False)
    venta = db.Column(db.Float, nullable=False)

class Registro_dia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String,unique=True, nullable=False)
    venta = db.Column(db.Float, nullable=False)
    gasto = db.Column(db.Float, nullable=False)

class Gastos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String, nullable=False)
    gasto = db.Column(db.Float, nullable=False)
    motivo = db.Column(db.String, nullable=False)

class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    costo = db.Column(db.Float, nullable=False)
    vendidos = db.Column(db.Integer, nullable=False)

class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto = db.Column(db.String, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    costo = db.Column(db.Float, nullable=False)

class Pedidos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compra = db.Column(db.String, nullable=False)
    detalle = db.Column(db.String, nullable=False)
    costo = db.Column(db.Float, nullable=False)
    llevar = db.Column(db.String, nullable=False)
    cliente = db.Column(db.String, nullable=False)

class PagosElectronicos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    plataforma = db.Column(db.String, nullable=False)


def obtener_fecha():
    today = datetime.now()
    año = today.year
    mes = today.month
    dia = today.day
    fe = f'{año}/{mes}/{dia}'
    return fe

def obtener_mes():
    today = datetime.now()
    año = today.year
    mes = today.month
    fe = f'{año}/{mes}'
    return fe

    

@app.route('/')
def index():
    try:
        nuevo = Registro_dia(fecha=obtener_fecha(), venta=0.0, gasto=0.0)
        db.session.add(nuevo)
        db.session.commit()
    except:
        pass
    if 'id_user' in session:
        return redirect('/home')
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.session.query(Usuario).filter_by(usuario=request.form['username'], clave=request.form['password']).first()
        try:
            session['id_user'] = user.id
            return redirect('/home')
        except:
            flash('Usuario no existe')
            return redirect('/')
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST':
        user = request.form['username']
        clave = request.form['password']
        name = request.form['name']
        sexo = request.form['sexo']
        if sexo not in ['masculino', 'Masculino', 'MASCULINO', 'femenino', 'Femenino', 'FEMENINO']:
            return redirect('/signup')
        nuevo_usuario = Usuario(usuario=user, nombre=name, sexo=sexo, clave=clave, ventas=0, cargo='Empleado')
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Registro exitoso')
            return redirect('/home')
        except:
            flash('Error a la hora de registrar')
            return redirect('/')
        
    elif request.method == 'GET':
        if 'id_user' in session:
            lista_productos = db.session.query(Productos).all()
        return render_template('signup.html', lista_productos = lista_productos)

@app.route('/inventario', methods=['POST'])
def inventario():
    if request.method == 'POST':
        producto = request.form['producto']
        unidades = int(request.form['unidades_compra'])
        inventario = db.session.query(Inventario).filter_by(nombre=producto).first()
        if inventario == None:
            nuevo_inventario = Inventario(nombre=producto, cantidad = unidades)
            db.session.add(nuevo_inventario)
            flash("Registro nuevo exitoso")
        else:
            inventario.cantidad = inventario.cantidad + unidades
            flash("Registro actualizado")
        db.session.commit()
    
    return redirect('/signup')

@app.route('/pedidos')
def pedidos():
    #try:
        usuario = db.session.query(Usuario).get(session['id_user'])
        pedidos = Pedidos.query.order_by(Pedidos.id.asc()).all()
        venta_hoy_list = db.session.query(Ventas).filter_by(fecha=obtener_fecha()).all()
        venta_hoy = 0
        if venta_hoy_list != None:
            for i in venta_hoy_list:
                venta_hoy += i.venta
        return render_template('pedidos.html', usuariodata = usuario, fecha = obtener_fecha(), ventas_hoy = venta_hoy, pedidos = pedidos)
    #except:
    #    flash('No se registran pedidos')
    #    return redirect('/')

@app.route('/agregar_carrito', methods=['POST'])
def agregar_carrito():
    if request.method == 'POST':
        producto = request.form['producto']
        unidades = int(request.form['unidades'])
        
        try:
            costo = db.session.query(Productos).filter_by(nombre=producto).first()
            monto = costo.precio * unidades
            db.session.commit()
            
            try:
                actualizar = db.session.query(Carrito).filter_by(producto=producto).first()
                actualizar.costo = monto + actualizar.costo
                actualizar.cantidad = unidades + actualizar.cantidad
            except:
                nuevo_producto = Carrito(producto=producto, cantidad=unidades, costo = monto)
                db.session.add(nuevo_producto)

            try:
                inventario = db.session.query(Inventario).filter_by(nombre=producto).first()
                inventario.cantidad = inventario.cantidad - unidades
                db.session.commit()
            except:
                pass
            costo.vendidos = costo.vendidos + unidades
            db.session.commit()
        except:
            flash('Error al agregar producto')
    return redirect('/')
    



@app.route('/home' )
def inicio():
    usuario = db.session.query(Usuario).get(session['id_user'])
    carrito = db.session.query(Carrito).all()
    print(usuario.nombre)
    total = 0
    for i in carrito:
        total += i.costo
    venta_hoy = 0
    ventas = db.session.query(Ventas).filter_by(fecha=obtener_fecha()).all()
    if ventas != None:
        for i in ventas:
            venta_hoy += i.venta
    lista_productos = db.session.query(Productos).all()
    return render_template('inicio.html', usuariodata = usuario, fecha = obtener_fecha(), productos = carrito, pagar = total, ventas_hoy = venta_hoy, lista_productos = lista_productos)

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('id_user')
    return redirect('/')

@app.route('/estadisticas')
def estadisticas():
    registros = Ventas.query.order_by(Ventas.venta.desc()).all()
    total_mes =0
    for i in registros:
        if obtener_mes() in i.fecha:
            total_mes += i.venta
        else:
            break
    dia_mayor =Ventas.query.order_by(Ventas.venta.desc()).first()
    dia_menor = Ventas.query.order_by(Ventas.venta.asc()).first()
    producto_menos = Productos.query.order_by(Productos.vendidos.asc()).first()
    producto_mas = Productos.query.order_by(Productos.vendidos.desc()).first()
    trabajadores = Usuario.query.order_by(Usuario.nombre.asc()).all()
    lista_inventario = Inventario.query.order_by(Inventario.cantidad.asc()).all()
    ventas = db.session.query(Ventas).filter_by(fecha=obtener_fecha()).all()
    venta = 0
    if ventas == None:
        dia_mayor = Ventas(fecha='No hay fecha', venta=0)
        dia_menor = Ventas(fecha='No hay fecha', venta=0)
    else:
        for i in ventas:
            venta += i.venta
        dia_mayor = dia_mayor
        dia_menor = dia_menor
    gastos = db.session.query(Gastos).filter_by(fecha=obtener_fecha()).all()
    gasto = 0
    if gastos == None:
        gasto = 0
    else:
        for i in gastos:
            gasto += i.gasto

    return render_template('estadisticas.html', informe = total_mes, diaMas = dia_mayor, diaMenos = dia_menor, producto_menos = producto_menos, producto_mas = producto_mas, trabajadores = trabajadores, inventario_final = lista_inventario, venta_hoy = venta, gasto = gasto)

@app.route('/listo_o_cancelar', methods=['POST'])
def listo():
    pedido = db.session.query(Pedidos).get(request.form['id'])
    if request.method == 'POST':
        if 'listo' in request.form:
            nueva_venta = Ventas(fecha=obtener_fecha(), venta=pedido.costo)
            actualizar = db.session.query(Registro_dia).filter_by(fecha=obtener_fecha()).first()
            actualizar.venta = actualizar.venta + pedido.costo
            db.session.add(nueva_venta)
            db.session.query(Pedidos).filter_by(id=pedido.id).delete()
            db.session.commit()
            return redirect('/pedidos')
        elif 'cancelar' in request.form:
            db.session.query(Ventas).filter(fecha=obtener_fecha(), venta=pedido.costo).delete()
            db.session.commit()
            return redirect('/pedidos')

    else:
        return redirect('/')

@app.route('/pagar', methods=['POST', 'GET'])
def pagar():

    if request.method == 'POST':
        cliente = request.form['cliente']
        total_pagar = 0
        llevar = request.form['llevar']
        detalles = request.form['detalles']
        compra = ""
        carrito = db.session.query(Carrito).all()
        for i in carrito:
            if i.cantidad != 1:
                compra = compra + i.producto + ' X' + str(i.cantidad) + ','
            else:
                compra = compra + i.producto + ','
            total_pagar += i.costo
        try:
            nuevo_pedido = Pedidos(compra=compra, detalle = detalles, costo = total_pagar, llevar=llevar, cliente=cliente)
            db.session.add(nuevo_pedido)
            db.session.query(Carrito).delete()
            db.session.commit()
        except:
            flash('Nada')
        return redirect('/')

    else:
        return redirect('/')


@app.route('/reiniciar_carrito')
def reiniciar():
    db.session.query(Carrito).delete()
    db.session.commit()
    return redirect('/')

@app.route('/gasto', methods=['POST'])
def gastos():
    if request.method == 'POST':
        motivo = request.form['motivo_gasto']
        valor_inicial = request.form['valor_gasto']
        try:
            valor_inicial = float(valor_inicial)/1000
            nuevo_gasto = Gastos(fecha=obtener_fecha(), gasto=valor_inicial, motivo=motivo)
            print(obtener_fecha())
            db.session.add(nuevo_gasto)
            actualizar = db.session.query(Registro_dia).filter_by(fecha=obtener_fecha()).first()
            actualizar.gasto = actualizar.gasto + valor_inicial
            db.session.commit()
        except:
            print("Valor no válido, por favor ingrese los numeros sin puntos ni comas")
            flash("Valor no válido, por favor ingrese los numeros sin puntos ni comas")
        return redirect('/signup')

@app.route('/detalles_gastos', methods=['POST'])
def detalles():
    if request.method == 'POST':
        data = request.form['fecha']
        fecha_dt = datetime.strptime(data, "%Y-%m-%d")
        fecha_formateada = fecha_dt.strftime("%Y/%m/%d")
        fecha_formateada = re.sub(r"(?<=/)(0+)", "", fecha_formateada)
        print(fecha_formateada)
        try:
            gastos = db.session.query(Gastos).filter_by(fecha=fecha_formateada).all()
            print(gastos)
            if gastos != []:
                return render_template('detalles.html', gastos = gastos, usuariodata = db.session.query(Usuario).get(session['id_user']))
            else:
                flash('No hay registros de esta fecha')
                return redirect('/consulta')
        except:
            return redirect('/consulta')
    return redirect('/')

@app.route('/consulta', methods = ['POST', 'GET'])
def consulta():
    usuario = db.session.query(Usuario).get(session['id_user'])
    productos = db.session.query(Productos).all()
    if request.method == 'POST':
        try:
            producto = request.form['producto']
            datos = db.session.query(Productos).filter_by(nombre=producto).first()
            cantidad = float(request.form['cantidad'])
            porciones = int(request.form['porciones'])
            ganancias = cantidad*porciones*datos.precio
            inversion = cantidad*porciones*datos.costo
            inventario = db.session.query(Inventario).filter_by(nombre=producto).first()
            if inventario != None:
                inventario = inventario.cantidad
            else:
                inventario = 0
            ventas = db.session.query(Ventas).all()
            venta = 0
            if ventas != None:
                for i in ventas:
                    venta += i.venta
            porcentaje_ventas = round((datos.precio*datos.vendidos/venta)*100, 2)
            miproyeccion = Proyeccion(producto, cantidad, porciones, ganancias, inversion, porcentaje_ventas, datos, inventario)
            print('siiiiiiiiiiiiiiiu')
            return render_template('detalles_proyeccion.html', usuariodata=usuario, proyeccion = miproyeccion)
        except:
            flash('Error al proyectar')
            pass
    ventas_db = Registro_dia.query.order_by(Registro_dia.id.asc()).all()
    return render_template('consulta.html', usuariodata=db.session.query(Usuario).get(session['id_user']), productos = productos, registros = ventas_db)


@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        costo = request.form['costo']

        try:
            precio = float(precio)/1000
            costo = float(costo)/1000
            nuevo_producto = Productos(nombre=nombre, precio=precio, costo=costo, vendidos=0)
            db.session.add(nuevo_producto)
            db.session.commit()
        except:
            flash('Error a la hora del registro.')
        return redirect('/signup')
# ESTOY TRABAJANDO AQUÍ        


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)