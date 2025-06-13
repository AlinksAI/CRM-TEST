from flask import Blueprint

# We specify template_folder to point to the main 'templates' directory
# one level up from 'crm_app/auth', if auth-specific templates are there.
# Or, if templates are in 'crm_app/templates/auth', it would be template_folder='templates'
# For simplicity with the current instructions, assuming auth templates (login.html, register.html)
# will reside in the main `crm_app/templates` directory.
auth_bp = Blueprint('auth', __name__, template_folder='../templates')

from . import routes  # Import routes after blueprint creation to avoid circular dependency
