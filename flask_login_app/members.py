from flask import (
    Blueprint, render_template
)
from flask_login import login_required
from .db import get_engine, get_session


db_engine = get_engine()
db_session = get_session()

bp = Blueprint('members', __name__, url_prefix='/members')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('members.html')

