from flask_wtf import Form
from wtforms import Form, StringField, TextAreaField, IntegerField, SelectField, SelectMultipleField, validators
from wtforms.fields.html5 import DateField

from wtforms.validators import DataRequired

# from .models import Openhour

class OpenhourForm(Form):
    # choices = volunteer_query()
    # choices=[('none', 'none')]
    # author = SelectField('Author', choices=choices)
    # author = StringField('Name')
    # author = QuerySelectField(query_factory=volunteer_query, allow_blank=True)
    date = DateField('Date', format='%Y-%m-%d')
    volunteers = StringField('Volunteers')
    shoppers = StringField('Shoppers')
    # volunteers = SelectField('Volunteer', coerce=int)
    # volunteers = SelectMultipleField('Volunteers', coerce=int)
    # shoppers = SelectMultipleField('Shoppers', coerce=int)
