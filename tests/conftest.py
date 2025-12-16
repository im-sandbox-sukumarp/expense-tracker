"""
Pytest Configuration and Fixtures for Expense Tracker Tests.

This module provides pytest fixtures that set up the test environment,
including a configured Flask application instance, test client, and
CLI runner. It also creates a temporary SQLite database with sample
data for testing.

Fixtures:
    app: A configured Flask application instance for testing.
    client: A test client for making HTTP requests.
    runner: A CLI runner for testing command-line commands.

Example:
    Using the client fixture in a test::

        def test_index(client):
            response = client.get('/')
            assert response.status_code == 200
"""

import os
import sys
import tempfile
from datetime import datetime
from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

# Add the parent directory to sys.path to import the app
parent_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

# Import here to avoid circular imports
import app as flask_app_module
from app import db, Expense


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    """
    Create and configure a Flask application instance for testing.

    This fixture creates a temporary SQLite database file and configures
    the Flask application for testing. It pre-populates the database with
    sample expense records for use in tests.

    Yields:
        Flask: A configured Flask application instance with a test database
            containing sample expenses.

    Sample Data:
        The fixture creates three sample expenses:
        - Grocery Shopping: $150.75 (Food category)
        - Electric Bill: $87.30 (Utilities category)
        - Movie Tickets: $35.50 (Entertainment category)

    Cleanup:
        After the test completes, the temporary database file is closed
        and removed.

    Example:
        Using the app fixture::

            def test_database(app):
                with app.app_context():
                    expenses = Expense.query.all()
                    assert len(expenses) == 3
    """
    # Create a temporary file to isolate the database for each test
    db_fd: int
    db_path: str
    db_fd, db_path = tempfile.mkstemp()

    test_app: Flask = flask_app_module.app
    test_app.config['TESTING'] = True
    test_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    test_app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    # Create the database and the tables
    with test_app.app_context():
        db.create_all()

        # Add some sample data
        sample_expenses: list[Expense] = [
            Expense(
                title='Grocery Shopping',
                amount=150.75,
                category='Food',
                date=datetime.strptime('2025-05-01', '%Y-%m-%d'),
                description='Weekly groceries'
            ),
            Expense(
                title='Electric Bill',
                amount=87.30,
                category='Utilities',
                date=datetime.strptime('2025-05-05', '%Y-%m-%d'),
                description='Monthly electricity bill'
            ),
            Expense(
                title='Movie Tickets',
                amount=35.50,
                category='Entertainment',
                date=datetime.strptime('2025-05-10', '%Y-%m-%d'),
                description='Weekend movie'
            )
        ]

        for expense in sample_expenses:
            db.session.add(expense)

        db.session.commit()

    yield test_app

    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """
    Create a test client for making HTTP requests.

    This fixture provides a test client that can be used to make HTTP
    requests to the Flask application without running a server.

    Args:
        app: The Flask application fixture.

    Returns:
        FlaskClient: A test client instance for the Flask application.

    Example:
        Using the client fixture::

            def test_get_index(client):
                response = client.get('/')
                assert response.status_code == 200

            def test_post_expense(client):
                response = client.post('/add', data={'title': 'Test'})
                assert response.status_code == 302
    """
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    """
    Create a test CLI runner for testing command-line commands.

    This fixture provides a CLI runner that can be used to test
    Flask CLI commands.

    Args:
        app: The Flask application fixture.

    Returns:
        FlaskCliRunner: A CLI runner instance for the Flask application.

    Example:
        Using the runner fixture::

            def test_cli_command(runner):
                result = runner.invoke(args=['my-command'])
                assert result.exit_code == 0
    """
    return app.test_cli_runner()
