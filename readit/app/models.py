from datetime import datetime
from flask import g

class User(g.db.Model):
    id = g.db.Column(g.db.Integer, primary_key=True)