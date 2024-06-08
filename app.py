from flask import Flask, render_template,request,redirect,flash, session,url_for,make_response
#from flaskext.mysql import MySQL
from datetime import datetime , date
from flask import jsonify
import json
from functools import wraps 
from flask_mysqldb import MySQL
import MySQLdb



app = Flask(__name__)
app.secret_key="DiegoJerez"


# CONEXION A LA BASE DE DATOS ----------------------------
#mysql = MySQL()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'internaciones'

mysql = MySQL(app)
#mysql.init_app(app)


 

@app.route('/')
def home():
    sql = "SELECT afiliado.id,afiliado.dni, afiliado.nombre, afiliado.apellido,afiliado.edad, afiliado.sexo, afiliado.fuerza,afiliado.estado,afiliado.observaciones FROM `afiliado`;"
    
    conn = mysql.connection
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        afiliado = cursor.fetchall()
        
    finally:
        cursor.close()  # Cierra el cursor
        # conn.close()    # No necesitas cerrar la conexión aquí, Flask-MySQLdb gestiona esto.
    return render_template('index.html', afiliado=afiliado)
    



@app.route('/ingresoafiliado', methods=['POST'])
def ingresoafiliado():
    
    _dni=request.form['txtDni']

    _nombre=request.form['txtNombre']
    _apellido=request.form['txtApellido']
    _edad=request.form['txtEdad']
    opciones_seleccionadas1= request.form.getlist('Sexo')
    opciones_fuerza=request.form.getlist('Fuerza')
    estado = request.form.get('flexRadioDefault')
    observaciones = request.form['observacionesA']

    

    
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT dni FROM afiliado WHERE dni=%s", (_dni,))
    dni = cursor.fetchone()
    #print(dni)

    if dni:
        flash('El DNI YA EXISTE','error')
        return redirect('/')



    if _nombre=='' or _dni=='' or _apellido=='' or _edad=='' or opciones_fuerza=='':
        flash('Todos los campos deben estar completos','error')
        return redirect('/')


   
    for Sexo in opciones_seleccionadas1:
        opcion1 = Sexo
    


    for Fuerza in opciones_fuerza:
        opcion2 = Fuerza
    
    #print(opcion2)
    #print(f'Estado: {estado}')
    
    sql = "INSERT INTO `afiliado` (`dni`, `nombre`, `apellido`, `edad`, `sexo`,`fuerza`,`estado`,`observaciones`) VALUES ( %s, %s, %s, %s,%s,%s,%s,%s);"

    datos=(_dni,_nombre,_apellido,_edad,opcion1,opcion2,estado,observaciones)
    conn = mysql.connection
    cursor = conn.cursor()

    try:
        cursor.execute(sql, datos)
        conn.commit()
        flash('Afiliado Agregado', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al agregar el afiliado: {str(e)}', 'error')
    finally:
        cursor.close()

    return redirect('/')
    
    
    

@app.route('/editarafiliado/<int:id>', methods=['GET'])
def editarafiliado(id):
    conn = mysql.connection
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM afiliado WHERE id=%s", (id,))
        afiliado = cursor.fetchone()
        if not afiliado:
            return jsonify({"error": "Afiliado no encontrado"}), 404
        return jsonify(afiliado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


@app.route('/actualizarafiliado', methods=['POST'])
def actualizarAafiliado():

    _dni=request.form['dni']
    _nombre=request.form['nombre']
    _apellido=request.form['apellido']
    _edad=request.form['edad']
    opciones_seleccionadas1= request.form.getlist('sexo')
    
    _id=request.form['id']
    opciones_fuerza=request.form.getlist('Fuerza')
    estado = request.form.get('flexRadioDefault')
    observaciones = request.form['observacionesA']

    #print(_id)

    if _nombre=='' or _dni=='' or _apellido=='' or _edad=='' :
        flash('Todos los campos deben estar completos','error')
        return redirect('/')
        
   
    for Sexo in opciones_seleccionadas1:
        opcion1 = Sexo

    
    for Fuerza in opciones_fuerza:
        opcion2 = Fuerza

    sql = "UPDATE afiliado SET dni =%s, nombre=%s, apellido=%s, edad=%s ,sexo=%s, fuerza=%s,estado=%s,observaciones=%s WHERE id=%s ;"

    datos=(_dni,_nombre,_apellido,_edad,opcion1,opcion2,estado,observaciones,_id)

    conn = mysql.connection
    cursor = conn.cursor()

    try:
        cursor.execute(sql, datos)
        conn.commit()
        flash('Afiliado Modificado', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al modificar el afiliado: {str(e)}', 'error')
    finally:
        cursor.close()

    
    return redirect(url_for('home'))

    #return redirect('/')

@app.route('/ingresointernacion', methods=['POST'])
def ingresointernacion():
    id=request.form['idInter']
    #_prestador=request.form['prestador']
    _opciones_prestador= request.form.getlist('prestador')
    _fechaingreso=request.form['fechaingreso']
    _fechasalida=request.form['fechasalida']
    _totaldias=request.form['totaldias']
    _medico=request.form['medico']
    _diagnostico= request.form['diagnostico']
    _observaciones = request.form['observaciones']

    for prestador in _opciones_prestador:
        _prestador = prestador

    # Convierte la fecha del formulario a un objeto datetime.date
    _fechaingreso = datetime.strptime(_fechaingreso, '%Y-%m-%d').date()
    
   
    

    # Conexión a la base de datos
    conn = mysql.connection
    cursor = conn.cursor()
    
    # Consulta para obtener las fechas de ingreso y salida existentes
    cursor.execute("""
        SELECT fechaingreso, fechasalida 
        FROM internacion 
        WHERE idafiliado=%s
    """, (id,))
    
    fechas = cursor.fetchall()
    
    # Verifica si la nueva fecha está en conflicto con alguna internación existente
    for fecha in fechas:
        fechaingreso_existente, fechasalida_existente = fecha
        if (_fechaingreso <= fechasalida_existente) and (_fechaingreso >= fechaingreso_existente):
            flash('Ya existe una internación en el rango de fechas ingresadas.', 'error')
            return redirect('/')


    
    if _prestador=='' or _fechaingreso=='' or _fechasalida=='' or _totaldias=='' or _diagnostico=='':
        flash('Todos los campos deben estar completos','error')
        return redirect('/')
       
    sql = "INSERT INTO `internacion` (`idafiliado`, `prestador`, `fechaingreso`, `fechasalida`, `diagnostico`,`totaldias`,`medico`,`observaciones`) VALUES (%s, %s, %s, %s,%s,%s,%s,%s);"

    datos=(id,_prestador,_fechaingreso,_fechasalida,_diagnostico,_totaldias,_medico,_observaciones)
    
    
    conn = mysql.connection
    cursor = conn.cursor()

    try:
        cursor.execute(sql, datos)
        conn.commit()
        flash('Internacion Agregada', 'success')
        actualizar_estado_afiliado(id)
    except Exception as e:
        conn.rollback()
        flash(f'Error al agregar la internacion: {str(e)}', 'error')
    finally:
        cursor.close()
    
    return redirect('/')



def actualizar_estado_afiliado(id):
    # Actualizar el campo deseado en la tabla afiliado
    # Aquí debes ajustar el campo y el valor que quieres actualizar

    # Conexión a la base de datos
    print(id)
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("UPDATE afiliado SET estado = 'CARGADO' WHERE id = %s", (id,))
    conn.commit()
    cursor.close()



@app.route('/mostrar/<int:id>')
def mostrar(id):
    sql_internacion = "SELECT * FROM internacion WHERE idafiliado=%s"
    sql_afiliado = "SELECT * FROM afiliado WHERE id=%s"
    conn = mysql.connection
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    try:
        cursor.execute(sql_internacion, (id,))
        internacion = cursor.fetchall()

        #print("Datos de internacion obtenidos:", internacion)

        # Formatear la fecha
        for a in internacion:
            #print("Tipo de fechaingreso antes de formatear:", type(a['fechaingreso']), a['fechaingreso'])  # Debug: Ver tipo de dato
            if isinstance(a['fechaingreso'], date):
                a['fechaingreso'] = a['fechaingreso'].strftime(" %d /%m/ %Y")
            
            if isinstance(a['fechasalida'], date):
                a['fechasalida'] = a['fechasalida'].strftime(" %d /%m/ %Y")
            
            

        cursor.execute(sql_afiliado, (id,))
        afiliado = cursor.fetchall()

        if not internacion:
            flash('El afiliado NO tiene internaciones cargadas', 'error')
            return redirect('/')

    except Exception as e:
        flash(f'Error al consultar la base de datos: {str(e)}', 'error')
        return redirect('/')
    finally:
        cursor.close()
        #conn.close()

    #print("datos enviados:" ,internacion,afiliado)
    return render_template('internaciones.html', internacion=internacion, afiliado=afiliado)

@app.route('/editarinternacion/<int:id>', methods=['GET'])
def editarinternacion(id):
    conn = mysql.connection
    cursor = conn.cursor()
    #print("El ID de la internación es: " + str(id))  # Convierte el ID a una cadena
    try:
        cursor.execute("SELECT * FROM internacion WHERE idinternacion=%s", (id,))
        internacion = cursor.fetchone()
        
        if internacion is None:
            flash('No se encontró la internación con el ID proporcionado', 'error')
            return redirect('/')

    except Exception as e:
        flash(f'Error al consultar la base de datos: {str(e)}', 'error')
        return redirect('/')
    finally:
        cursor.close()
        #conn.close()
    
    return jsonify(internacion)

@app.route('/actualizarinternacion', methods=['POST'])
def actualizarinternacion():
    id = request.form['idInter']
    #_prestador = request.form['prestador']
    _opciones_prestador= request.form.getlist('prestador')
    _fechaingreso = request.form['fechaingreso']
    _fechasalida = request.form['fechasalida']
    _totaldias = request.form['totaldias']
    _medico = request.form['medico']
    _diagnostico = request.form['diagnostico']
    _observaciones = request.form['observaciones']

    for prestador in _opciones_prestador:
        _prestador = prestador

    
    if not all([_prestador, _fechaingreso, _fechasalida, _totaldias, _diagnostico]):
        flash('Todos los campos deben estar completos', 'error')
        return redirect('/')
      
    sql = "UPDATE internacion SET prestador=%s, fechaingreso=%s, fechasalida=%s, diagnostico=%s, totaldias=%s, medico=%s,observaciones=%s WHERE idinternacion=%s;"
    datos = (_prestador, _fechaingreso, _fechasalida, _diagnostico, _totaldias, _medico,_observaciones, id)
    
    conn = mysql.connection
    cursor = conn.cursor()
    
    try:
        # Primero obtenemos el id del afiliado usando el id de internacion
        cursor.execute("SELECT idafiliado FROM internacion WHERE idinternacion=%s", (id,))
        id_afiliado = cursor.fetchone()[0]

        cursor.execute(sql, datos)
        conn.commit()
        flash('Internacion Modificada', 'success') 
        # Redirigir a la vista 'mostrar' usando el id del afiliado
        return redirect(url_for('mostrar', id=id_afiliado))
    except Exception as e:
        flash(f'Error al modificar la internacion: {str(e)}', 'error')
        return redirect('/')



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)