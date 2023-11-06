from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from .forms import NoteForm  # Make sure to import your form

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', methods=['GET'])
@login_required
def home():
    form = NoteForm()  # Instantiate your form
    return render_template("home.html", user=current_user, form=form)

@main.route('/add-note', methods=['POST'])
@login_required
def add_note():
    form = NoteForm()  # Instantiate your form
    if form.validate_on_submit():
        new_note = Note(data=form.note.data, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        #flash('Note added!', category='success')
        # Render and return the new note as a list item
        return render_template("partials/_note.html", note=new_note), 200
    # If validation fails, return the form errors
    return jsonify(form.errors), 400

@main.route('/delete-note', methods=['POST'])
def delete_note():
    noteId = request.form.get('noteId')
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return '', 200  # No Content response is appropriate here