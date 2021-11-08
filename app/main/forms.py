from wtforms import StringField,TextAreaField, SubmitField, SelectField
from wtforms.validators import Required
from flask_wtf import FlaskForm

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
    title = StringField('Pitch title', validators=[Required()])
    category = SelectField('Pitch category',choices=[('Choose category','Choose category'),('Pickup lines', 'Pickup lines'),('Interview','Interview'),('Product','Product'),('Promotions','Promotions')], validators=[Required()])
    comment = StringField('What is your idea?')
    submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):
    comment = TextAreaField('Comment on your idea', validators=[Required()])
    submit = SubmitField('Submit')

