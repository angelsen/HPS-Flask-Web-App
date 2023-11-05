from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ...models import DutyCycle, Load
from ... import db

duty_cycle_blueprint = Blueprint('duty_cycle', __name__, template_folder='templates')
duty_cycle = 'projects.project_detail.duty_cycle'

duty_cycle_blueprint.endpoint()

# Create a new duty cycle within the project
@duty_cycle_blueprint.route('', methods=['POST'])
@login_required
def create_duty_cycle(project_id):
    duty_cycle_name = request.form.get('duty_cycle_name')
    if duty_cycle_name:
        new_duty_cycle = DutyCycle(name=duty_cycle_name, project_id=project_id)
        db.session.add(new_duty_cycle)
        db.session.commit()
        flash('Duty cycle added successfully!', 'success')
    else:
        flash('Duty cycle name is required!', 'error')
    return redirect(url_for('project.project_detail', project_id=project_id))

# Retrieve a specific duty cycle and its loads
@duty_cycle_blueprint.route('/<int:duty_cycle_id>', methods=['GET'])
@login_required
def get_duty_cycle(project_id, duty_cycle_id):
    duty_cycle = DutyCycle.query.get_or_404(duty_cycle_id)
    if duty_cycle.project_id != project_id:
        flash('Duty cycle does not belong to the specified project.', 'error')
        return redirect(url_for('main.home'))
    return render_template('duty_cycle.html', user=current_user, duty_cycle=duty_cycle)

# Delete a specific duty cycle
@duty_cycle_blueprint.route('/<int:duty_cycle_id>', methods=['POST', 'DELETE'])
@login_required
def delete_duty_cycle(project_id, duty_cycle_id):
    # Check if the hidden _method field is present and if its value is 'DELETE', or if the actual HTTP method is 'DELETE'
    if request.form.get('_method') == 'DELETE' or request.method == 'DELETE':
        duty_cycle = DutyCycle.query.get_or_404(duty_cycle_id)
        if duty_cycle.project_id != project_id:
            flash('Duty cycle does not belong to the specified project.', 'error')
            return redirect(url_for('main.home'))
        db.session.delete(duty_cycle)
        db.session.commit()
        flash('Duty cycle deleted!', 'success')
    return redirect(url_for('project.project_detail', project_id=project_id))

# Add a new load to a duty cycle
@duty_cycle_blueprint.route('/<int:duty_cycle_id>/load', methods=['POST'])
@login_required
def add_load_to_duty_cycle(project_id, duty_cycle_id):
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
    #return redirect(url_for('duty_cycle.get_duty_cycle', project_id=project_id, duty_cycle_id=duty_cycle_id))
    return redirect(url_for(f'{duty_cycle}.get_duty_cycle', project_id=project_id, duty_cycle_id=duty_cycle_id))

# Delete a specific load from a duty cycle
@duty_cycle_blueprint.route('/<int:duty_cycle_id>/load/<int:load_id>', methods=['POST', 'DELETE'])
@login_required
def delete_load(project_id, duty_cycle_id, load_id):
    # Check if the hidden _method field is present and if its value is 'DELETE', or if the actual HTTP method is 'DELETE'
    if request.form.get('_method') == 'DELETE' or request.method == 'DELETE':
        load = Load.query.get_or_404(load_id)
        if load.duty_cycle_id != duty_cycle_id:
            flash('Load does not belong to the specified duty cycle or project.', 'error')
            return redirect(url_for('main.home'))
        db.session.delete(load)
        db.session.commit()
        flash('Load deleted!', category='success')
    # Redirect to the duty cycle detail page
    return redirect(url_for(f'{duty_cycle}.get_duty_cycle', project_id=project_id, duty_cycle_id=duty_cycle_id))