from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class CpetForm(Form):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    age = IntegerField('Age (years)', validators=[DataRequired()])
    bmi = IntegerField('BMI', validators=[DataRequired()])
    chronotropic = IntegerField('Chronotropic Response (HR)', validators=[DataRequired()])
    etco2 = IntegerField('End-Tidal CO2', validators=[DataRequired()])
    submit = SubmitField('Classify')