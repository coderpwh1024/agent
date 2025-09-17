from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key'


class HelloForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')




@app.route('/', methods=['GET', 'POST'])
def hello():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        return f'Hello,{name}({email})!'
    return form.render_template()


@app.errorhandler(400)
def bad_request():
    return 'Bad Request', 400

if __name__ == '__main__':
    app.run(debug=True)





