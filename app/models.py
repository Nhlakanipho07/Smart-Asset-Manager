from enum import Enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class HardDriveType(Enum):
    HDD = "HDD"
    SSD = "SSD"
    HYBRID = "HYBRID"


class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hard_drive_type = db.Column(db.Enum(HardDriveType), nullable=False)
    processor = db.Column(db.String(100), nullable=False)
    ram_amount = db.Column(db.Integer, nullable=False)
    maximum_ram = db.Column(db.Integer, nullable=False)
    hard_drive_space = db.Column(db.Integer, nullable=False)
    form_factor = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Computer {self.processor}>"
