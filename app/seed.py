"""
Sample data (seed) - pehli baar app chalane par 6 students + 1 admin user add ho jayenge.

NOTE (race-safety): gunicorn jaise multi-worker servers pe har worker alag process
me create_app() chalata hai. Agar do workers ek saath seed karein to UNIQUE
constraint violation hota hai. Isliye har commit ko try/except se guard kiya
hai: jo worker race haar jaye wo chup-chaap rollback kar deta hai, kyunki
data jeetne wale worker ne pehle se daal diya hota hai.
"""
from sqlalchemy.exc import IntegrityError

from .models import db, Student, User

SAMPLE_STUDENTS = [
    ("CS2021001", "Aarav Sharma",   "aarav.sharma@example.com",   "B.Tech CSE", 3, 88.5, "Active"),
    ("CS2021002", "Diya Patel",     "diya.patel@example.com",     "B.Tech CSE", 3, 92.0, "Active"),
    ("EC2022014", "Rohan Deshmukh", "rohan.d@example.com",        "B.Tech ECE", 2, 74.5, "Active"),
    ("MC2023007", "Sneha Kulkarni", "sneha.k@example.com",        "MCA",        1, 65.0, "Active"),
    ("ME2020031", "Kabir Joshi",    "kabir.joshi@example.com",    "B.Tech ME",  4, 41.0, "Graduated"),
    ("CS2024009", "Ananya Iyer",    "ananya.iyer@example.com",    "B.Tech CSE", 1, 96.5, "Active"),
]


def _safe_commit():
    """Commit karo; race condition me IntegrityError aaye to rollback kar do."""
    try:
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False


def seed_if_empty():
    if Student.query.count() == 0:
        for row in SAMPLE_STUDENTS:
            db.session.add(Student(
                roll_no=row[0], name=row[1], email=row[2],
                course=row[3], year=row[4], marks=row[5], status=row[6],
            ))
        _safe_commit()

    if User.query.filter_by(username="admin").first() is None:
        admin = User(username="admin")
        admin.set_password("admin123")   # demo password - production me kabhi mat karna
        db.session.add(admin)
        _safe_commit()