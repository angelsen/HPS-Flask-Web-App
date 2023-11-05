from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Project, DutyCycle, Load
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/projects', methods=['GET', 'POST'])
@login_required
def projects():
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        if project_name:
            new_project = Project(name=project_name)
            db.session.add(new_project)
            db.session.commit()
            flash('Project created successfully!', 'success')
            return redirect(url_for('views.projects'))
        else:
            flash('Project name is required!', 'error')

    all_projects = Project.query.all()
    return render_template('projects.html', user=current_user, projects=all_projects)

@views.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        if not project_name:
            flash('Project name is required!', category='error')
        else:
            new_project = Project(name=project_name)
            db.session.add(new_project)
            db.session.commit()
            flash('Project created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_project.html', user=current_user)

@views.route('/project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        duty_cycle_name = request.form.get('duty_cycle_name')
        if duty_cycle_name:
            new_duty_cycle = DutyCycle(name=duty_cycle_name, project_id=project.id)
            db.session.add(new_duty_cycle)
            db.session.commit()
            flash('Duty cycle added successfully!', 'success')
        else:
            flash('Duty cycle name is required!', 'error')
    return render_template('project_detail.html', user=current_user, project=project)

@views.route('/edit_duty_cycle/<int:duty_cycle_id>', methods=['GET', 'POST'])
@login_required
def edit_duty_cycle(duty_cycle_id):
    duty_cycle = DutyCycle.query.get_or_404(duty_cycle_id)
    # Handle the POST request if you want to allow editing duty cycle details
    return render_template('duty_cycle.html', user=current_user, duty_cycle=duty_cycle)

@views.route('/delete_duty_cycle/<int:duty_cycle_id>', methods=['POST'])
@login_required
def delete_duty_cycle(duty_cycle_id):
    duty_cycle = DutyCycle.query.get_or_404(duty_cycle_id)
    if duty_cycle:
        db.session.delete(duty_cycle)
        db.session.commit()
        flash('Duty cycle deleted!', 'success')
    else:
        flash('You do not have permission to delete this duty cycle.', 'error')
    return redirect(url_for('views.project_detail', user=current_user, project_id=duty_cycle.project_id))

@views.route('/add_duty_cycle/<int:project_id>', methods=['POST'])
@login_required
def add_duty_cycle(project_id):
    project = Project.query.get_or_404(project_id)
    duty_cycle_name = request.form.get('duty_cycle_name')
    if duty_cycle_name:
        new_duty_cycle = DutyCycle(name=duty_cycle_name, project_id=project.id)
        db.session.add(new_duty_cycle)
        db.session.commit()
        flash('Duty cycle added successfully!', 'success')
    else:
        flash('Duty cycle name is required!', 'error')
    return redirect(url_for('views.project_detail', project_id=project.id))

@views.route('/duty_cycle/<int:duty_cycle_id>', methods=['GET', 'POST'])
@login_required
def duty_cycle(duty_cycle_id):
    duty_cycle = DutyCycle.query.get_or_404(duty_cycle_id)
    if request.method == 'POST':
        load_name = request.form.get('load_name')
        load_value = request.form.get('load_value')

        if not load_name or not load_value:
            flash('Load name and value are required!', category='error')
        else:
            try:
                load_value = float(load_value)  # Convert the string to a float
                new_load = Load(name=load_name, value=load_value, duty_cycle_id=duty_cycle_id)
                db.session.add(new_load)
                db.session.commit()
                flash('Load added!', category='success')
            except ValueError:
                flash('Please enter a valid number for the load value.', category='error')

    # Retrieve the updated duty cycle to include new loads
    duty_cycle = DutyCycle.query.get_or_404(duty_cycle_id)
    return render_template('duty_cycle.html', user=current_user, duty_cycle=duty_cycle)

@views.route('/delete_load/<int:load_id>', methods=['POST'])
@login_required
def delete_load(load_id):
    load = Load.query.get_or_404(load_id)
    if load:
        duty_cycle_id = load.duty_cycle_id  # Save duty_cycle_id before deleting the load
        db.session.delete(load)
        db.session.commit()
        flash('Load deleted!', category='success')
        return redirect(url_for('views.duty_cycle', duty_cycle_id=duty_cycle_id))
    else:
        flash('Load not found or you do not have permission to delete it.', category='error')
        # Redirect to a default page if no load found or not authorized
        return redirect(url_for('views.projects'))