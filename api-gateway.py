from flask import Flask, Response, jsonify, request
import requests, os
from flasgger import Swagger, swag_from
from swagger.config import swagger_config

RAPPORT_SERVICE_URL = os.getenv('RAPPORT_SERVICE_URL', 'http://localhost:5001')
SKADES_SERVICE_URL = os.getenv('SKADES_SERVICE_URL', 'http://localhost:5002')
LEJEAFTALE_SERVICE_URL = os.getenv('LEJEAFTALE_SERVICE_URL', 'http://localhost:5003')

app = Flask(__name__)
swagger = Swagger(app, config=swagger_config)

#API Documentation
@app.route('/')
@swag_from('swagger/home.yaml')
def home():
    return jsonify({
        "service": "API Gateway",
        "available_endpoints": [
            {
                "path": "/rapport/login",
                "method": "POST",
                "description": "Login to get JWT token"
            },
            {
                "path": "/rapport/protected",
                "method": "GET",
                "description": "Access protected resource"
            },
            {
                "path": "/rapport/udlejedeBiler",
                "method": "GET",
                "description": "Get a list of rented cars and the total price sum"
            },
            {
                "path": "/rapport/gem_udlejede_biler",
                "method": "POST",
                "description": "Save the count of rented cars and the total price sum"
            },
            {
                "path": "/rapport/process_skade_niveau/<int:damage_niveau>",
                "method": "GET",
                "description": "Get specific damage data by niveau"
            },
            {
                "path": "/rapport/export_skadet_biler",
                "method": "GET",
                "description": "Export damaged cars data as CSV"
            },
            {
                "path": "/skade/hent_alle_skade_rapporter",
                "method": "GET",
                "description": "Fetch all damage reports"
            },
            {
                "path": "/skade/tilføj_skade_rapport",
                "method": "POST",
                "description": "Add a new damage report"
            },
            {
                "path": "/skade/slet_skade_rapport/<int:reportID>",
                "method": "DELETE",
                "description": "Delete a damage report"
            },
            {
                "path": "/skade/send_data",
                "method": "GET",
                "description": "Send static data"
            },
            {
                "path": "/skade/send_kunde_data/<int:lejeaftaleID>",
                "method": "GET",
                "description": "Fetch agreement and damage cost"
            },
            {
                "path": "/skade/process_damage_data",
                "method": "POST",
                "description": "Process damage data"
            },
            {
                "path": "/lejeaftale/hent_alle_aftaler",
                "method": "GET",
                "description": "Fetch all agreements"
            },
            {
                "path": "/lejeaftale/ledige_biler",
                "method": "GET",
                "description": "Fetch available cars"
            },
            {
                "path": "/lejeaftale/hent_nyeste_lejeaftale",
                "method": "GET",
                "description": "Fetch new agreements"
            },
            {
                "path": "/lejeaftale/opret_lejeaftale",
                "method": "POST",
                "description": "Add a new agreement"
            },
            {
                "path": "/lejeaftale/status_opdatering/<int:lejeAftaleID>",
                "method": "PUT",
                "description": "Update agreement status"
            },
            {
                "path": "/lejeaftale/slet_lejeaftale/<int:lejeAftaleID>",
                "method": "DELETE",
                "description": "Delete agreement"
            },
            {
                "path": "/lejeaftale/hent_lejeaftale_kundeID/<int:kundeID>",
                "method": "GET",
                "description": "Fetch customer data"
            },
            {
                "path": "/lejeaftale/process_data",
                "method": "POST",
                "description": "Process data to Skades Service"
            },
            {
                "path": "/lejeaftale/process_kunde_data",
                "method": "POST",
                "description": "Process customer data to Skades Service"
            },
            {
                "path": "/lejeaftale/send_skade_data/ny_dskade",
                "method": "POST",
                "description": "Send new damage data"
            },
            {
                "path": "/lejeaftale/hent_lejeaftaler",
                "method": "GET",
                "description": "Fetch active agreements"
            },
            {
                "path": "/lejeaftale/status/<int:bil_id>",
                "method": "GET",
                "description": "Fetch car status"
            },
            {
                "path": "/lejeaftale/process_pris_data",
                "method": "POST",
                "description": "Process price data"
            },
            {
                "path": "/lejeaftale/opdater_database",
                "method": "POST",
                "description": "Update database"
            },
            {
                "path": "/biler",
                "method": "GET",
                "description": "Fetch all cars"
            },
            {
                "path": "/biler/<int:bil_id>",
                "method": "GET",
                "description": "Fetch a specific car by ID"
            },
            {
                "path": "/biler/<int:bil_id>",
                "method": "DELETE",
                "description": "Delete a car"
            },
            {
                "path": "/biler/<int:bil_id>/status",
                "method": "PUT",
                "description": "Update car status"
            }
        ]
    })

###############   Routes for Rapport Service   ###############


###############   Health check   ###############

# Health check endpoint for API Gateway.
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API Gateway is running"}), 200


# 1. Login route (POST)
@app.route('/rapport/login', methods=['POST'])
@swag_from('swagger/rapportLogin.yaml')
def rapport_service_login():
    print(request.get_data())
    rapport_url = f'{RAPPORT_SERVICE_URL}/login'
    response = requests.post(rapport_url, data=request.get_data(), headers=request.headers)
    return jsonify(response.json())

# 2. Protected route (GET) (to check if you have access to the sensitive data with your login)
@app.route('/rapport/protected', methods=['GET'])
@swag_from('swagger/rapportProtected.yaml')
def rapport_service_protected():
    print(request.get_data())
    rapport_url = f'{RAPPORT_SERVICE_URL}/protected'
    response = requests.get(rapport_url, headers=request.headers)
    return jsonify(response.json())

# 3. Fetch rented cars (GET)
@app.route('/rapport/udlejedeBiler', methods=['GET'])
@swag_from('swagger/rapportUdlejedeBiler.yaml')
def rapport_service_rented_cars():
    rapport_url = f'{RAPPORT_SERVICE_URL}/udlejedeBiler'
    response = requests.get(rapport_url)
    return jsonify(response.json()), response.status_code

# 4. Save rented cars (POST)
@app.route('/rapport/gem_udlejede_biler', methods=['POST'])
@swag_from('swagger/rapportGemUdlejedeBiler.yaml')
def rapport_service_save_rented_cars():
    rapport_url = f'{RAPPORT_SERVICE_URL}/gemUdlejedeBiler'
    response = requests.post(rapport_url, data=request.get_data(), headers=request.headers)
    return jsonify(response.json()), response.status_code

# 1. Fetch damage niveau (GET)
@app.route('/rapport/process_skade_niveau/', methods=['GET'])
@app.route('/rapport/process_skade_niveau/<int:damage_niveau>', methods=['GET'])
@swag_from('swagger/rapportProcessSkadeNiveau.yaml')
def gateway_process_skade_niveau(damage_niveau=None):

    # Endpoint to fetch all damage levels or specific damage level data. Forwards the request to the Rapport Service.
    try:
        # Construct the URL for the Rapport Service
        if damage_niveau is not None:
            service_url = f"{RAPPORT_SERVICE_URL}/process-skade-niveau/{damage_niveau}"
        else:
            service_url = f"{RAPPORT_SERVICE_URL}/process-skade-niveau/"

        # Forward the GET request to the service
        response = requests.get(service_url, headers=request.headers)

        # Return the response from the Rapport Service
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": "Failed to process damage niveau", "details": str(e)}), 500


# 2. Export damaged cars to csv (GET)
@app.route('/rapport/export_skadet_biler', methods=['GET'])
@swag_from('swagger/rapportExportSkadetBiler.yaml')
def gateway_export_damaged_cars():
    # exports damaged car data as a CSV file. Forwards the request to Rapport Service.

    try:
        # Construct the URL for the Rapport Service
        service_url = f"{RAPPORT_SERVICE_URL}/export-skadet-biler"

        # Forward the GET request to the service
        response = requests.get(service_url, headers=request.headers)

        # Return the CSV file response from the Rapport Service
        if response.status_code == 200:
            return Response(
                response.content,
                mimetype='text/csv',
                headers={"Content-Disposition": "attachment; filename=damage_loss.csv"}
            )
        else:
            return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": "Failed to export damaged cars", "details": str(e)}), 500




###############   Routes for Skade Service   ###############


# 1. Fetch all damage reports (GET)
@app.route('/skade/hent_alle_skade_rapporter', methods=['GET'])
@swag_from('swagger/skadeHentAlleRapporter.yaml')
def skades_service_get_reports():
    skades_url = f'{SKADES_SERVICE_URL}/skadeRapporter'
    response = requests.get(skades_url, headers=request.headers)
    return jsonify(response.json()), response.status_code

# 2. Add a new damage report (POST)
@app.route('/skade/tilføj_skade_rapport', methods=['POST'])
@swag_from('swagger/skadeTilføjSkadeRapport.yaml')
def skades_service_add_report():
    skades_url = f'{SKADES_SERVICE_URL}/skadeRapporter'
    response = requests.post(skades_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 3. Delete a damage report (DELETE)
@app.route('/skade/slet_skade_rapport/<int:reportID>', methods=['DELETE'])
@swag_from('swagger/skadeSletSkadeRapport.yaml')
def skades_service_delete_report(reportID):
    skades_url = f'{SKADES_SERVICE_URL}/skadeRapporter/{reportID}'
    response = requests.delete(skades_url)
    return jsonify(response.json()), response.status_code

# 4. Send static data (GET)
@app.route('/skade/send_data', methods=['GET'])
@swag_from('swagger/skadeSendData.yaml')
def skades_service_send_data():
    skades_url = f'{SKADES_SERVICE_URL}/send-data'
    response = requests.get(skades_url)
    return jsonify(response.json()), response.status_code

# 5. Fetch agreement and damage cost (GET)
@app.route('/skade/send_kunde_data/<int:lejeaftaleID>', methods=['GET'])
@swag_from('swagger/skadeSendKundeData.yaml')
def skades_service_fetch_kunde_data(lejeaftaleID):
    skades_url = f'{SKADES_SERVICE_URL}/send-kunde-data/{lejeaftaleID}'
    response = requests.get(skades_url)
    return jsonify(response.json()), response.status_code

# 6. Process damage data (POST)
@app.route('/skade/process_damage_data', methods=['POST'])
@swag_from('swagger/skadeProcessDamageData.yaml')
def skades_service_process_damage():
    skades_url = f'{SKADES_SERVICE_URL}/process-damage-data'
    response = requests.post(skades_url, json=request.get_json())
    return jsonify(response.json()), response.status_code



###############   Routes for Skade Service   ###############


# 1. Fetch all agreements (GET)
@app.route('/lejeaftale/hent_alle_aftaler', methods=['GET'])
@swag_from('swagger/lejeaftaleHentAlleAftaler.yaml')
def get_all_agreements():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/lejeaftaler'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 2. Fetch available cars (GET)
@app.route('/lejeaftale/ledige_biler', methods=['GET'])
@swag_from('swagger/lejeaftaleLedigeBiler.yaml')
def available_cars():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/ledigeBiler'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 3. Fetch new agreements (GET)
@app.route('/lejeaftale/hent_nyeste_lejeaftale', methods=['GET'])
@swag_from('swagger/lejeaftaleHentNyesteLejeaftale.yaml')
def new_agreements():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/nyLejeaftale'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 4. Add a new agreement (POST)
@app.route('/lejeaftale/opret_lejeaftale', methods=['POST'])
@swag_from('swagger/lejeaftaleOpretLejeaftale.yaml')
def add_agreement():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/opretLejeaftale'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 5. Update agreement status (PUT)
@app.route('/lejeaftale/status_opdatering/<int:lejeAftaleID>', methods=['PUT'])
@swag_from('swagger/lejeaftaleStatusOpdatering.yaml')
def update_agreement_status(lejeAftaleID):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/statusOpdatering/{lejeAftaleID}'
    response = requests.put(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 6. Delete agreement (DELETE)
@app.route('/lejeaftale/slet_lejeaftale/<int:lejeAftaleID>', methods=['DELETE'])
@swag_from('swagger/lejeaftaleSletLejeaftale.yaml')
def remove_agreement(lejeAftaleID):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/sletLejeaftale/{lejeAftaleID}'
    response = requests.delete(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 7. Fetch customer data (GET)
@app.route('/lejeaftale/hent_lejeaftale_kundeID/<int:kundeID>', methods=['GET'])
@swag_from('swagger/lejeaftaleHentKundeID.yaml')
def get_customer_data(kundeID):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/kundeID/{kundeID}'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 8. Process data to Skades Service (POST)
@app.route('/lejeaftale/process_data', methods=['POST'])
@swag_from('swagger/lejeaftaleProcessData.yaml')
def process_data():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/process-data'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 9. Process customer data to Skades Service (POST)
@app.route('/lejeaftale/process_kunde_data', methods=['POST'])
@swag_from('swagger/lejeaftaleProcessKundeData.yaml')
def process_kunde_data():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/process-kunde-data'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 10. Send new damage data (POST)
@app.route('/lejeaftale/send_skade_data/ny_dskade', methods=['POST'])
@swag_from('swagger/lejeaftaleSendSkadeData.yaml')
def send_request():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/send-damage-data/new-damage'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 11. Fetch active agreements (GET)
@app.route('/lejeaftale/hent_lejeaftaler', methods=['GET'])
@swag_from('swagger/lejeaftaleHentLejeaftaler.yaml')
def active_lejeaftale():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/lejeaftale'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 12. Fetch car status (GET)
@app.route('/lejeaftale/status/<int:bil_id>', methods=['GET'])
@swag_from('swagger/lejeaftaleStatus.yaml')
def get_car_status(bil_id):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/status/{bil_id}'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 13. Process price data (POST)
@app.route('/lejeaftale/process_pris_data', methods=['POST'])
@swag_from('swagger/lejeaftaleProcessPrisData.yaml')
def process_price_data():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/process-pris-data'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 14. Update database (POST)
@app.route('/lejeaftale/opdater_database', methods=['POST'])
@swag_from('swagger/lejeaftaleOpdaterDatabase.yaml')
def opdater_database():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/opdater-database'
    response = requests.post(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 15. Fetch all cars (GET)
@app.route('/biler', methods=['GET'])
@swag_from('swagger/lejeaftaleBiler.yaml')
def get_all_cars():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/biler'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 16. Fetch a specific car by ID (GET)
@app.route('/biler/<int:bil_id>', methods=['GET'])
@swag_from('swagger/lejeaftaleBilerByID.yaml')
def get_car(bil_id):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/biler/{bil_id}'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 17. Delete a car (DELETE)
@app.route('/biler/<int:bil_id>', methods=['DELETE'])
@swag_from('swagger/lejeaftaleSletBilByID.yaml')
def remove_car(bil_id):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/biler/{bil_id}'
    response = requests.delete(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 18. Update car status (PUT)
@app.route('/biler/<int:bil_id>/status', methods=['PUT'])
@swag_from('swagger/lejeaftaleOpdaterBilStatus.yaml')
def change_car_status(bil_id):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/biler/{bil_id}/status'
    response = requests.put(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code


    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)