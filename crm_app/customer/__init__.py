from flask import Blueprint

customer_bp = Blueprint('customer',
                        __name__,
                        template_folder='templates',
                        url_prefix='/customers')

from . import routes
