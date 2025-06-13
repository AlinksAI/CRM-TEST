from flask import Flask
from .config import Config
from .extensions import db, login_manager, csrf # Import csrf
from .models import User # Ensure User is imported

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app) # Initialize CSRF protection

    # Configure login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints here
    from .auth import auth_bp # Import the auth blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .main import main_bp # Import the main blueprint
    app.register_blueprint(main_bp) # Register main_bp, typically without a prefix for '/'

    from .customer import customer_bp # Import the customer blueprint
    app.register_blueprint(customer_bp) # Register customer_bp

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
