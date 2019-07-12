from flask import (
    Blueprint, render_template
)
from flask_login import login_required


bp = Blueprint('members', __name__, url_prefix='/members')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('members.html')

