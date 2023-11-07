from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required
from .models import Location
from . import db
import json

location_blueprint = Blueprint('location', __name__)

@location_blueprint.route('')
@login_required
def manage_locations():
    # Fetch all locations from the database
    locations = Location.query.all()
    # Render the location.html template, passing in the locations
    return render_template('location.html', locations=locations)

# Route to handle adding a location
@location_blueprint.route('/add', methods=['POST'])
@login_required
def add_location():
    name = request.form.get('name')
    description = request.form.get('description')
    parameters = request.form.get('parameters')

    try:
        # Attempt to parse the parameters as JSON
        parameters_dict = json.loads(parameters)
    except json.JSONDecodeError:
        flash('Invalid JSON format for parameters.', 'error')
        return jsonify({'error': 'Invalid JSON format for parameters.'}), 400

    # Create and add new location to database
    new_location = Location(name=name, description=description, parameters=parameters_dict)
    db.session.add(new_location)
    db.session.commit()

    # Render the partial _location.html with the new location
    return render_template('partials/_location.html', location=new_location)

# Route to handle deleting a location
@location_blueprint.route('/<int:location_id>/delete', methods=['POST'])
@login_required
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    return '', 200  # No content to return