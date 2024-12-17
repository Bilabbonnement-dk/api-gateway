from flask import Flask, Response, jsonify, request
import requests, os

RAPPORT_SERVICE_URL = os.getenv('RAPPORT_SERVICE_URL', 'http://localhost:5001')
SKADES_SERVICE_URL = os.getenv('SKADES_SERVICE_URL', 'http://localhost:5002')
LEJEAFTALE_SERVICE_URL = os.getenv('LEJEAFTALE_SERVICE_URL', 'http://localhost:5003')

app = Flask(__name__)


###############   Routes for Rapport Service   ###############

# 1. Login route (POST)
@app.route('/rapport/login', methods=['POST'])
def rapport_service_login():
    print(request.get_data())
    rapport_url = f'{RAPPORT_SERVICE_URL}/login'
    response = requests.post(rapport_url, data=request.get_data(), headers=request.headers)
    return jsonify(response.json())

# 2. Protected route (GET) (to check if you have access to the sensitive data with your login)
@app.route('/rapport/protected', methods=['GET'])
def rapport_service_protected():
    print(request.get_data())
    rapport_url = f'{RAPPORT_SERVICE_URL}/protected'
    response = requests.get(rapport_url, headers=request.headers)
    return jsonify(response.json())

# 3. Fetch rented cars (GET)
@app.route('/rapport/udlejedeBiler', methods=['GET'])
def rapport_service_rented_cars():
    rapport_url = f'{RAPPORT_SERVICE_URL}/udlejedeBiler'
    response = requests.get(rapport_url)
    return jsonify(response.json()), response.status_code

# 4. Save rented cars (POST)
@app.route('/rapport/gem_udlejede_biler', methods=['POST'])
def rapport_service_save_rented_cars():
    rapport_url = f'{RAPPORT_SERVICE_URL}/gemUdlejedeBiler'
    response = requests.post(rapport_url, data=request.get_data(), headers=request.headers)
    return jsonify(response.json()), response.status_code

# 1. Fetch damage niveau (GET)
@app.route('/rapport/process_skade_niveau/', methods=['GET'])
@app.route('/rapport/process_skade_niveau/<int:damage_niveau>', methods=['GET'])
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
def skades_service_get_reports():
    skades_url = f'{SKADES_SERVICE_URL}/skadeRapporter'
    response = requests.get(skades_url, headers=request.headers)
    return jsonify(response.json()), response.status_code

# 2. Add a new damage report (POST)
@app.route('/skade/tilføj_skade_rapport', methods=['POST'])
def skades_service_add_report():
    skades_url = f'{SKADES_SERVICE_URL}/skadeRapporter'
    response = requests.post(skades_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 3. Delete a damage report (DELETE)
@app.route('/skade/slet_skade_rapport/<int:reportID>', methods=['DELETE'])
def skades_service_delete_report(reportID):
    skades_url = f'{SKADES_SERVICE_URL}/skadeRapporter/{reportID}'
    response = requests.delete(skades_url)
    return jsonify(response.json()), response.status_code

# 4. Send static data (GET)
@app.route('/skade/send_data', methods=['GET'])
def skades_service_send_data():
    skades_url = f'{SKADES_SERVICE_URL}/send-data'
    response = requests.get(skades_url)
    return jsonify(response.json()), response.status_code

# 5. Fetch agreement and damage cost (GET)
@app.route('/skade/send_kunde_data/<int:lejeaftaleID>', methods=['GET'])
def skades_service_fetch_kunde_data(lejeaftaleID):
    skades_url = f'{SKADES_SERVICE_URL}/send-kunde-data/{lejeaftaleID}'
    response = requests.get(skades_url)
    return jsonify(response.json()), response.status_code

# 6. Process damage data (POST)
@app.route('/skade/process_damage_data', methods=['POST'])
def skades_service_process_damage():
    skades_url = f'{SKADES_SERVICE_URL}/process-damage-data'
    response = requests.post(skades_url, json=request.get_json())
    return jsonify(response.json()), response.status_code



###############   Routes for Skade Service   ###############


# 1. Fetch all agreements (GET)
@app.route('/lejeaftale/hent_alle_aftaler', methods=['GET'])
def get_all_agreements():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/lejeaftaler'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 2. Fetch available cars (GET)
@app.route('/lejeaftale/ledige_biler', methods=['GET'])
def available_cars():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/ledigeBiler'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 3. Fetch new agreements (GET)
@app.route('/lejeaftale/hent_nyeste_lejeaftale', methods=['GET'])
def new_agreements():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/nyLejeaftale'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 4. Add a new agreement (POST)
@app.route('/lejeaftale/opret_lejeaftale', methods=['POST'])
def add_agreement():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/opretLejeaftale'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 5. Update agreement status (PUT)
@app.route('/lejeaftale/status_opdatering/<int:lejeAftaleID>', methods=['PUT'])
def update_agreement_status(lejeAftaleID):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/statusOpdatering/{lejeAftaleID}'
    response = requests.put(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 6. Delete agreement (DELETE)
@app.route('/lejeaftale/slet_lejeaftale/<int:lejeAftaleID>', methods=['DELETE'])
def remove_agreement(lejeAftaleID):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/sletLejeaftale/{lejeAftaleID}'
    response = requests.delete(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 7. Fetch customer data (GET)
@app.route('/lejeaftale/hent_lejeaftale_kundeID/<int:kundeID>', methods=['GET'])
def get_customer_data(kundeID):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/kundeID/{kundeID}'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 8. Process data to Skades Service (POST)
@app.route('/lejeaftale/process_data', methods=['POST'])
def process_data():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/process-data'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 9. Process customer data to Skades Service (POST)
@app.route('/lejeaftale/process_kunde_data', methods=['POST'])
def process_kunde_data():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/process-kunde-data'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 10. Send new damage data (POST)
@app.route('/lejeaftale/send_skade_data/ny_dskade', methods=['POST'])
def send_request():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/send-damage-data/new-damage'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 11. Fetch active agreements (GET)
@app.route('/lejeaftale/hent_lejeaftaler', methods=['GET'])
def active_lejeaftale():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/lejeaftale'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 12. Fetch car status (GET)
@app.route('/lejeaftale/status/<int:bil_id>', methods=['GET'])
def get_car_status(bil_id):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/status/{bil_id}'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 13. Process price data (POST)
@app.route('/lejeaftale/process_pris_data', methods=['POST'])
def process_price_data():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/process-pris-data'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 14. Update database (POST)
@app.route('/lejeaftale/opdater_database', methods=['POST'])
def opdater_database():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/opdater-database'
    response = requests.post(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 15. Fetch all cars (GET)
@app.route('/biler', methods=['GET'])
def get_all_cars():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/biler'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 16. Fetch a specific car by ID (GET)
@app.route('/biler/<int:bil_id>', methods=['GET'])
def get_car(bil_id):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/biler/{bil_id}'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 17. Delete a car (DELETE)
@app.route('/biler/<int:bil_id>', methods=['DELETE'])
def remove_car(bil_id):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/biler/{bil_id}'
    response = requests.delete(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 18. Update car status (PUT)
@app.route('/biler/<int:bil_id>/status', methods=['PUT'])
def change_car_status(bil_id):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/biler/{bil_id}/status'
    response = requests.put(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code



###############   Health check   ###############

# Health check endpoint for API Gateway.
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API Gateway is running"}), 200

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)