# backend/analyst/analyst_routes.py
from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from pymysql.cursors import DictCursor  
from pymysql import Error                

import csv
import io
import datetime


analyst = Blueprint("analyst", __name__)

# ---------------- Data Requests ----------------
@analyst.route("/datarequests", methods=["GET"])
def list_data_requests():
    try:
        cursor = db.get_db().cursor(DictCursor)
        cursor.execute("SELECT * FROM DataRequest ORDER BY dateCreated DESC")
        reqs = cursor.fetchall()
        cursor.close()
        return jsonify(reqs), 200
    except Error as e:
        current_app.logger.error(f"list_data_requests: {e}")
        return jsonify({"error": str(e)}), 500

@analyst.route("/datarequests", methods=["POST"])
def create_data_request():
    try:
        data = request.get_json() or {}
        required = ["title", "description", "dateCreated", "staffId"]
        for r in required:
            if r not in data:
                return jsonify({"error": f"Missing {r}"}), 400

        cursor = db.get_db().cursor()
        cursor.execute(
            "INSERT INTO DataRequest (title, description, status, dateCreated, staffId) VALUES (%s, %s, %s, %s, %s)",
            (data["title"], data["description"], data.get("status", "pending"), data["dateCreated"], data["staffId"])
        )
        db.get_db().commit()
        new_id = cursor.lastrowid
        cursor.close()
        return jsonify({"message": "request created", "requestId": new_id}), 201
    except Error as e:
        current_app.logger.error(f"create_data_request: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- Projects ----------------
@analyst.route("/projects", methods=["GET"])
def get_projects():
    try:
        cursor = db.get_db().cursor(DictCursor)
        cursor.execute("SELECT * FROM Project")
        projects = cursor.fetchall()
        cursor.close()
        return jsonify(projects), 200
    except Error as e:
        current_app.logger.error(f"get_projects: {e}")
        return jsonify({"error": str(e)}), 500

@analyst.route("/projects", methods=["POST"])
def create_project():
    try:
        data = request.get_json() or {}
        required = ["name", "startDate", "endDate", "requestId"]
        for r in required:
            if r not in data:
                return jsonify({"error": f"Missing {r}"}), 400
        cursor = db.get_db().cursor()
        cursor.execute("INSERT INTO Project (name, startDate, endDate, requestId) VALUES (%s, %s, %s, %s)",
                       (data["name"], data["startDate"], data["endDate"], data["requestId"]))
        db.get_db().commit()
        pid = cursor.lastrowid
        cursor.close()
        return jsonify({"message": "project created", "projectId": pid}), 201
    except Error as e:
        current_app.logger.error(f"create_project: {e}")
        return jsonify({"error": str(e)}), 500

@analyst.route("/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM Project WHERE projectId = %s", (project_id,))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "project deleted"}), 200
    except Error as e:
        current_app.logger.error(f"delete_project: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- Project dataset composition ----------------
@analyst.route("/projects/<int:project_id>/add/vitals", methods=["POST"])
def add_vitals_to_project(project_id):
    """
    Accept body with list of {vitalsId, patientId} entries to map into Project_Vitals.
    """
    try:
        payload = request.get_json() or {}
        items = payload.get("items", [])
        if not items:
            return jsonify({"error": "No items provided"}), 400

        cursor = db.get_db().cursor()
        for it in items:
            cursor.execute(
                "INSERT IGNORE INTO Project_Vitals (projectId, vitalsId, patientId) VALUES (%s, %s, %s)",
                (project_id, it["vitalsId"], it["patientId"])
            )
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "vitals added to project"}), 200
    except Error as e:
        current_app.logger.error(f"add_vitals_to_project: {e}")
        return jsonify({"error": str(e)}), 500

@analyst.route("/projects/<int:project_id>/add/labs", methods=["POST"])
def add_labs_to_project(project_id):
    try:
        payload = request.get_json() or {}
        items = payload.get("items", [])
        if not items:
            return jsonify({"error": "No items provided"}), 400
        cursor = db.get_db().cursor()
        for it in items:
            cursor.execute(
                "INSERT IGNORE INTO Project_Labs (projectId, labResultId, patientId) VALUES (%s, %s, %s)",
                (project_id, it["labResultId"], it["patientId"])
            )
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "labs added to project"}), 200
    except Error as e:
        current_app.logger.error(f"add_labs_to_project: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- LabResults: mark outliers / correct ----------------
@analyst.route("/labresults/<int:lab_id>", methods=["PUT"])
def update_lab_result(lab_id):
    """
    Update lab result fields (value, isOutlier, isModified)
    """
    try:
        data = request.get_json() or {}
        allowed = ["value", "isOutlier", "isModified", "date"]
        updates, params = [], []
        for a in allowed:
            if a in data:
                updates.append(f"{a} = %s")
                params.append(data[a])
        if not updates:
            return jsonify({"error": "No valid fields"}), 400
        params.append(lab_id)
        cursor = db.get_db().cursor()
        cursor.execute(f"UPDATE LabResult SET {', '.join(updates)} WHERE labResultId = %s", params)
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "lab result updated"}), 200
    except Error as e:
        current_app.logger.error(f"update_lab_result: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- Outlier detection helper ----------------
@analyst.route("/labresults/outliers", methods=["GET"])
def list_outliers():
    try:
        cursor = db.get_db().cursor(DictCursor)
        cursor.execute("SELECT * FROM LabResult WHERE isOutlier = TRUE OR isModified = TRUE ORDER BY date DESC")
        rows = cursor.fetchall()
        cursor.close()
        return jsonify(rows), 200
    except Error as e:
        current_app.logger.error(f"list_outliers: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- Missing Data checks ----------------
@analyst.route("/patients/missing", methods=["GET"])
def patients_with_missing():
    """
    Return patients missing key fields like DOB or status or without vitals/labs
    Query params:
      - check: 'demographics'|'vitals'|'labs'
    """
    try:
        check = request.args.get("check", "demographics")
        cursor = db.get_db().cursor(DictCursor)
        if check == "demographics":
            cursor.execute("SELECT * FROM Patient WHERE DOB IS NULL OR status IS NULL")
        elif check == "vitals":
            cursor.execute("""
                SELECT p.* FROM Patient p
                LEFT JOIN Vitals v ON p.patientId = v.patientId
                WHERE v.patientId IS NULL
            """)
        elif check == "labs":
            cursor.execute("""
                SELECT p.* FROM Patient p
                LEFT JOIN LabResult l ON p.patientId = l.patientId
                WHERE l.patientId IS NULL
            """)
        else:
            cursor.close()
            return jsonify({"error": "unknown check"}), 400

        rows = cursor.fetchall()
        cursor.close()
        return jsonify(rows), 200
    except Error as e:
        current_app.logger.error(f"patients_with_missing: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- Export project dataset ----------------
@analyst.route("/projects/<int:project_id>/export", methods=["GET"])
def export_project(project_id):
    """
    Export project lab results and vitals to CSV and return as string (for demo).
    In production, stream as file or S3 upload.
    """
    try:
        cursor = db.get_db().cursor(DictCursor)
        # labs in project
        cursor.execute("""
            SELECT l.* FROM LabResult l
            JOIN Project_Labs pl ON l.labResultId = pl.labResultId
            WHERE pl.projectId = %s
        """, (project_id,))
        labs = cursor.fetchall()
        # vitals in project
        cursor.execute("""
            SELECT v.* FROM Vitals v
            JOIN Project_Vitals pv ON v.vitalsId = pv.vitalsId AND v.patientId = pv.patientId
            WHERE pv.projectId = %s
        """, (project_id,))
        vitals = cursor.fetchall()
        cursor.close()

        # Build CSV in-memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["type", "value", "timestamp", "patientId", "source"])
        for r in labs:
            writer.writerow([r.get("labType"), r.get("value"), r.get("date"), r.get("patientId"), "lab"])
        for v in vitals:
            writer.writerow([v.get("type"), v.get("value"), v.get("timestamp"), v.get("patientId"), "vital"])

        csv_data = output.getvalue()
        return jsonify({"csv": csv_data}), 200
    except Error as e:
        current_app.logger.error(f"export_project: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- Visualizations ----------------
@analyst.route("/visualizations", methods=["POST"])
def create_visualization():
    try:
        data = request.get_json() or {}
        required = ["type", "dateCreated", "summary", "projectId"]
        for r in required:
            if r not in data:
                return jsonify({"error": f"Missing {r}"}), 400
        cursor = db.get_db().cursor()
        cursor.execute("INSERT INTO Visualization (type, dateCreated, summary, projectId) VALUES (%s, %s, %s, %s)",
                       (data["type"], data["dateCreated"], data["summary"], data["projectId"]))
        db.get_db().commit()
        vid = cursor.lastrowid
        cursor.close()
        return jsonify({"message": "visualization created", "visualizationId": vid}), 201
    except Error as e:
        current_app.logger.error(f"create_visualization: {e}")
        return jsonify({"error": str(e)}), 500

@analyst.route("/visualizations", methods=["GET"])
def list_visualizations():
    try:
        project_id = request.args.get("projectId")
        cursor = db.get_db().cursor(DictCursor)
        if project_id:
            cursor.execute("SELECT * FROM Visualization WHERE projectId = %s", (project_id,))
        else:
            cursor.execute("SELECT * FROM Visualization")
        rows = cursor.fetchall()
        cursor.close()
        return jsonify(rows), 200
    except Error as e:
        current_app.logger.error(f"list_visualizations: {e}")
        return jsonify({"error": str(e)}), 500
