from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CpetForm(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Classify')