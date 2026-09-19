"""
Database models (SQLAlchemy ORM).
Student + User tables.
"""
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    course = db.Column(db.String(50), nullable=False)     # B.Tech / MCA / MBA ...
    year = db.Column(db.Integer, nullable=False)           # 1,2,3,4
    marks = db.Column(db.Float, nullable=False, default=0) # percentage 0-100
    status = db.Column(db.String(20), default="Active")    # Active / Inactive / Graduated
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def grade(self):
        """Marks se grade calculate karna - ye hum unit test karenge."""
        m = self.marks
        if m >= 90:
            return "A+"
        if m >= 80:
            return "A"
        if m >= 70:
            return "B"
        if m >= 60:
            return "C"
        if m >= 50:
            return "D"
        if m >= 40:
            return "E"
        return "F"

    def result(self):
        return "PASS" if self.marks >= 40 else "FAIL"

    def to_dict(self):
        return {
            "id": self.id,
            "roll_no": self.roll_no,
            "name": self.name,
            "email": self.email,
            "course": self.course,
            "year": self.year,
            "marks": self.marks,
            "grade": self.grade(),
            "result": self.result(),
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Student {self.roll_no} {self.name}>"


class User(db.Model):
    """Simple admin login."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
