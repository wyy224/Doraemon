from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField
from wtforms.validators import DataRequired, Regexp
from flask_wtf.file import FileRequired, FileAllowed


	
class UpdateForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(),Regexp(regex='^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$')])
	address = StringField('Address', validators=[DataRequired()])
	phone_num = StringField('Phone number', validators=[DataRequired()])
	name = StringField('Name', validators=[DataRequired()])
	submit = SubmitField('Submit')
	

	
	
	
	



