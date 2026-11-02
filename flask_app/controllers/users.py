from functools import wraps
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión.", "error")
            return redirect("/")
        return f(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("index.html", form=request.args)

@app.route("/register", methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect("/")
    user_id = User.save(request.form)
    session["user_id"] = user_id
    session["name"] = request.form["first_name"].strip()
    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login():
    user = User.validate_login(request.form)
    if not user:
        return redirect("/")
    session["user_id"] = user["id"]
    session["name"] = user["first_name"]
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
