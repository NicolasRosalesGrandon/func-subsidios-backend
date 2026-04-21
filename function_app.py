import azure.functions as func
import logging
import pyodbc
import os
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Configuración de la conexión a Azure SQL (Serverless)
# Estos datos se extraen de las variables de entorno configuradas en el portal
connection_string = os.environ.get('SQL_CONNECTION_STRING')

@app.route(route="ProcesarSubsidio")
def ProcesarSubsidio(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Procesando solicitud de postulación a subsidio.')

    try:
        # 1. Obtener datos del cuerpo de la solicitud (JSON del Frontend)
        req_body = req.get_json()
        rut = req_body.get('rut')
        nombre = req_body.get('nombre')

        if not rut or not nombre:
            return func.HttpResponse(
                "Error: RUT y Nombre son obligatorios.",
                status_code=400
            )

        # 2. Conectar a la base de datos y ejecutar el INSERT
        # Se utilizan los nombres de columna actualizados en SSMS
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO Postulaciones (RutCiudadano, NombreCompleto, FechaPostulacion)
                    VALUES (?, ?, GETDATE())
                """
                cursor.execute(query, (rut, nombre))
                conn.commit()

        # 3. Respuesta exitosa
        return func.HttpResponse(
            json.dumps({
                "mensaje": "Postulacion recibida exitosamente",
                "estado": "Procesado por demanda (Serverless)"
            }),
            mimetype="application/json",
            status_code=201
        )

    except Exception as e:
        logging.error(f"Error en el procesamiento: {str(e)}")
        return func.HttpResponse(
            f"Error interno en el servidor backend: {str(e)}",
            status_code=500
        )
