from flask_wtf import FlaskForm
from wtforms import StringField, FileField, DecimalField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

from openwebpos.blueprints.pos.models import Category


def get_categories():
    return Category.query.filter_by(active=True).all()


class CategoryForm(FlaskForm):
    """
    Form for adding/editing categories.
    """
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    description = StringField('Description', validators=[Length(max=255)])
    image = FileField('Image')
    submit = SubmitField('Submit')


class ItemForm(FlaskForm):
    """
    Form for adding/editing items.
    """
    categories = SelectField('Category', coerce=int, validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    description = StringField('Description', validators=[Length(max=255)])
    image = FileField('Image')
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')
