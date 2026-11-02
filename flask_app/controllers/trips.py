from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.trip import Trip
from flask_app.controllers.users import login_required

@app.route("/dashboard")
@login_required
def dashboard():
    trips = Trip.get_all_upcoming()
    return render_template("dashboard.html", trips=trips)

@app.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        if Trip.validate_trip(request.form):
            data = dict(request.form)
            data["user_id"] = session["user_id"]
            Trip.save(data)
            return redirect("/dashboard")
        return render_template("form.html", title="Nuevo Viaje", action="/nuevo", trip=request.form)
    return render_template("form.html", title="Nuevo Viaje", action="/nuevo", trip={})

@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    trip = Trip.get_by_id(id)
    if not trip or trip["user_id"] != session["user_id"]:
        flash("Solo el organizador puede editar este viaje.", "error")
        return redirect("/dashboard")
    if request.method == "POST":
        if Trip.validate_trip(request.form):
            data = dict(request.form)
            data["id"] = id
            Trip.update(data)
            return redirect("/dashboard")
        return render_template("form.html", title="Editar Viaje", action=f"/editar/{id}", trip=request.form)
    return render_template("form.html", title="Editar Viaje", action=f"/editar/{id}", trip=trip)

@app.route("/borrar/<int:id>")
@login_required
def borrar(id):
    Trip.delete(id, session["user_id"])
    return redirect("/dashboard")

@app.route("/ver/<int:id>")
@login_required
def ver(id):
    trip = Trip.get_by_id(id)
    if not trip:
        return redirect("/dashboard")
    travelers = Trip.get_travelers(id)
    joined = any(t["id"] == session["user_id"] for t in travelers)
    return render_template("ver.html", trip=trip, travelers=travelers, joined=joined)

@app.route("/unirme/<int:id>")
@login_required
def unirme(id):
    Trip.add_traveler(session["user_id"], id)
    return redirect(f"/ver/{id}")

@app.route("/cancelar/<int:id>")
@login_required
def cancelar(id):
    Trip.remove_traveler(session["user_id"], id)
    return redirect(f"/ver/{id}")
