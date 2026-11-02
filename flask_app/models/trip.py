from datetime import date, datetime
from flask import flash
from flask_app.config.mysqlconnection import query

class Trip:
    def __init__(self, data):
        self.id = data.get("id")
        self.destination = data.get("destination")
        self.start_date = data.get("start_date")
        self.end_date = data.get("end_date")
        self.plan = data.get("plan")
        self.user_id = data.get("user_id")

    @classmethod
    def get_all_upcoming(cls):
        sql = """SELECT t.*, u.first_name AS organizer FROM trips t
                 JOIN users u ON u.id=t.user_id
                 WHERE t.start_date >= CURDATE() ORDER BY t.start_date ASC"""
        return query(sql)

    @classmethod
    def save(cls, data):
        sql = "INSERT INTO trips (destination, start_date, end_date, plan, user_id) VALUES (%s, %s, %s, %s, %s)"
        params = (data["destination"].strip(), data["start_date"], data["end_date"], data["plan"].strip(), data["user_id"])
        return query(sql, params)

    @classmethod
    def get_by_id(cls, trip_id):
        sql = """SELECT t.*, u.first_name AS organizer FROM trips t
                JOIN users u ON u.id=t.user_id WHERE t.id=%s"""
        return query(sql, (trip_id,), one=True)

    @classmethod
    def update(cls, data):
        sql = "UPDATE trips SET destination=%s, start_date=%s, end_date=%s, plan=%s WHERE id=%s"
        params = (data["destination"].strip(), data["start_date"], data["end_date"], data["plan"].strip(), data["id"])
        return query(sql, params)

    @classmethod
    def delete(cls, trip_id, user_id):
        sql = "DELETE FROM trips WHERE id=%s AND user_id=%s"
        return query(sql, (trip_id, user_id))

    @classmethod
    def get_travelers(cls, trip_id):
        sql = """SELECT u.id, u.first_name FROM travelers tr
                JOIN users u ON u.id=tr.user_id WHERE tr.trip_id=%s"""
        return query(sql, (trip_id,))

    @classmethod
    def add_traveler(cls, user_id, trip_id):
        sql = "INSERT IGNORE INTO travelers (user_id, trip_id) VALUES (%s, %s)"
        return query(sql, (user_id, trip_id))

    @classmethod
    def remove_traveler(cls, user_id, trip_id):
        sql = "DELETE FROM travelers WHERE user_id=%s AND trip_id=%s"
        return query(sql, (user_id, trip_id))

    @staticmethod
    def validate_trip(form):
        ok = True
        if not all(form.get(k, "").strip() for k in ("destination", "start_date", "end_date", "plan")):
            flash("Todos los campos son obligatorios.", "error")
            return False
        if len(form.get("plan", "")) > 40:
            flash("El itinerario no puede tener más de 40 caracteres.", "error")
            ok = False
        try:
            start = datetime.strptime(form["start_date"], "%Y-%m-%d").date()
            end = datetime.strptime(form["end_date"], "%Y-%m-%d").date()
        except ValueError:
            flash("Fechas inválidas.", "error")
            return False
        if start < date.today():
            flash("La fecha de inicio no puede ser en el pasado.", "error")
            ok = False
        if end <= start:
            flash("La fecha de fin debe ser después de la fecha de inicio.", "error")
            ok = False
        return ok
