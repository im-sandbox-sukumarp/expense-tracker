"""
Test Module for HTTP Routes and API Endpoints.

This module contains tests for all HTTP routes in the Expense Tracker
application, including both web interface routes and API endpoints.
Tests cover GET and POST requests, successful operations, and error
handling for non-existent resources.

Tests:
    test_index_route: Tests the main index page.
    test_add_expense_get: Tests the add expense form display.
    test_add_expense_post: Tests adding a new expense.
    test_edit_expense_get: Tests the edit expense form display.
    test_edit_expense_post: Tests updating an expense.
    test_delete_expense: Tests deleting an expense.
    test_categories_route: Tests the categories summary page.
    test_api_expenses: Tests the JSON API endpoint.
    test_non_existent_expense_edit: Tests 404 handling for edit.
    test_non_existent_expense_delete: Tests 404 handling for delete.
"""

from typing import Any

from flask import Flask
from flask.testing import FlaskClient


def test_index_route(client: FlaskClient) -> None:
    """
    Test that the index route displays expenses correctly.

    Verifies that:
    - The index page returns a 200 status code
    - The page contains expected content (expenses list)

    Args:
        client: The Flask test client fixture.
    """
    response = client.get('/')
    assert response.status_code == 200
    # Test if the page loads - look for key elements that should be there
    assert b'Expenses' in response.data


def test_add_expense_get(client: FlaskClient) -> None:
    """
    Test the GET request to the add expense page.

    Verifies that:
    - The add page returns a 200 status code
    - The page contains the form and expected headers

    Args:
        client: The Flask test client fixture.
    """
    response = client.get('/add')
    assert response.status_code == 200
    assert b'Add New Expense' in response.data
    assert b'<form' in response.data


def test_add_expense_post(client: FlaskClient, app: Flask) -> None:
    """
    Test adding a new expense via POST request.

    Verifies that:
    - The form submission redirects successfully
    - A success flash message is displayed
    - The expense data appears on the index page
    - The expense is correctly saved to the database

    Args:
        client: The Flask test client fixture.
        app: The Flask application fixture.
    """
    response = client.post('/add', data={
        'title': 'Test Expense',
        'amount': '75.50',
        'category': 'Test Category',
        'date': '2025-05-15',
        'description': 'This is a test expense'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Expense added successfully!' in response.data
    assert b'Test Expense' in response.data
    assert b'$75.50' in response.data
    assert b'Test Category' in response.data

    # Verify expense was added to database
    with app.app_context():
        from app import Expense
        expense: Expense | None = Expense.query.filter_by(
            title='Test Expense'
        ).first()
        assert expense is not None
        assert expense.amount == 75.50
        assert expense.category == 'Test Category'
        assert expense.description == 'This is a test expense'


def test_edit_expense_get(client: FlaskClient) -> None:
    """
    Test the GET request to edit an expense.

    Verifies that:
    - The edit page returns a 200 status code
    - The form is pre-populated with existing expense data

    Args:
        client: The Flask test client fixture.
    """
    # Get the first expense (id=1)
    response = client.get('/edit/1')
    assert response.status_code == 200
    assert b'Edit Expense' in response.data
    assert b'Grocery Shopping' in response.data
    assert b'150.75' in response.data


def test_edit_expense_post(client: FlaskClient, app: Flask) -> None:
    """
    Test editing an expense via POST request.

    Verifies that:
    - The form submission redirects successfully
    - A success flash message is displayed
    - The updated data appears on the index page
    - The expense is correctly updated in the database

    Args:
        client: The Flask test client fixture.
        app: The Flask application fixture.
    """
    response = client.post('/edit/1', data={
        'title': 'Updated Grocery Shopping',
        'amount': '160.25',
        'category': 'Food',
        'date': '2025-05-01',
        'description': 'Updated grocery description'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Expense updated successfully!' in response.data
    assert b'Updated Grocery Shopping' in response.data

    # Verify expense was updated in database
    with app.app_context():
        from app import Expense
        expense: Expense | None = Expense.query.filter_by(id=1).first()
        assert expense.title == 'Updated Grocery Shopping'
        assert expense.amount == 160.25
        assert expense.description == 'Updated grocery description'


def test_delete_expense(client: FlaskClient, app: Flask) -> None:
    """
    Test deleting an expense.

    Verifies that:
    - The delete request redirects successfully
    - A success flash message is displayed
    - The expense is removed from the database

    Args:
        client: The Flask test client fixture.
        app: The Flask application fixture.
    """
    response = client.get('/delete/2', follow_redirects=True)
    assert response.status_code == 200
    assert b'Expense deleted successfully!' in response.data

    # Verify expense was deleted from database
    with app.app_context():
        from app import Expense
        expense: Expense | None = Expense.query.filter_by(id=2).first()
        assert expense is None


def test_categories_route(client: FlaskClient) -> None:
    """
    Test the categories summary page.

    Verifies that:
    - The categories page returns a 200 status code
    - The page displays category names from the test data

    Args:
        client: The Flask test client fixture.
    """
    response = client.get('/categories')
    assert response.status_code == 200
    assert b'Expense Categories' in response.data or b'Categories' in response.data
    assert b'Food' in response.data
    assert b'Entertainment' in response.data


def test_api_expenses(client: FlaskClient) -> None:
    """
    Test the API endpoint for retrieving expenses as JSON.

    Verifies that:
    - The API returns a 200 status code
    - The response is valid JSON
    - The response is a list of expense objects
    - Each expense object contains all required fields

    Args:
        client: The Flask test client fixture.
    """
    response = client.get('/api/expenses')
    assert response.status_code == 200

    # Check that response is JSON
    data: list[dict[str, Any]] = response.get_json()
    assert isinstance(data, list)

    # Check the first expense data
    assert (
        data[0]['title'] == 'Grocery Shopping'
        or data[2]['title'] == 'Grocery Shopping'
    )

    # Make sure all expenses have the required fields
    for expense in data:
        assert 'id' in expense
        assert 'title' in expense
        assert 'amount' in expense
        assert 'category' in expense
        assert 'date' in expense
        assert 'description' in expense


def test_non_existent_expense_edit(client: FlaskClient) -> None:
    """
    Test accessing a non-existent expense for editing.

    Verifies that requesting to edit an expense that doesn't exist
    returns a 404 Not Found status code.

    Args:
        client: The Flask test client fixture.
    """
    response = client.get('/edit/999')
    assert response.status_code == 404


def test_non_existent_expense_delete(client: FlaskClient) -> None:
    """
    Test deleting a non-existent expense.

    Verifies that requesting to delete an expense that doesn't exist
    returns a 404 Not Found status code.

    Args:
        client: The Flask test client fixture.
    """
    response = client.get('/delete/999')
    assert response.status_code == 404
