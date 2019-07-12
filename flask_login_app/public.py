from flask import (
    Blueprint, render_template
)


bp = Blueprint('public', __name__, url_prefix='/public')


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

