# API Gateway 

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
![Azure](https://img.shields.io/badge/Microsoft%20Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white)

Dette repository indeholder koden til API-gateway, der fungerer som en mellemmand for klienter og tre separate microservices, Rapport Service, Lejeaftale Service og Skade Service. API-gateway håndterer routing og videresender anmodninger til de relevante services.

## Indholdsfortegnelse

1. [Introduktion](#introduktion)
2. [Arkitektur](#arkitektur)
3. [Installation og Opsætning](#installation-og-opsætning)
4. [Tilgængelige Endpoints](#tilgængelige-endpoints)
    * [Rapport Service](#rapport-service)
    * [Skade Service](#skade-service)
    * [Lejeaftale Service](#lejeaftale-service)
    * [Sundhedstjek](#sundhedstjek)
9. [Miljøvariabler](#miljøvariabler)
10. [Kørsel og Drift](#kørsel-og-drift)
11. [Fejlhåndtering](#fejlhåndtering)


## Introduktion

API-gateway fungerer som en centraliseret indgang til at interagere med følgende microservices:

* Rapport Service: Håndterer rapportering, dataeksport og skaderegistrering.
* Skade Service: Administrerer skaderapporter og relaterede operationer.
* Lejeaftale Service: Styrer lejeaftaler, bilstatus og kundedata.

Gateway'en eksponerer samlet adgang til endpoints for disse services og sikrer, at forespørgsler videresendes korrekt.


## Arkitektur

API-gatewayen bruger Flask som webframework og håndterer routing til tre services via HTTP-requests. Kommunikation mellem gateway og microservices sker via RESTful APIs. For bedre skalerbarhed og fleksibilitet, kan miljøvariabler bruges til at konfigurere URL'er for services.

**Oversigt**:

```plaintext
Klienter --> API Gateway --> Rapport Service (Port 5001)
                         --> Skade Service (Port 5002)
                         --> Lejeaftale Service (Port 5003)
```


## Installation og Opsætning

Følg disse trin for at installere og køre API-gateway lokalt:

### Krav

* Python 3.x
* Flask bibliotek
* requests bibliotek

### Trin-for-trin Guide

1. **Klon repositoryet**:
```bash
git clone https://github.com/Bilabbonnement-dk/api-gateway.git
cd api-gateway
```
2. **Installer nødvendige pakker**:
Kør følgende kommando for at installere Flask og requests:
```bash
pip install flask requests
```
3. **Konfigurer miljøvariabler**:
Man kan tilpasse URL'er til microservices ved at oprette en .env-fil i projektmappen. 
Eksempel:
```env
RAPPORT_SERVICE_URL=http://localhost:5001
SKADES_SERVICE_URL=http://localhost:5002
LEJEAFTALE_SERVICE_URL=http://localhost:5003
```
4. ***Start API Gateway***:
Kør følgende kommando for at starte serveren:
```bash
python api_gateway.py
```
Gateway køre nu på porten 5004.

5. **Test API-gatewayen**:
Du kan teste ved at sende anmodninger til:
```bash
http://localhost:5004/health
```


## Tilgængelige Endpoints

API-gateway servicen eksponerer en række endpoints til de tre services. Nedenfor er en oversigt over alle tilgængelige ruter.

1. ### Rapport Service
|   Endpoint	                               |   Metode	       |   Beskrivelse
|---------------------------------------|-----------------------|-----------------------------------------------------------|
| `/rapport/login`                        |   POST	                |   Log ind og få adgang til Rapport Service.               |
| `/rapport/protected`                    |   GET	                |   Kontroller adgang til beskyttede data.                  |
| `/rapport/udlejedeBiler`                |   GET	                |   Hent liste over udlejede biler.                         |
| `/rapport/gem_udlejede_biler`           |   POST	                |   Gem udlejede biler i systemet.                          |
| `/rapport/process_skade_niveau/`	      |   GET	                |   Hent alle skadeniveauer.                                |
| `/rapport/process_skade_niveau/<id>`	   |   GET	                |   Hent specifikt skadeniveau baseret på ID.               |
| `/rapport/export_skadet_biler`       	|   GET	                |   Eksporter skadet-bil-data som CSV-fil.                  |


2. ### Skade Service
|   Endpoint                                 |   Metode	       |   Beskrivelse
|---------------------------------------|-----------------------|-----------------------------------------------------------|
| `/skade/hent_alle_skade_rapporter`         |   GET	                |   Hent alle skaderapporter.                               |
| `/skade/tilføj_skade_rapport`	            |   POST	                |   Tilføj en ny skaderapport.                              |
| `/skade/slet_skade_rapport/<reportID>`	   |   DELETE	             |   Slet en skaderapport med angivet ID.                    |
| `/skade/send_data`	                        |   GET	                |   Send statiske data om skader.                           |
| `/skade/send_kunde_data/<lejeaftaleID>`	   |   GET	                |   Hent skadeomkostninger for en specifik lejeaftale.      |
| `/skade/process_damage_data`	            |   POST	                |   Processer skade-data i systemet.                        |

3. ### Lejeaftale Service
|  Endpoint	                                 |   Metode	       |   Beskrivelse
|---------------------------------------|-----------------------|-----------------------------------------------------------|
| `/lejeaftale/hent_alle_aftaler`	         |   GET	                |   Hent alle lejeaftaler.                                  |
| `/lejeaftale/ledige_biler`	               |   GET	                |   Hent ledige biler i systemet.                           |
| `/lejeaftale/opret_lejeaftale`	            |   POST	                |   Opret en ny lejeaftale.                                 |  
| `/lejeaftale/status_opdatering/<id>`	      |   PUT	                |   Opdater status for en lejeaftale.                       |
| `/biler`	                                 |   GET	                |   Hent alle biler i systemet.                             |
| `/biler/<bil_id>`	                        |   GET	                |   Hent specifik bil baseret på ID.                        |
| `/biler/<bil_id>/status`	                  |   PUT	                |   Opdater status for en bil.                              |


4. ### Sundhedstjek
|   Endpoint	                              |   Metode	       |   Beskrivelse
|---------------------------------------|-----------------------|-----------------------------------------------------------|
| `/health`	                                 |   GET	                |   Tjek status for API-gatewayen.                          |


## Miljøvariabler

Gatewayen bruger følgende miljøvariabler til at konfigurere service-URL'er:

|   Variabel	            |   Standardværdi	         |   Beskrivelse
|---------------------------------------|-----------------------|-----------------------------------------------------------|
| RAPPORT_SERVICE_URL	   | http://localhost:5001    | URL til Rapport Service.                                                  |
| SKADES_SERVICE_URL	      | http://localhost:5002	   | URL til Skade Service.                                                    |
| LEJEAFTALE_SERVICE_URL	| http://localhost:5003	   | URL til Lejeaftale Service.                                               |


## Kørsel og Drift

For at køre gatewayen i produktion anbefales det at bruge en WSGI-server som Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5004 api_gateway:app
```
Hvis man kun ønsker at køre gateway servicen lokalt og ikke i et produktions miljø, kan man bruge:
```bash
python3 api-gateway.py
```

## Fejlhåndtering

API-gatewayen håndterer fejl og videresender svar fra microservices. Ved interne fejl returneres en 500-fejl med detaljer:

```json
{
    "error": "Fejlbeskrivelse",
    "details": "Fejldetaljer"
}
```

### Kontakt

Hvis du har nogen spørgsmål eller oplever problemer, så er du velkommen til at kontakt udviklerteamet: Natazja, Sofie og Viktor.
