"""
Test Module for Database Models.

This module contains tests for the database models used in the Expense
Tracker application. It verifies that models are correctly defined,
can be persisted to the database, and have proper default values.

Tests:
    test_expense_model: Tests the Expense model creation and retrieval.
    test_expense_default_date: Tests the default date assignment for expenses.
"""

from datetime import date, datetime

from flask import Flask

from app import Expense, db


def test_expense_model(app: Flask) -> None:
    """
    Test the Expense model creation and database operations.

    Verifies that:
    - An Expense can be created with all required fields
    - The expense is correctly persisted to the database
    - The expense can be retrieved with all fields intact
    - The __repr__ method returns the expected string format

    Args:
        app: The Flask application fixture.
    """
    with app.app_context():
        # Create a new expense
        expense = Expense(
            title='Test Model',
            amount=100.00,
            category='Test',
            date=datetime.strptime('2025-05-20', '%Y-%m-%d'),
            description='Test description'
        )

        # Add to database
        db.session.add(expense)
        db.session.commit()

        # Query the database
        queried_expense: Expense | None = Expense.query.filter_by(
            title='Test Model'
        ).first()

        # Check that the expense was created properly
        assert queried_expense is not None
        assert queried_expense.title == 'Test Model'
        assert queried_expense.amount == 100.00
        assert queried_expense.category == 'Test'
        assert queried_expense.date == datetime.strptime(
            '2025-05-20', '%Y-%m-%d'
        ).date()
        assert queried_expense.description == 'Test description'

        # Test __repr__ method
        assert repr(queried_expense) == '<Expense Test Model>'


def test_expense_default_date(app: Flask) -> None:
    """
    Test that the Expense model uses a default date when none is provided.

    Verifies that when an expense is created without specifying a date,
    the model automatically assigns a valid date (defaults to UTC now).

    Args:
        app: The Flask application fixture.
    """
    with app.app_context():
        # Create a new expense without a date
        expense = Expense(
            title='No Date Expense',
            amount=50.00,
            category='Test',
            description='No date provided'
        )

        # Add to database
        db.session.add(expense)
        db.session.commit()

        # Query the database
        queried_expense: Expense | None = Expense.query.filter_by(
            title='No Date Expense'
        ).first()

        # Check that a date was assigned
        assert queried_expense.date is not None
        # Since we don't know when the test will run, just verify it's a valid date
        assert isinstance(queried_expense.date, date)
