import unittest
from flask_login import current_user # Though not used directly in BaseTestCase, useful for debugging tests
from crm_app import create_app
from crm_app.extensions import db
from crm_app.models import User, Customer # Ensure Customer is imported if used in any test setup/teardown directly
from crm_app.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Use in-memory SQLite for tests
    WTF_CSRF_ENABLED = False # Disable CSRF for easier form testing in unit tests
    LOGIN_DISABLED = False # Ensure login is not disabled for tests needing authentication

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create a test user
        self.test_user = User(username='testuser', email='test@example.com')
        self.test_user.set_password('password123')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_test_user(self):
        # It's important that url_for is used within an app context if routes depend on app setup
        # or if it's used outside a request context in helper methods.
        # However, self.client.post operates within a request-like context.
        return self.client.post('/auth/login', data=dict(
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)

    def logout_test_user(self):
        return self.client.get('/auth/logout', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
