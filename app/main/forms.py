from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class AnswerForm(FlaskForm):
    performance_rating = FloatField('Performance rating', validators=[NumberRange(min=0.0, max=1.0)])
    body = TextAreaField('Answer', validators=[DataRequired()])
    submit = SubmitField('Answer')


class TopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Topic body', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')