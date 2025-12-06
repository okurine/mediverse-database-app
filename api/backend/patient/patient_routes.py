# backend/patient/patient_routes.py
from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app  
import io
import csv


# Create a Blueprint 
patient = Blueprint("patients", __name__)


# ---------------- Patient Health Dashboard ----------------
@patient.route("/patients/<int:patient_id>/dashboard", methods=["GET"])
def patient_dashboard(patient_id):
    """
    Returns an overview: latest vitals, active care plans, treatments, recent labs
    """
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Patient WHERE patientId = %s", (patient_id,))
        patient_row = cursor.fetchone()
        if not patient_row:
            return jsonify({"error": "Patient not found"}), 404

        cursor.execute("SELECT * FROM Vitals WHERE patientId = %s ORDER BY timestamp DESC LIMIT 20", (patient_id,))
        vitals = cursor.fetchall()

        cursor.execute("SELECT * FROM CarePlan WHERE patientId = %s ORDER BY startTime DESC", (patient_id,))
        careplans = cursor.fetchall()

        cursor.execute("SELECT * FROM Treatment WHERE patientId = %s", (patient_id,))
        treatments = cursor.fetchall()

        cursor.execute("SELECT * FROM LabResult WHERE patientId = %s ORDER BY date DESC LIMIT 20", (patient_id,))
        labs = cursor.fetchall()

        cursor.close()
        return jsonify({
            "patient": patient_row,
            "vitals": vitals,
            "careplans": careplans,
            "treatments": treatments,
            "labs": labs
        }), 200
    except Error as e:
        current_app.logger.error(f"patient_dashboard: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- Care Plans for Patient (read-only for patients) ----------------
@patient.route("/patients/<int:patient_id>/careplans", methods=["GET"])
def get_patient_careplans(patient_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM CarePlan WHERE patientId = %s ORDER BY startTime DESC", (patient_id,))
        cps = cursor.fetchall()
        cursor.close()
        return jsonify(cps), 200
    except Error as e:
        current_app.logger.error(f"get_patient_careplans: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- Treatments for Patient (read-only) ----------------
@patient.route("/patients/<int:patient_id>/treatments", methods=["GET"])
def get_patient_treatments(patient_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM Treatment WHERE patientId = %s", (patient_id,))
        txs = cursor.fetchall()
        cursor.close()
        return jsonify(txs), 200
    except Error as e:
        current_app.logger.error(f"get_patient_treatments: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- Export patient data ----------------
@patient.route("/patients/<int:patient_id>/export", methods=["GET"])
def export_patient_data(patient_id):
    """
    Return CSV string of selected patient data (vitals + labs + careplans + treatments)
    """
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM Vitals WHERE patientId = %s ORDER BY timestamp", (patient_id,))
        vitals = cursor.fetchall()
        cursor.execute("SELECT * FROM LabResult WHERE patientId = %s ORDER BY date", (patient_id,))
        labs = cursor.fetchall()
        cursor.execute("SELECT * FROM CarePlan WHERE patientId = %s ORDER BY startTime", (patient_id,))
        careplans = cursor.fetchall()
        cursor.execute("SELECT * FROM Treatment WHERE patientId = %s", (patient_id,))
        treatments = cursor.fetchall()
        cursor.close()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["source", "type", "value", "timestamp", "notes", "extra"])
        for v in vitals:
            writer.writerow(["vital", v.get("type"), v.get("value"), v.get("timestamp"), "", v.get("patientId")])
        for l in labs:
            writer.writerow(["lab", l.get("labType"), l.get("value"), l.get("date"), "", l.get("patientId")])
        for c in careplans:
            writer.writerow(["careplan", c.get("goals"), "", c.get("startTime"), "", c.get("endTime")])
        for t in treatments:
            writer.writerow(["treatment", t.get("name"), t.get("dosage"), t.get("startdate"), t.get("frequency"), t.get("patientId")])

        csv_data = output.getvalue()
        return jsonify({"csv": csv_data}), 200
    except Error as e:
        current_app.logger.error(f"export_patient_data: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- Patient: Data Security Info ----------------
@patient.route("/patients/<int:patient_id>/security", methods=["GET"])
def patient_security_info(patient_id):
    """
    Return info about permissions and security summary for patient (what was accessed recently)
    """
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM AuditLog WHERE staffId IS NOT NULL ORDER BY timeStamp DESC LIMIT 20")
        recent_access = cursor.fetchall()
        cursor.close()
        return jsonify({"recent_access": recent_access, "message": "Your data is protected. See admin for more details."}), 200
    except Error as e:
        current_app.logger.error(f"patient_security_info: {e}")
        return jsonify({"error": str(e)}), 500
