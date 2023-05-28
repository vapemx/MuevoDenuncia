from datetime import datetime as dt
from flask import render_template
from flask import Flask, request
from hashlib import sha256
import requests
import pyodbc


def check_user(hash_clave):
    conn = None
    try:
        # Establecer la conexión con la base de datos
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MuevoDenuncia;UID=LSBDUSER;PWD=eliasv')

        # Crear un cursor para ejecutar la consulta
        cursor = conn.cursor()

        # Ejecutar el procedimiento almacenado para verificar el usuario
        cursor.execute("select hash_clave from addresses_validated where hash_clave = ?", (hash_clave,))

        # Obtener el resultado de la consulta
        row = cursor.fetchone()

        # Verificar si el usuario existe
        if row is not None:
            return True
        else:
            return False

    except pyodbc.Error as e:
        print("Error al verificar usuario", str(e))
        return False

    finally:
        # Cerrar la conexión con la base de datos
        if conn is not None:
            conn.close()


def check_address(address):
    conn = None
    try:
        # Establecer la conexión con la base de datos
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MuevoDenuncia;UID=LSBDUSER;PWD=eliasv')

        # Crear un cursor para ejecutar la consulta
        cursor = conn.cursor()

        # Ejecutar el procedimiento almacenado para verificar el usuario
        cursor.execute("select address from addresses_validated where address = ?", (address,))

        # Obtener el resultado de la consulta
        row = cursor.fetchone()

        # Verificar si el usuario existe
        if row is not None:
            return True
        else:
            return False

    except pyodbc.Error as e:
        print("Error al verificar usuario", str(e))
        return False

    finally:
        # Cerrar la conexión con la base de datos
        if conn is not None:
            conn.close()


def add_complaint_db(address, vehicle_reported, datetime, municipio, street, reference, complaint):
    # Obtener el hash de la queja
    hash = sha256(str(address + vehicle_reported + datetime + municipio + street + reference + complaint).encode()).hexdigest()

    conn = None
    try:
        # Establecer la conexión con la base de datos
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MuevoDenuncia;UID=LSBDUSER;PWD=eliasv')

        # Crear un cursor para ejecutar la consulta
        cursor = conn.cursor()

        # Ejecutar el procedimiento almacenado para verificar el usuario
        cursor.execute("insert into complaints (signers, vehicle_reported, incident_date, municipio, street, reference, complaint, resolved, complaint_hash) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", (address, vehicle_reported, datetime, municipio, street, reference, complaint, 0, hash,))
        conn.commit()
        return True

    except pyodbc.Error as e:
        print("Error al registrar queja", str(e))
        return False

    finally:
        # Cerrar la conexión con la base de datos
        if conn is not None:
            conn.close()


def new_user(hash_clave, address):
    conn = None
    try:
        # Establecer la conexión con la base de datos
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MuevoDenuncia;UID=LSBDUSER;PWD=eliasv')

        # Crear un cursor para ejecutar la consulta
        cursor = conn.cursor()

        # Ejecutar el procedimiento almacenado para verificar el usuario
        cursor.execute("insert into addresses_validated (hash_clave, address, is_valid) values (?, ?, ?)", (hash_clave, address,1,))
        conn.commit()
        return True

    except pyodbc.Error as e:
        print("Error al registrar usuario", str(e))
        return False

    finally:
        # Cerrar la conexión con la base de datos
        if conn is not None:
            conn.close()


app = Flask(__name__)

# Index y registro
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=['POST'])
def upload():
    # Obtener los datos del formulario de "address"
    address = request.form.get('address')

    # Obtener el archivo de imagen enviado
    image = request.files.get('image')
    image = image.filename

    # LLama la llave y el endpoint de Azure Computer Vision
    subscription_key = '5af781ed31e04435a0d6fe205eaffa1d'
    endpoint = 'https://testocrhackathon.cognitiveservices.azure.com/'

    # URL de la API de Computer Vision
    api_url = endpoint + '/vision/v3.2/ocr'

    # Ruta de la imagen local
    image_path = image

    # Parámetros de la solicitud
    params = {'language': 'es', 'detectOrientation': 'true'}

    # Headers de la peticion
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}

    # Leer la imagen en forma de bytes
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Realizar la solicitud POST a la API
    response = requests.post(api_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # Obtener el resultado como JSON
    result = response.json()

    # Extraer el texto de las regiones y líneas
    extracted_text = ''
    for region in result['regions']:
        for line in region['lines']:
            for word in line['words']:
                extracted_text += word['text'] + ' '

    # Buscar la clave de elector
    words = extracted_text.split()
    if 'CLAVEDEELECTOR' in words:
        index = words.index('CLAVEDEELECTOR')
        clave = words[index + 1]
        print("Clave de elector encontrada:", clave)

        hash = sha256(str(clave).encode()).hexdigest()
        
        print(address)
        if check_user(hash) == True:
            return 'Usuario ya creado, si desea hacer una denuncia, use su address'
        else:
            if new_user(hash, address) == True:
                return 'Usuario creado correctamente'
            else:
                return 'Error al crear usuario'

    else:
        print("Hubo un error al escanear la imagen. Escanea la imagen nuevamente.")
    return 'Datos recibidos: address={}, imagen={}'.format(address, image.filename)


# Denuncia page
@app.route('/complaint')
def complaint():
    return render_template('complaint.html')


# Mis denuncias
@app.route('/my_complaints')
def my_complaints():
    return render_template('tabla.php')


# Make complaint
@app.route('/make_complaint', methods=['POST'])
def make_complaint():
    # Leer: address, vehicle_reported, datetime, municipio, street, reference, complaint 
    address = request.form.get('address')
    vehicle_reported = request.form.get('vehicle_reported')
    selected_date = request.form.get('date')
    selected_time = request.form.get('time')
    selected_datetime_str = f"{selected_date} {selected_time}"
    selected_datetime_obj = dt.strptime(selected_datetime_str, "%Y-%m-%d %H:%M")
    datetime = str(selected_datetime_obj)
    municipios = {
    'municipio1': 'Apodaca',
    'municipio2': 'Escobedo',
    'municipio3': 'Garcia',
    'municipio4': 'Juárez',
    'municipio5': 'Monterrey',
    'municipio6': 'San Nicolas',
    'municipio7': 'San Pedro',
    'municipio8': 'Santa Catarina'
    }   
    selected_option = request.form.get('list')

    if selected_option:
        if selected_option in municipios:
            municipio = municipios[selected_option]
        
    street = request.form.get('street')
    reference = request.form.get('reference')
    complaint = request.form.get('complaint')

    if check_address(address) == True:
        if add_complaint_db(address, vehicle_reported, datetime, municipio, street, reference, complaint) == True:
            return 'Denuncia realizada correctamente'
        else:
            return 'Error al realizar denuncia'
    else:
        return index()


if __name__ == '__main__':
    app.run(debug=True, port=5000)