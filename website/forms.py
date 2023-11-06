from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class NoteForm(FlaskForm):
    note = TextAreaField('Note', validators=[DataRequired(), Length(min=1, message='Note is too short!')])
    submit = SubmitField('Add Note')