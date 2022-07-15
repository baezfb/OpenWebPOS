from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    """
    Form for adding/editing categories.
    """
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    description = StringField('Description', validators=[Length(max=255)])
    image = FileField('Image')
    submit = SubmitField('Submit')
