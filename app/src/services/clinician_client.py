import requests

API_BASE = "http://web-api:4000"   

def get_patient(patient_id: str):
    resp = requests.get(f"{API_BASE}/clinician/patient/{patient_id}")
    resp.raise_for_status()
    return resp.json()

def get_vitals(patient_id: str):
    resp = requests.get(f"{API_BASE}/clinician/vitals/{patient_id}")
    resp.raise_for_status()
    return resp.json()

def get_careplans(patient_id: str):
    resp = requests.get(f"{API_BASE}/clinician/careplans/{patient_id}")
    resp.raise_for_status()
    return resp.json()
