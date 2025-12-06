
from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app  
import io
import csv


clinician = Blueprint("clinician", __name__)

@clinician.route("/patients/<int:patient_id>/timeline", methods=["GET"])
def get_patient_timeline(patient_id):
    try:
        cursor = db.get_db().cursor()

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






# -------------------------------------------------------------
# 2. Risk Alerts (for clinicians)
# -------------------------------------------------------------
@clinician.route("/risk", methods=["GET"])
def get_risk_alerts():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("""
            SELECT * FROM SystemAlert
            WHERE severity IN ('warning', 'CRITICAL')
            ORDER BY timestamp DESC
        """)

        alerts = cursor.fetchall()
        cursor.close()
        return jsonify(alerts), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------------------
# 3. Care Plan Management
# -------------------------------------------------------------
@clinician.route("/careplans", methods=["POST"])
def create_care_plan():
    """
    Create a new care plan.
    Required fields:
        - goals
        - startTime
        - staffId
        - patientId
    """
    try:
        data = request.get_json()
        required = ["goals", "startTime", "staffId", "patientId"]

        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO CarePlan (goals, startTime, endTime, staffId, patientId)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["goals"],
            data["startTime"],
            data.get("endTime"),
            data["staffId"],
            data["patientId"]
        ))

        db.get_db().commit()
        new_id = cursor.lastrowid
        cursor.close()

        return jsonify({
            "message": "Care plan created successfully",
            "carePlanId": new_id
        }), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


@clinician.route("/careplans/<int:careplan_id>", methods=["PUT"])
def update_care_plan(careplan_id):
    """
    Update a care plan's goals, dates, or staff assignment.
    """
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()

        # Check exists
        cursor.execute("SELECT * FROM CarePlan WHERE carePlanId = %s", (careplan_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Care plan not found"}), 404

        update_fields = []
        params = []

        allowed = ["goals", "startTime", "endTime", "staffId"]
        for field in allowed:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(careplan_id)
        query = f"UPDATE CarePlan SET {', '.join(update_fields)} WHERE carePlanId = %s"
        cursor.execute(query, params)

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Care plan updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------------------
# 4. Smart Notes (auto-summarized)
# -------------------------------------------------------------
@clinician.route("/notes", methods=["POST"])
def create_note():
    """
    Creates a new note (Smart Notes Integration).
    Currently stores a summarized version in AuditLog.
    """
    try:
        data = request.get_json()

        required = ["action", "outcome", "staffId"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO AuditLog (timeStamp, action, outcome, staffId)
            VALUES (NOW(), %s, %s, %s)
        """
        cursor.execute(query, (
            data["action"],
            data["outcome"],  # this stores auto-summary
            data["staffId"]
        ))

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Note stored successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------------------
# 5. Medication Tracking
# -------------------------------------------------------------
@clinician.route("/medications/<int:patient_id>", methods=["GET"])
def get_patient_medications(patient_id):
    try:
        cursor = db.get_db().cursor(dictionary=True)

        cursor.execute("SELECT * FROM Treatment WHERE patientId = %s", (patient_id,))
        meds = cursor.fetchall()

        cursor.close()
        return jsonify(meds), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


@clinician.route("/medications", methods=["POST"])
def add_medication():
    """
    Add a new treatment.
    """
    try:
        data = request.get_json()
        required = ["treatmentId", "type", "name", "dosage", "frequency", "startdate", "endDate", "patientId"]

        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO Treatment (treatmentId, type, name, dosage, frequency, startdate, endDate, patientId)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["treatmentId"],
            data["type"],
            data["name"],
            data["dosage"],
            data["frequency"],
            data["startdate"],
            data["endDate"],
            data["patientId"]
        ))

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Medication added successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500








