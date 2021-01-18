from flask_wtf import FlaskForm
from wtforms.fields import SubmitField


class DownloadForm(FlaskForm):
    download = SubmitField('download')
