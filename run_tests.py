import unittest
import os
import sys

if __name__ == '__main__':
    # This script assumes it's in the project root, and crm_app is a subdirectory.
    # Add crm_app's parent directory to sys.path to allow crm_app imports
    # This makes `from crm_app import ...` work.
    project_root = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, project_root)

    # It's also common to add the app directory itself if tests are structured like:
    # from crm_app.tests.base import ...
    # In this case, the current structure should work if crm_app is discoverable.
    # If crm_app is not directly in PYTHONPATH, the following might be needed:
    # sys.path.insert(0, os.path.join(project_root, 'crm_app'))


    loader = unittest.TestLoader()

    # Discover tests in the 'crm_app/tests' directory
    # The start_dir should be relative to the project root where run_tests.py is.
    start_dir = os.path.join(project_root, 'crm_app', 'tests')

    # Check if the directory exists, useful for debugging path issues
    if not os.path.isdir(start_dir):
        print(f"Error: Test directory not found at {start_dir}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Is 'crm_app/tests' a valid path from here?")
        sys.exit(1)

    print(f"Looking for tests in: {start_dir}")
    suite = loader.discover(start_dir, pattern='test_*.py')

    if suite.countTestCases() == 0:
        print(f"No tests found in {start_dir} with pattern 'test_*.py'.")
        # List files to help debug:
        try:
            print(f"Files in {start_dir}: {os.listdir(start_dir)}")
            # Also check one level up if structure is different
            # print(f"Files in {os.path.dirname(start_dir)}: {os.listdir(os.path.dirname(start_dir))}")
        except FileNotFoundError:
            print(f"{start_dir} or its parent does not exist.")

        sys.exit(1)


    runner = unittest.TextTestRunner(verbosity=2) # Increased verbosity
    result = runner.run(suite)

    # Exit with a non-zero status if tests failed
    if not result.wasSuccessful():
        sys.exit(1)
