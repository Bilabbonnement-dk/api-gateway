from flask import Flask, jsonify, request
import requests, os

RAPPORT_SERVICE_URL = os.getenv('RAPPORT_SERVICE_URL', 'http://localhost:5001')
SKADES_SERVICE_URL = os.getenv('SKADES_SERVICE_URL', 'http://localhost:5002')
LEJEAFTALE_SERVICE_URL = os.getenv('http://localhost:5003')

app = Flask(__name__)


###############   Routes for Rapport Service   ###############

# 1. Login Route (POST)
@app.route('/rapport/login', methods=['POST'])
def rapport_service_login():
    print(request.get_data())
    rapport_url = f'{RAPPORT_SERVICE_URL}/login'
    response = requests.post(rapport_url, data=request.get_data(), headers=request.headers)
    return jsonify(response.json())

# 2. Protected Route (GET)
@app.route('/rapport/protected', methods=['GET'])
def rapport_service_protected():
    print(request.get_data())
    rapport_url = f'{RAPPORT_SERVICE_URL}/protected'
    response = requests.get(rapport_url, headers=request.headers)
    return jsonify(response.json())

# 3. Fetch Rented Cars (GET)
@app.route('/rapport/udlejedeBiler', methods=['GET'])
def rapport_service_rented_cars():
    rapport_url = f'{RAPPORT_SERVICE_URL}/udlejedeBiler'
    response = requests.get(rapport_url)
    return jsonify(response.json()), response.status_code

# 4. Save Rented Cars (POST)
@app.route('/rapport/gemUdlejedeBiler', methods=['POST'])
def rapport_service_save_rented_cars():
    rapport_url = f'{RAPPORT_SERVICE_URL}/gemUdlejedeBiler'
    response = requests.post(rapport_url, data=request.get_data(), headers=request.headers)
    return jsonify(response.json()), response.status_code

# 5. Fetch Report (GET)
@app.route('/rapport/hentRapport', methods=['GET'])
def rapport_service_fetch_report():
    rapport_url = f'{RAPPORT_SERVICE_URL}/hentRapport'
    response = requests.get(rapport_url)
    return jsonify(response.json()), response.status_code

# 6. Fetch Report by Date (GET)
@app.route('/rapport/hentRapport/<string:date>', methods=['GET'])
def rapport_service_fetch_report_by_date(date):
    rapport_url = f'{RAPPORT_SERVICE_URL}/hentRapport/{date}'
    response = requests.get(rapport_url)
    return jsonify(response.json()), response.status_code



###############   Routes for Skade Service   ###############


# 1. Fetch all damage reports (GET)
@app.route('/skadeRapporter', methods=['GET'])
def skades_service_get_reports():
    skades_url = f'{SKADES_SERVICE_URL}/skadeRapporter'
    response = requests.get(skades_url)
    return jsonify(response.json()), response.status_code

# 2. Add a new damage report (POST)
@app.route('/skadeRapporter', methods=['POST'])
def skades_service_add_report():
    skades_url = f'{SKADES_SERVICE_URL}/skadeRapporter'
    response = requests.post(skades_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 3. Delete a damage report (DELETE)
@app.route('/skadeRapporter/<int:reportID>', methods=['DELETE'])
def skades_service_delete_report(reportID):
    skades_url = f'{SKADES_SERVICE_URL}/skadeRapporter/{reportID}'
    response = requests.delete(skades_url)
    return jsonify(response.json()), response.status_code

# 4. Send static data (GET)
@app.route('/skade/send-data', methods=['GET'])
def skades_service_send_data():
    skades_url = f'{SKADES_SERVICE_URL}/send-data'
    response = requests.get(skades_url)
    return jsonify(response.json()), response.status_code

# 5. Fetch agreement and damage cost (GET)
@app.route('/skade/send-kunde-data/<int:lejeaftaleID>', methods=['GET'])
def skades_service_fetch_kunde_data(lejeaftaleID):
    skades_url = f'{SKADES_SERVICE_URL}/send-kunde-data/{lejeaftaleID}'
    response = requests.get(skades_url)
    return jsonify(response.json()), response.status_code

# 6. Process damage data (POST)
@app.route('/skade/process-damage-data', methods=['POST'])
def skades_service_process_damage():
    skades_url = f'{SKADES_SERVICE_URL}/process-damage-data'
    response = requests.post(skades_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 7. Send damage data (GET with an optional perameter: damage_niveau)
@app.route('/skade/send-skade-data', defaults={'damage_niveau': None}, methods=['GET'])
@app.route('/skade/send-skade-data/<int:damage_niveau>', methods=['GET'])
def skades_service_send_skade_data(damage_niveau):
    skades_url = f'{SKADES_SERVICE_URL}/send-skade-data'
    if damage_niveau is not None:
        skades_url += f'/{damage_niveau}'
    response = requests.get(skades_url)
    return jsonify(response.json()), response.status_code



###############   Routes for Skade Service   ###############


# 1. Fetch all agreements (GET)
@app.route('/lejeaftaler', methods=['GET'])
def get_all_agreements():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/lejeaftaler'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 2. Fetch available cars (GET)
@app.route('/ledigeBiler', methods=['GET'])
def available_cars():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/ledigeBiler'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 3. Fetch new agreements (GET)
@app.route('/nyLejeaftale', methods=['GET'])
def new_agreements():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/nyLejeaftale'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 4. Add a new agreement (POST)
@app.route('/opretLejeaftale', methods=['POST'])
def add_agreement():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/opretLejeaftale'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 5. Update agreement status (PUT)
@app.route('/statusOpdatering/<int:lejeAftaleID>', methods=['PUT'])
def update_agreement_status(lejeAftaleID):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/statusOpdatering/{lejeAftaleID}'
    response = requests.put(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 6. Delete agreement (DELETE)
@app.route('/sletLejeaftale/<int:lejeAftaleID>', methods=['DELETE'])
def remove_agreement(lejeAftaleID):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/sletLejeaftale/{lejeAftaleID}'
    response = requests.delete(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 7. Fetch customer data (GET)
@app.route('/kundeID/<int:kundeID>', methods=['GET'])
def get_customer_data(kundeID):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/kundeID/{kundeID}'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 8. Process data to Skades Service (POST)
@app.route('/process-data', methods=['POST'])
def process_data():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/process-data'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 9. Process customer data to Skades Service (POST)
@app.route('/process-kunde-data', methods=['POST'])
def process_kunde_data():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/process-kunde-data'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 10. Send new damage data (POST)
@app.route('/send-damage-data/new-damage', methods=['POST'])
def send_request():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/send-damage-data/new-damage'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 11. Fetch active agreements (GET)
@app.route('/lejeaftale', methods=['GET'])
def active_lejeaftale():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/lejeaftale'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 12. Fetch car status (GET)
@app.route('/status/<int:bil_id>', methods=['GET'])
def get_car_status(bil_id):
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/status/{bil_id}'
    response = requests.get(lejeaftale_url)
    return jsonify(response.json()), response.status_code

# 13. Process price data (POST)
@app.route('/process-pris-data', methods=['POST'])
def process_price_data():
    lejeaftale_url = f'{LEJEAFTALE_SERVICE_URL}/process-pris-data'
    response = requests.post(lejeaftale_url, json=request.get_json())
    return jsonify(response.json()), response.status_code

# 14. Update database (POST)
@app.route('/opdater-database', methods=['POST'])
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