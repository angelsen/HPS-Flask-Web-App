from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .. models import Project
from .. import db

projects = Blueprint('projects', __name__, template_folder='templates')

from . project_detail.views import project_detail
projects.register_blueprint(project_detail, url_prefix='/<int:project_id>')


@projects.route('', methods=['GET', 'POST'])
@login_required
def project_list():
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        if not project_name:
            flash('Project name is required!', category='error')
        else:
            new_project = Project(name=project_name)
            db.session.add(new_project)
            db.session.commit()
            flash('Project created successfully!', category='success')
            # Stay on the same page after creating the project
            return redirect(url_for('projects.project_list'))

    all_projects = Project.query.all()
    return render_template('projects.html', user=current_user, projects=all_projects)
