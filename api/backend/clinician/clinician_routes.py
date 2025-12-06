from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from pymysql.cursors import DictCursor  
from pymysql import Error                

clinician = Blueprint("clinician", __name__)


@clinician.route("/patients/<int:patient_id>/timeline", methods=["GET"])
def get_patient_timeline(patient_id):
    try:
        conn = db.get_db()

        # Use PyMySQL dictionary cursor
        cursor = conn.cursor(DictCursor)

        # Check patient exists
        cursor.execute("SELECT * FROM Patient WHERE patientId = %s", (patient_id,))
        patient = cursor.fetchone()
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        cursor.execute("SELECT * FROM Vitals WHERE patientId = %s", (patient_id,))
        vitals = cursor.fetchall()

        cursor.execute("SELECT * FROM Conditions WHERE patientId = %s", (patient_id,))
        conditions = cursor.fetchall()

        cursor.execute("SELECT * FROM Treatment WHERE patientId = %s", (patient_id,))
        treatments = cursor.fetchall()

        cursor.execute("SELECT * FROM CarePlan WHERE patientId = %s", (patient_id,))
        careplans = cursor.fetchall()

        cursor.execute("SELECT * FROM Appointment WHERE patientId = %s", (patient_id,))
        appointments = cursor.fetchall()

        cursor.execute("SELECT * FROM LabResult WHERE patientId = %s", (patient_id,))
        labs = cursor.fetchall()

        cursor.close()

        # Response
        return jsonify({
            "patient": patient,
            "vitals": vitals,
            "conditions": conditions,
            "treatments": treatments,
            "careplans": careplans,
            "appointments": appointments,
            "lab_results": labs
        }), 200

    except Error as e:
        current_app.logger.error(str(e))
        return jsonify({"error": str(e)}), 500



# --- Patients ---
def get_patient(patient_id):
    conn = db.get_db()
    cursor = conn.cursor(DictCursor)
    cursor.execute("SELECT * FROM Patient WHERE patientId = %s", (patient_id,))
    result = cursor.fetchall()
    return result[0] if result else None

def get_all_patients():
    conn = db.get_db()
    cursor = conn.cursor(DictCursor)
    cursor.execute("SELECT * FROM Patient")
    result = cursor.fetchall()
    return result

# --- Vitals ---
def get_vitals(patient_id):
    conn = db.get_db()
    cursor = conn.cursor(DictCursor)
    cursor.execute("SELECT * FROM Vitals WHERE patientId = %s ORDER BY timestamp DESC", (patient_id,))
    result = cursor.fetchall()
    return result[0] if result else None

# --- Care Plans ---
def get_careplans(patient_id):
    conn = db.get_db()
    cursor = conn.cursor(DictCursor)
    cursor.execute("SELECT * FROM CarePlan WHERE patientId = %s", (patient_id,))
    result = cursor.fetchall()
    return result[0] if result else None

def create_careplan(patient_id, goals, start_time, end_time, staff_id):
    sql = """
        INSERT INTO CarePlan (goals, startTime, endTime, patientId, staffId)
        VALUES (%s, %s, %s, %s, %s)
    """
    conn = db.get_db()
    cursor = conn.cursor(DictCursor)
    cursor.execute(sql, (goals, start_time, end_time, patient_id, staff_id))

# --- Medications / Treatments ---
def get_treatments(patient_id):
    conn = db.get_db()
    cursor = conn.cursor(DictCursor)
    cursor.execute("SELECT * FROM Treatment WHERE patientId = %s", (patient_id,))
    result = cursor.fetchall()
    return result[0] if result else None
