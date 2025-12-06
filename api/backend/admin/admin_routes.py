# backend/admin/admin_routes.py
from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from pymysql.cursors import DictCursor  
from pymysql import Error    

admin = Blueprint("admin", __name__)


# ---------------- Roles / Permissions ----------------

@admin.route("/roles", methods=["GET"])
def get_roles():
    try:
        cursor = db.get_db().cursor(DictCursor)
        cursor.execute("SELECT * FROM Role")
        roles = cursor.fetchall()
        cursor.close()
        return jsonify(roles), 200
    except Error as e:
        current_app.logger.error(f"get_roles: {e}")
        return jsonify({"error": str(e)}), 500

@admin.route("/roles", methods=["POST"])
def create_role():
    try:
        data = request.get_json() or {}
        required = ["roleId", "name", "description", "permissionId"]
        for r in required:
            if r not in data:
                return jsonify({"error": f"Missing {r}"}), 400

        cursor = db.get_db().cursor()
        cursor.execute(
            "INSERT INTO Role (roleId, name, description, permissionId) VALUES (%s, %s, %s, %s)",
            (data["roleId"], data["name"], data["description"], data["permissionId"])
        )
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "role created"}), 201
    except Error as e:
        current_app.logger.error(f"create_role: {e}")
        return jsonify({"error": str(e)}), 500

@admin.route("/roles/<int:role_id>", methods=["PUT"])
def update_role(role_id):
    try:
        data = request.get_json() or {}
        allowed = ["name", "description", "permissionId"]
        updates, params = [], []
        for a in allowed:
            if a in data:
                updates.append(f"{a} = %s")
                params.append(data[a])

        if not updates:
            return jsonify({"error": "No valid fields"}), 400

        params.append(role_id)
        cursor = db.get_db().cursor()
        cursor.execute(f"UPDATE Role SET {', '.join(updates)} WHERE roleId = %s", params)
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "role updated"}), 200
    except Error as e:
        current_app.logger.error(f"update_role: {e}")
        return jsonify({"error": str(e)}), 500

# Permissions CRUD
@admin.route("/permissions", methods=["GET"])
def get_permissions():
    try:
        cursor = db.get_db().cursor(DictCursor)
        cursor.execute("SELECT * FROM Permission")
        perms = cursor.fetchall()
        cursor.close()
        return jsonify(perms), 200
    except Error as e:
        current_app.logger.error(f"get_permissions: {e}")
        return jsonify({"error": str(e)}), 500

@admin.route("/permissions", methods=["POST"])
def create_permission():
    try:
        data = request.get_json() or {}
        required = ["permissionId", "action", "resource"]
        for r in required:
            if r not in data:
                return jsonify({"error": f"Missing {r}"}), 400

        cursor = db.get_db().cursor()
        cursor.execute(
            "INSERT INTO Permission (permissionId, action, resource) VALUES (%s, %s, %s)",
            (data["permissionId"], data["action"], data["resource"])
        )
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "permission created"}), 201
    except Error as e:
        current_app.logger.error(f"create_permission: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- Staff (User Provisioning) ----------------
@admin.route("/staff", methods=["GET"])
def list_staff():
    try:
        cursor = db.get_db().cursor(DictCursor)
        cursor.execute("SELECT * FROM Staff")
        staff = cursor.fetchall()
        cursor.close()
        return jsonify(staff), 200
    except Error as e:
        current_app.logger.error(f"list_staff: {e}")
        return jsonify({"error": str(e)}), 500

@admin.route("/staff", methods=["POST"])
def create_staff():
    try:
        data = request.get_json() or {}
        required = ["name", "email", "status"]
        for r in required:
            if r not in data:
                return jsonify({"error": f"Missing {r}"}), 400

        cursor = db.get_db().cursor()
        cursor.execute("INSERT INTO Staff (name, email, status) VALUES (%s, %s, %s)",
                       (data["name"], data["email"], data["status"]))
        db.get_db().commit()
        new_id = cursor.lastrowid
        cursor.close()
        return jsonify({"message": "staff created", "staffId": new_id}), 201
    except Error as e:
        current_app.logger.error(f"create_staff: {e}")
        return jsonify({"error": str(e)}), 500

@admin.route("/staff/<int:staff_id>", methods=["PUT"])
def update_staff(staff_id):
    try:
        data = request.get_json() or {}
        allowed = ["name", "email", "status"]
        updates, params = [], []
        for a in allowed:
            if a in data:
                updates.append(f"{a} = %s")
                params.append(data[a])
        if not updates:
            return jsonify({"error": "No valid fields"}), 400
        params.append(staff_id)
        cursor = db.get_db().cursor()
        cursor.execute(f"UPDATE Staff SET {', '.join(updates)} WHERE staffId = %s", params)
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "staff updated"}), 200
    except Error as e:
        current_app.logger.error(f"update_staff: {e}")
        return jsonify({"error": str(e)}), 500

@admin.route("/staff/<int:staff_id>", methods=["DELETE"])
def delete_staff(staff_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("DELETE FROM Staff WHERE staffId = %s", (staff_id,))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "staff deleted"}), 200
    except Error as e:
        current_app.logger.error(f"delete_staff: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- Audit Logs ----------------
@admin.route("/auditlogs", methods=["GET"])
def get_audit_logs():
    try:
        cursor = db.get_db().cursor(DictCursor)
        cursor.execute("SELECT * FROM AuditLog ORDER BY timeStamp DESC LIMIT 1000")
        logs = cursor.fetchall()
        cursor.close()
        return jsonify(logs), 200
    except Error as e:
        current_app.logger.error(f"get_audit_logs: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- Integrations ----------------
@admin.route("/integrations", methods=["GET"])
def list_integrations():
    try:
        cursor = db.get_db().cursor(DictCursor)
        cursor.execute("SELECT * FROM Integration")
        ints = cursor.fetchall()
        cursor.close()
        return jsonify(ints), 200
    except Error as e:
        current_app.logger.error(f"list_integrations: {e}")
        return jsonify({"error": str(e)}), 500

@admin.route("/integrations", methods=["POST"])
def create_integration():
    try:
        data = request.get_json() or {}
        required = ["systemName", "status", "lastSyncDate", "departmentId"]
        for r in required:
            if r not in data:
                return jsonify({"error": f"Missing {r}"}), 400
        cursor = db.get_db().cursor()
        cursor.execute(
            "INSERT INTO Integration (systemName, status, lastSyncDate, departmentId) VALUES (%s, %s, %s, %s)",
            (data["systemName"], data["status"], data["lastSyncDate"], data["departmentId"])
        )
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "integration created"}), 201
    except Error as e:
        current_app.logger.error(f"create_integration: {e}")
        return jsonify({"error": str(e)}), 500

@admin.route("/integrations/<int:int_id>", methods=["PUT"])
def update_integration(int_id):
    try:
        data = request.get_json() or {}
        allowed = ["systemName", "status", "lastSyncDate", "departmentId"]
        updates, params = [], []
        for a in allowed:
            if a in data:
                updates.append(f"{a} = %s")
                params.append(data[a])
        if not updates:
            return jsonify({"error": "No valid fields"}), 400
        params.append(int_id)
        cursor = db.get_db().cursor()
        cursor.execute(f"UPDATE Integration SET {', '.join(updates)} WHERE integrationId = %s", params)
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "integration updated"}), 200
    except Error as e:
        current_app.logger.error(f"update_integration: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------- System Health & Security Alerts ----------------
@admin.route("/system/health", methods=["GET"])
def system_health():
    try:
        # Example: return counts and last sync times; adapt with real metrics
        cursor = db.get_db().cursor(DictCursor)
        cursor.execute("SELECT COUNT(*) AS staff_count FROM Staff")
        staff_count = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) AS active_patients FROM Patient WHERE status = 'active'")
        patient_count = cursor.fetchone()
        cursor.execute("SELECT MAX(lastSyncDate) AS last_integration_sync FROM Integration")
        last_sync = cursor.fetchone()
        cursor.close()
        return jsonify({"staff_count": staff_count, "active_patients": patient_count, "last_integration_sync": last_sync}), 200
    except Error as e:
        current_app.logger.error(f"system_health: {e}")
        return jsonify({"error": str(e)}), 500

@admin.route("/alerts/system", methods=["GET"])
def system_alerts():
    try:
        cursor = db.get_db().cursor(DictCursor)
        cursor.execute("SELECT * FROM SystemAlert ORDER BY timestamp DESC LIMIT 200")
        alerts = cursor.fetchall()
        cursor.close()
        return jsonify(alerts), 200
    except Error as e:
        current_app.logger.error(f"system_alerts: {e}")
        return jsonify({"error": str(e)}), 500
