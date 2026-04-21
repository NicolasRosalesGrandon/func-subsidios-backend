import azure.functions as func
import logging
import pyodbc
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="ProcesarSubsidio", methods=["POST"])
def ProcesarSubsidio(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Procesando solicitud de subsidio UTEM.')

    try:
        # 1. Obtener los datos del formulario web
        req_body = req.get_json()
        nombre = req_body.get('nombre')
        rut = req_body.get('rut')

        if not nombre or not rut:
            return func.HttpResponse("Faltan datos (nombre o rut)", status_code=400)

        # 2. Configuración de la Base de Datos (Ajusta con tus datos)
        # El server suele ser: nombre-servidor.database.windows.net
        server = 'TU_SERVIDOR_AQUI' 
        database = 'TU_DB_AQUI'
        username = 'TU_USUARIO'
        password = 'TU_PASSWORD'
        
        # Driver 18 es el estándar en Azure Linux/Windows
        conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

        # 3. Insertar datos en la tabla
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                # La tabla 'Postulaciones' debe tener columnas Nombre y RUT
                query = "INSERT INTO Postulaciones (Nombre, RUT) VALUES (?, ?)"
                cursor.execute(query, (nombre, rut))
                conn.commit()

        return func.HttpResponse(
            json.dumps({"mensaje": f"Postulación exitosa para {nombre}"}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(f"Error interno: {str(e)}", status_code=500)
