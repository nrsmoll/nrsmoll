from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, InputRequired

class CpetForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    age = IntegerField('Age (years)', validators=[InputRequired(),
                                                  NumberRange(min=0, max=110, message='Age between 0 and 110 years')
                                                  ])
    bmi = IntegerField('BMI', validators=[DataRequired()])
    chronotropic = IntegerField('Chronotropic Response (HR)', validators=[DataRequired()])
    etco2 = IntegerField('End-Tidal CO2', validators=[DataRequired()])
    submit = SubmitField('Classify')