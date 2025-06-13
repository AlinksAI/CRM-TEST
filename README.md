# Simple CRM Application

A basic Customer Relationship Management (CRM) application built with Python and Flask.

## Features

*   User Authentication:
    *   User registration
    *   User login and logout
    *   Password hashing for security
    *   User profile viewing and editing
*   Customer Management:
    *   CRUD operations (Create, Read, Update, Delete) for customer records.
    *   Customers are associated with the user who created them.
    *   Users can only view and manage their own customer records.
*   Basic Styling: Clean and simple interface for usability.
*   Unit Tests: Coverage for core authentication and CRM functionalities.

## Project Structure

*   `crm_app/`: Main application package.
    *   `app.py`: Flask application factory (`create_app`) and main run script.
    *   `config.py`: Configuration settings.
    *   `extensions.py`: Flask extension initializations (SQLAlchemy, LoginManager, CSRFProtect).
    *   `models.py`: SQLAlchemy database models (User, Customer).
    *   `forms.py`: WTForms definitions.
    *   `static/`: Static files (CSS).
    *   `templates/`: HTML templates.
    *   `auth/`: Blueprint for authentication routes and templates.
    *   `main/`: Blueprint for main routes (home, profile) and templates.
    *   `customer/`: Blueprint for CRM (customer) routes and templates.
    *   `tests/`: Unit test files.
*   `requirements.txt`: Project dependencies.
*   `run_tests.py`: Script to execute unit tests.
*   `README.md`: This file.

## Setup and Installation

### Prerequisites

*   Python 3.7+
*   pip (Python package installer)
*   Virtual environment tool (e.g., `venv`)

### Installation Steps

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    # venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup:**
    The database and tables will be created automatically when you first run the application. The application uses SQLite by default, creating an `app.db` file (as per current `config.py`) in the `crm_app` directory instance folder (or alongside `config.py` if instance folder is not explicitly used for db path).
    *Note: The current `config.py` places `app.db` in the same directory as `config.py`.*


### Running the Application

To run the Flask development server (from the project root directory):

```bash
python -m crm_app.app
```

The application will typically be available at `http://127.0.0.1:5000/`.

*Alternative using Flask CLI (from project root directory):*
```bash
export FLASK_APP=crm_app:create_app
# On Windows: set FLASK_APP=crm_app:create_app
flask run
```
*Make sure your `FLASK_APP` environment variable points to the application factory if you use this method.*

## Running Unit Tests

To run the unit tests, execute the following command from the project root directory:

```bash
python run_tests.py
```

This will discover and run all tests in the `crm_app/tests` directory.
