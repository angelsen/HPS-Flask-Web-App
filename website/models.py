from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Load(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    value = db.Column(db.Float)
    duty_cycle_id = db.Column(db.Integer, db.ForeignKey('duty_cycle.id'))

class DutyCycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    loads = db.relationship('Load', cascade="all, delete-orphan")
    schedules = db.relationship('Schedule', cascade="all, delete-orphan")
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    duty_cycles = db.relationship('DutyCycle')

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(150))
    duty_cycle_id = db.Column(db.Integer, db.ForeignKey('duty_cycle.id'))
    loads = db.relationship('Load', secondary='schedule_load', backref='schedules')

# Create an association table for many-to-many relationship between Schedule and Load
schedule_load = db.Table('schedule_load',
    db.Column('schedule_id', db.Integer, db.ForeignKey('schedule.id'), primary_key=True),
    db.Column('load_id', db.Integer, db.ForeignKey('load.id'), primary_key=True)
)