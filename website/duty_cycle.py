from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import DutyCycle, Load, Project
from . import db

duty_cycle_blueprint = Blueprint('duty_cycle', __name__, template_folder='templates')
duty_cycle = 'projects.project_detail.duty_cycle'

from .operating_loads import operating_loads_blueprint
duty_cycle_blueprint.register_blueprint(operating_loads_blueprint, url_prefix='/<int:duty_cycle_id>/operating-load')

from .operating_schedule import operating_schedule_blueprint
duty_cycle_blueprint.register_blueprint(operating_schedule_blueprint, url_prefix='/<int:duty_cycle_id>/operating-schedule')

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

    return redirect(url_for('projects.project_detail.view_project', project_id=project_id))

# Retrieve a specific duty cycle and its loads
@duty_cycle_blueprint.route('/<int:duty_cycle_id>', methods=['GET'])
@login_required
def get_duty_cycle(project_id, duty_cycle_id):
    duty_cycle = DutyCycle.query.get_or_404(duty_cycle_id)
    if duty_cycle.project_id != project_id:
        flash('Duty cycle does not belong to the specified project.', 'error')
        return redirect(url_for('main.home'))
    #loads = Load.query.get_or_404(duty_cycle_id)
    loads = Load.query.all()
    for schedule in duty_cycle.schedules:
        schedule.current_load_ids = [load.id for load in schedule.loads]
    
    project = Project.query.get_or_404(project_id)

    breadcrumbs = [
        {'label': 'Home', 'url': url_for('main.home')},
        {'label': 'Projects', 'url': url_for('projects.project_list')},
        {'label': f'{project.name}', 'url': url_for('projects.project_detail.view_project', project_id=project_id)},
        {'label': f'{duty_cycle.name}', 'url': None}
    ]
    return render_template('duty_cycle.html', user=current_user, duty_cycle=duty_cycle, loads=loads, breadcrumbs=breadcrumbs)

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
    return redirect(url_for('projects.project_detail.view_project', project_id=project_id))