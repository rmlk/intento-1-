import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash
from flask_app.config.mysqlconnection import query

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

class User:
    def __init__(self, data):
        self.id = data.get("id")
        self.first_name = data.get("first_name")
        self.last_name = data.get("last_name")
        self.email = data.get("email")
        self.password = data.get("password")
        self.created_at = data.get("created_at")

    @classmethod
    def save(cls, data):
        sql = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        params = (data["first_name"].strip(), data["last_name"].strip(), data["email"], generate_password_hash(data["password"]))
        return query(sql, params)

    @classmethod
    def get_by_email(cls, email):
        sql = "SELECT * FROM users WHERE email=%s"
        return query(sql, (email,), one=True)

    @classmethod
    def get_by_id(cls, user_id):
        sql = "SELECT * FROM users WHERE id=%s"
        return query(sql, (user_id,), one=True)

    @staticmethod
    def validate_register(form):
        ok = True
        if len(form.get("first_name", "").strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "error")
            ok = False
        if len(form.get("last_name", "").strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "error")
            ok = False
        if not EMAIL_RE.match(form.get("email", "")):
            flash("El email no tiene un formato válido.", "error")
            ok = False
        elif User.get_by_email(form.get("email")):
            flash("Ese email ya está registrado.", "error")
            ok = False
        if len(form.get("password", "")) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error")
            ok = False
        if form.get("password") != form.get("confirm"):
            flash("La contraseña y la confirmación deben ser iguales.", "error")
            ok = False
        return ok

    @staticmethod
    def validate_login(form):
        user = User.get_by_email(form.get("email"))
        if not user:
            flash("El email no está registrado.", "error")
            return None
        if not check_password_hash(user["password"], form.get("password", "")):
            flash("La contraseña es incorrecta.", "error")
            return None
        return user
