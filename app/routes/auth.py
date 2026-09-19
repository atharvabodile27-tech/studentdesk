from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from ..models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["user"] = user.username
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for("main.dashboard"))

        flash("Galat username ya password.", "danger")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Aap logout ho gaye.", "info")
    return redirect(url_for("auth.login"))
