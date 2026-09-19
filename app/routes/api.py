"""
JSON REST API - Jenkins ke API tests aur monitoring ke liye useful.
"""
from flask import Blueprint, jsonify, request

from ..models import db, Student

api_bp = Blueprint("api", __name__)


@api_bp.route("/students", methods=["GET"])
def api_list_students():
    students = Student.query.order_by(Student.id).all()
    return jsonify({"count": len(students), "students": [s.to_dict() for s in students]})


@api_bp.route("/students/<int:student_id>", methods=["GET"])
def api_get_student(student_id):
    s = db.get_or_404(Student, student_id)
    return jsonify(s.to_dict())


@api_bp.route("/students", methods=["POST"])
def api_create_student():
    data = request.get_json(silent=True) or {}
    required = ["roll_no", "name", "email", "course", "year", "marks"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        marks = float(data["marks"])
        year = int(data["year"])
    except (TypeError, ValueError):
        return jsonify({"error": "marks aur year numeric hone chahiye"}), 400

    if not (0 <= marks <= 100):
        return jsonify({"error": "marks 0-100 range me hone chahiye"}), 400

    if Student.query.filter_by(roll_no=data["roll_no"]).first():
        return jsonify({"error": "roll_no already exists"}), 409
    if Student.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "email already exists"}), 409

    s = Student(
        roll_no=data["roll_no"], name=data["name"], email=data["email"],
        course=data["course"], year=year, marks=marks,
        status=data.get("status", "Active"),
    )
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201


@api_bp.route("/students/<int:student_id>", methods=["DELETE"])
def api_delete_student(student_id):
    s = db.get_or_404(Student, student_id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"deleted": student_id}), 200


@api_bp.route("/stats", methods=["GET"])
def api_stats():
    students = Student.query.all()
    total = len(students)
    return jsonify({
        "total_students": total,
        "active": sum(1 for s in students if s.status == "Active"),
        "pass_count": sum(1 for s in students if s.result() == "PASS"),
        "average_marks": round(sum(s.marks for s in students) / total, 2) if total else 0,
    })
