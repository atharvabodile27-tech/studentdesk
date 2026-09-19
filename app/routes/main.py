from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy import or_

from ..models import db, Student

main_bp = Blueprint("main", __name__)


def login_required(view):
    """Chhota sa decorator - bina login ke pages nahi khulenge."""
    from functools import wraps

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


@main_bp.route("/")
@login_required
def dashboard():
    students = Student.query.all()
    total = len(students)
    active = sum(1 for s in students if s.status == "Active")
    passed = sum(1 for s in students if s.result() == "PASS")
    avg_marks = round(sum(s.marks for s in students) / total, 2) if total else 0
    pass_rate = round((passed / total) * 100, 1) if total else 0

    courses = {}
    for s in students:
        courses[s.course] = courses.get(s.course, 0) + 1

    return render_template(
        "dashboard.html",
        total=total, active=active, passed=passed,
        avg_marks=avg_marks, pass_rate=pass_rate,
        courses=courses, recent=sorted(students, key=lambda x: x.id, reverse=True)[:5],
    )


@main_bp.route("/students")
@login_required
def student_list():
    q = request.args.get("q", "").strip()
    course = request.args.get("course", "").strip()

    query = Student.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Student.name.ilike(like), Student.roll_no.ilike(like), Student.email.ilike(like)))
    if course:
        query = query.filter(Student.course == course)

    students = query.order_by(Student.roll_no).all()
    all_courses = [c[0] for c in db.session.query(Student.course).distinct().all()]
    return render_template("students.html", students=students, q=q, course=course, all_courses=all_courses)


@main_bp.route("/students/new", methods=["GET", "POST"])
@login_required
def student_add():
    if request.method == "POST":
        try:
            marks = float(request.form.get("marks", 0))
            year = int(request.form.get("year", 1))
        except ValueError:
            flash("Marks aur Year numbers hone chahiye.", "danger")
            return render_template("student_form.html", student=None)

        if not (0 <= marks <= 100):
            flash("Marks 0 se 100 ke beech hone chahiye.", "danger")
            return render_template("student_form.html", student=None)

        roll_no = request.form.get("roll_no", "").strip()
        email = request.form.get("email", "").strip()

        if Student.query.filter_by(roll_no=roll_no).first():
            flash("Ye Roll Number pehle se exist karta hai.", "danger")
            return render_template("student_form.html", student=None)
        if Student.query.filter_by(email=email).first():
            flash("Ye Email pehle se registered hai.", "danger")
            return render_template("student_form.html", student=None)

        s = Student(
            roll_no=roll_no,
            name=request.form.get("name", "").strip(),
            email=email,
            course=request.form.get("course", "").strip(),
            year=year,
            marks=marks,
            status=request.form.get("status", "Active"),
        )
        db.session.add(s)
        db.session.commit()
        flash(f"Student {s.name} add ho gaya.", "success")
        return redirect(url_for("main.student_list"))

    return render_template("student_form.html", student=None)


@main_bp.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def student_edit(student_id):
    s = db.get_or_404(Student, student_id)
    if request.method == "POST":
        try:
            s.marks = float(request.form.get("marks", s.marks))
            s.year = int(request.form.get("year", s.year))
        except ValueError:
            flash("Marks aur Year numbers hone chahiye.", "danger")
            return render_template("student_form.html", student=s)

        s.name = request.form.get("name", s.name).strip()
        s.email = request.form.get("email", s.email).strip()
        s.course = request.form.get("course", s.course).strip()
        s.status = request.form.get("status", s.status)
        db.session.commit()
        flash("Details update ho gayi.", "success")
        return redirect(url_for("main.student_list"))

    return render_template("student_form.html", student=s)


@main_bp.route("/students/<int:student_id>/delete", methods=["POST"])
@login_required
def student_delete(student_id):
    s = db.get_or_404(Student, student_id)
    db.session.delete(s)
    db.session.commit()
    flash(f"{s.name} delete kar diya gaya.", "warning")
    return redirect(url_for("main.student_list"))
