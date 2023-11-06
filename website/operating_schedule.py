from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required
from .models import DutyCycle, Schedule, Load
from . import db
import datetime
from dateutil import parser

operating_schedule_blueprint = Blueprint('operating_schedule', __name__)

# Route to handle adding a schedule
@operating_schedule_blueprint.route('/add', methods=['POST'])
@login_required
def add_schedule_to_duty_cycle(project_id, duty_cycle_id):
    dates = request.form.get('dates')
    start_time_str, end_time_str = dates.split(' - ')
    start_time = parser.parse(start_time_str)
    end_time = parser.parse(end_time_str)
    
    location = request.form.get('location')

    duty_cycle = DutyCycle.query.get(duty_cycle_id)

    # Create and add new schedule to database
    new_schedule = Schedule(start_time=start_time, end_time=end_time, location=location, duty_cycle_id=duty_cycle_id)
    db.session.add(new_schedule)
    db.session.commit()
    
    # Render the partial _operating_schedule.html with the new schedule
    return render_template('partials/_operating_schedule.html', schedule=new_schedule, loads=Load.query.all(), duty_cycle=duty_cycle)

# Route to handle deleting a schedule
@operating_schedule_blueprint.route('/<int:schedule_id>/delete', methods=['POST'])
@login_required
def delete_schedule(project_id, duty_cycle_id, schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    if schedule.duty_cycle_id != duty_cycle_id:
        return jsonify({'error': 'Schedule does not belong to the specified duty cycle.'}), 400
    else:
        db.session.delete(schedule)
        db.session.commit()
        return '', 200  # No content to return

# Route to handle adding multiple loads to a schedule
@operating_schedule_blueprint.route('/<int:schedule_id>/add_loads', methods=['POST'])
@login_required
def add_loads_to_schedule(project_id, duty_cycle_id, schedule_id):
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
        # Render the partial _operating_schedule.html with the updated schedule
        #return render_template('partials/_operating_schedule.html', schedule=schedule, loads=Load.query.all())
        return '', 204
    else:
        return jsonify({'error': 'Invalid schedule!'}), 400