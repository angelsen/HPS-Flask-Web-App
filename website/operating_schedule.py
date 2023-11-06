from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from .models import DutyCycle, Schedule, Load
from . import db
import datetime

operating_schedule_blueprint = Blueprint('operating_schedule', __name__)

# Route to handle adding a schedule
@operating_schedule_blueprint.route('/add', methods=['POST'])
@login_required
def add_schedule_to_duty_cycle(project_id, duty_cycle_id):
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    location = request.form.get('location')

    # Validate input
    if not start_time or not end_time:
        flash('Start and end times are required!', category='error')
    else:
        # Convert string time to datetime.time object
        start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
        end_time = datetime.datetime.strptime(end_time, '%H:%M').time()

        # Create and add new schedule to database
        new_schedule = Schedule(start_time=start_time, end_time=end_time, location=location, duty_cycle_id=duty_cycle_id)
        db.session.add(new_schedule)
        db.session.commit()
        flash('Schedule added!', category='success')

    return redirect(url_for('projects.project_detail.duty_cycle.get_duty_cycle', project_id=project_id, duty_cycle_id=duty_cycle_id))

# Route to handle deleting a schedule
@operating_schedule_blueprint.route('/<int:schedule_id>/delete', methods=['POST'])
@login_required
def delete_schedule(project_id, duty_cycle_id, schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    if schedule.duty_cycle_id != duty_cycle_id:
        flash('Schedule does not belong to the specified duty cycle.', category='error')
    else:
        db.session.delete(schedule)
        db.session.commit()
        flash('Schedule deleted!', category='success')

    return redirect(url_for('projects.project_detail.duty_cycle.get_duty_cycle', project_id=project_id, duty_cycle_id=duty_cycle_id))

# Route to handle adding multiple loads to a schedule
@operating_schedule_blueprint.route('/<int:schedule_id>/add_loads', methods=['POST'])
@login_required
def add_loads_to_schedule(project_id, duty_cycle_id, schedule_id):
    print(request.form)
    selected_load_ids = request.form.getlist('load_ids[]')
    schedule = Schedule.query.get(schedule_id)

    if schedule:
        # Clear existing loads and add new selections
        schedule.loads.clear()
        for load_id in selected_load_ids:
            load = Load.query.get(load_id)
            if load:
                schedule.loads.append(load)
        db.session.commit()
        flash('Schedule updated with selected loads!', category='success')
    else:
        flash('Invalid schedule!', category='error')

    return redirect(url_for('projects.project_detail.duty_cycle.get_duty_cycle', project_id=project_id, duty_cycle_id=duty_cycle_id))