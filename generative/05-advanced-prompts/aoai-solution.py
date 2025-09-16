from flask import Flask, request
from flask_wtf import  FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key'

