from wtforms import Form, StringField, SelectField, validators, PasswordField, SubmitField, DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Regexp, Email

class CreateUserForm(Form):
    first_name = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('', [validators.DataRequired()], choices=[('', 'Select Gender'), ('F', 'Female'), ('M', 'Male')], default='')
    username = StringField('', [validators.Length(min=1, max=10), validators.DataRequired()])
    email = StringField('', [validators.Length(min=3, max=150), validators.DataRequired()])
    password = PasswordField('', [validators.Length(min=8, max=150), validators.DataRequired()])


class CreateListingForm(Form):
    title = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    brand = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    category = SelectField('', [validators.DataRequired()], choices=[('', 'Select Category'),
                                                                             ('Grains', 'Grains'), ('Canned Foods', 'Canned Foods'),
                                                                             ('Dairy', 'Dairy'),
                                                                             ('Fruits & Vegetables', 'Fruits & Vegetables'),
                                                                             ('Beverages', 'Beverages')], default='')
    expiry_date = DateField('', format='%Y-%m-%d')
    location = StringField('', [validators.length(max=200), validators.DataRequired()])
    description = StringField('', [validators.Optional()])

class LoginForm(FlaskForm):
    username = StringField('', [validators.Length(min=1, max=10), validators.DataRequired()])
    password = PasswordField('', [validators.Length(min=8, max=150), validators.DataRequired()])
    submit = SubmitField("Login")

class CreateReviewForm(Form): 
    review = StringField('Write a review...', [validators.length(max=2000), validators.DataRequired()]) 
    rating = SelectField('Your Donor Rating:', choices=[('Very Dissatisfied'), ( 'Dissatisfied'), ('Satisfied'), ('Very Satisfied')])