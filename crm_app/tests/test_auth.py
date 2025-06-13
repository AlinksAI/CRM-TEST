from crm_app.tests.base import BaseTestCase, db
from crm_app.models import User
from flask import url_for # Import url_for

class AuthTestCase(BaseTestCase):

    def test_registration_page_loads(self):
        response = self.client.get(url_for('auth.register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_user_registration(self):
        # Ensure the app context is active for url_for
        with self.app.app_context():
            response = self.client.post(url_for('auth.register'), data=dict(
                username='newuser',
                email='new@example.com',
                password='newpassword',
                confirm_password='newpassword'
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created! You are now able to log in.', response.data)
        user = User.query.filter_by(email='new@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'newuser')

    def test_login_page_loads(self):
        with self.app.app_context():
            response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_user_login_logout(self):
        # Login - uses helper which implicitly handles url_for context via client
        response = self.login_test_user()
        self.assertEqual(response.status_code, 200)

        # Check for flash message and presence of Logout link
        # Depending on how flash messages are rendered and session handling in tests,
        # it might be tricky to catch them reliably without specific test configurations.
        # For now, we check if the page content indicates a successful login (e.g., Logout link).
        self.assertIn(b'Login successful!', response.data) # Check for flash message
        self.assertIn(b'Logout', response.data) # Logout link should be visible

        # Logout
        response = self.logout_test_user()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out.', response.data) # Check for flash message
        self.assertIn(b'Login', response.data) # Login link should be visible again
        self.assertNotIn(b'Logout', response.data) # Logout link should not be visible

    def test_login_with_invalid_credentials(self):
        with self.app.app_context():
            response = self.client.post(url_for('auth.login'), data=dict(
                email='test@example.com',
                password='wrongpassword'
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200) # Stays on login page
        self.assertIn(b'Login Unsuccessful. Please check email and password.', response.data)
        self.assertIn(b'Login', response.data) # Still on login page
        self.assertNotIn(b'Logout', response.data)

    def test_access_profile_when_not_logged_in(self):
        with self.app.app_context():
            response = self.client.get(url_for('main.profile'), follow_redirects=True)
        # Should redirect to login page
        self.assertIn(b'Login', response.data) # Check if it's the login page
        self.assertIn(b'Please log in to access this page.', response.data) # Default Flask-Login message

    def test_access_profile_when_logged_in(self):
        self.login_test_user()
        with self.app.app_context():
            response = self.client.get(url_for('main.profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Profile', response.data)
        self.assertIn(b'testuser', response.data) # Username of logged-in user
        self.logout_test_user() # Clean up session
