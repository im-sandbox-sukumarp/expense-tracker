"""
Test Module for Application Setup and Configuration.

This module contains tests that verify the Flask application is correctly
configured, including database settings, secret key configuration, and
route registration.

Tests:
    test_app_config: Verifies application configuration settings.
    test_app_routes_registered: Verifies all expected routes are registered.
"""

from flask import Flask


def test_app_config(app: Flask) -> None:
    """
    Test that the application is configured correctly for testing.

    Verifies the following configuration settings:
    - TESTING mode is enabled
    - SQLite database is being used
    - SQLAlchemy modifications tracking is disabled
    - Secret key is set correctly

    Args:
        app: The Flask application fixture.
    """
    assert app.config['TESTING'] is True
    assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False
    assert app.secret_key == 'expense_tracker_secret_key'


def test_app_routes_registered(app: Flask) -> None:
    """
    Test that all necessary routes are registered with the application.

    Verifies that the following routes are available:
    - / (index page)
    - /add (add expense)
    - /edit/<int:id> (edit expense)
    - /delete/<int:id> (delete expense)
    - /categories (category breakdown)
    - /api/expenses (JSON API endpoint)

    Args:
        app: The Flask application fixture.
    """
    routes: list[str] = [rule.rule for rule in app.url_map.iter_rules()]

    # Check that all expected routes are registered
    assert '/' in routes
    assert '/add' in routes
    assert '/edit/<int:id>' in routes
    assert '/delete/<int:id>' in routes
    assert '/categories' in routes
    assert '/api/expenses' in routes
