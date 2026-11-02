from flask import Flask

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-secreta"

from flask_app.controllers import users, trips
