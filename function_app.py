import azure.functions as func
import logging
import pyodbc
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="ProcesarSubsidio")
def ProcesarSubsidio(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == 'GET':
        return func.HttpResponse(
            "Backend UTEM Activo. Esperando datos por POST.",
            status_code=200
        )

    try:
        req_body = req.get_json()
        nombre = req_body.get('nombre')
        rut = req_body.get('rut')

        if not nombre or not rut:
            return func.HttpResponse("Error: Faltan datos", status_code=400)

        server = 'server-subsidios.database.windows.net' 
        database = 'db-subsidios' 
        username = 'nicolas_admin'
        password = 'NicoDiegoAngelo2026'
        
        conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                query = "INSERT INTO Postulaciones (Nombre, RUT) VALUES (?, ?)"
                cursor.execute(query, (nombre, rut))
                conn.commit()

        return func.HttpResponse(
            json.dumps({"status": "exito", "mensaje": f"Registrado: {nombre}"}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
