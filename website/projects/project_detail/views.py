from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ... models import Project, DutyCycle
from ... import db

project_detail = Blueprint('project_detail', __name__, template_folder='templates')

from . duty_cycle.views import duty_cycle_blueprint
project_detail.register_blueprint(duty_cycle_blueprint, url_prefix='/duty-cycle')

@project_detail.route('', methods=['GET', 'POST'])
@login_required
def view_project(project_id):
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