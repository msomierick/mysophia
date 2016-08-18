from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import get_faculties


class StudentForm(Form):
    surname = StringField(
        u'Surname Name:', validators=[InputRequired(), Length(max=20)])
    first_name = StringField(
        u'First Name:', validators=[InputRequired(), Length(max=20)])
    second_name = StringField(
        u'Second Name:', validators=[InputRequired(), Length(max=20)])
    email = StringField(
        u'Email:', validators=[InputRequired(), Length(max=50), Email()])
    admin_no = StringField(
        u'Admin No:', validators=[InputRequired(), Length(max=20)])
    phone_no = StringField(
        u'Phone no:', validators=[InputRequired(), Length(max=20)])
    faculty = QuerySelectField('Faculty/School', query_factory=get_faculties)
    submit = SubmitField('Submit')
