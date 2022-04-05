from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, TextAreaField
from wtforms.validators import DataRequired, Regexp
from flask_wtf.file import FileRequired, FileAllowed


	
class UpdateForm(FlaskForm):
	avatar = FileField('Change your avatar', validators = [FileAllowed(['jpg','jpeg','png'], 'Only pictures please')])
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(),Regexp(regex='^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$')])
	address = StringField('Address')
	phone_num = StringField('Phone number')
	name = StringField('Name')
	submit = SubmitField('Submit')

class ReviewForm(FlaskForm):
	title = StringField('TITLE', validators=[DataRequired()])
	text = TextAreaField('YOUR COMMENT ...', validators=[DataRequired()])
	send = SubmitField('SEND')
	

	
	
	
	



