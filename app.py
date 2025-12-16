"""
Expense Tracker Application.

A Flask-based web application for tracking personal expenses. This module
provides the main application setup, database models, and route handlers
for managing expenses including creating, reading, updating, and deleting
expense records.

Attributes:
    app (Flask): The Flask application instance.
    db (SQLAlchemy): The SQLAlchemy database instance.
    basedir (str): The absolute path to the application directory.

Example:
    To run the application::

        $ python app.py

    The application will be available at http://localhost:5000
"""

from typing import Any

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
)
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app
app: Flask = Flask(__name__)
app.secret_key = 'expense_tracker_secret_key'

# Configure database
basedir: str = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'expenses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db: SQLAlchemy = SQLAlchemy(app)


class Expense(db.Model):
    """
    SQLAlchemy model representing an expense record.

    This model stores information about individual expenses including
    the title, amount, category, date, and optional description.

    Attributes:
        id (int): The unique identifier for the expense (primary key).
        title (str): The title or name of the expense (max 100 characters).
        amount (float): The monetary amount of the expense.
        category (str): The category of the expense (max 50 characters).
        date (datetime.date): The date of the expense. Defaults to current UTC date.
        description (str, optional): Additional details about the expense.

    Example:
        Creating a new expense::

            expense = Expense(
                title='Grocery Shopping',
                amount=150.75,
                category='Food',
                date=datetime.strptime('2025-05-01', '%Y-%m-%d'),
                description='Weekly groceries'
            )
            db.session.add(expense)
            db.session.commit()
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)

    def __repr__(self) -> str:
        """
        Return a string representation of the Expense instance.

        Returns:
            str: A string in the format '<Expense {title}>'.
        """
        return f'<Expense {self.title}>'

# Routes
@app.route('/')
def index() -> str:
    """
    Render the home page displaying all expenses.

    Retrieves all expenses from the database, ordered by date in descending
    order (most recent first), and calculates the total amount spent.

    Returns:
        str: Rendered HTML template for the index page containing the list
            of expenses and total amount.
    """
    expenses: list[Any] = Expense.query.order_by(Expense.date.desc()).all()
    total_amount: float = sum(expense.amount for expense in expenses)
    return render_template('index.html', expenses=expenses, total_amount=total_amount)


@app.route('/add', methods=['GET', 'POST'])
def add() -> str | Response:
    """
    Handle the add expense page and form submission.

    For GET requests, renders the form to add a new expense.
    For POST requests, processes the form data and creates a new expense
    record in the database.

    Returns:
        str | Response: For GET requests, returns rendered HTML template.
            For successful POST requests, redirects to the index page.

    Form Fields:
        title (str): The title of the expense.
        amount (str): The monetary amount (converted to float).
        category (str): The expense category.
        date (str): The expense date in 'YYYY-MM-DD' format.
        description (str, optional): Additional details about the expense.
    """
    if request.method == 'POST':
        title: str | None = request.form.get('title')
        amount: float = float(request.form.get('amount'))
        category: str | None = request.form.get('category')
        date_str: str | None = request.form.get('date')
        description: str | None = request.form.get('description')

        date: datetime = (
            datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.utcnow()
        )

        expense = Expense(
            title=title,
            amount=amount,
            category=category,
            date=date,
            description=description
        )

        db.session.add(expense)
        db.session.commit()

        flash('Expense added successfully!', 'success')
        return redirect(url_for('index'))

    # Pass today's date to the template
    return render_template('add.html', now=datetime.utcnow())


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id: int) -> str | Response:
    """
    Handle the edit expense page and form submission.

    For GET requests, renders the form populated with the existing expense data.
    For POST requests, updates the expense record with the new data.

    Args:
        id: The unique identifier of the expense to edit.

    Returns:
        str | Response: For GET requests, returns rendered HTML template
            with the expense form. For successful POST requests, redirects
            to the index page.

    Raises:
        404: If no expense with the given ID exists.

    Form Fields:
        title (str): The updated title of the expense.
        amount (str): The updated monetary amount (converted to float).
        category (str): The updated expense category.
        date (str): The updated expense date in 'YYYY-MM-DD' format.
        description (str, optional): Updated description.
    """
    expense: Expense = Expense.query.get_or_404(id)

    if request.method == 'POST':
        expense.title = request.form.get('title')
        expense.amount = float(request.form.get('amount'))
        expense.category = request.form.get('category')
        date_str: str | None = request.form.get('date')
        expense.date = (
            datetime.strptime(date_str, '%Y-%m-%d') if date_str else expense.date
        )
        expense.description = request.form.get('description')

        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit.html', expense=expense)


@app.route('/delete/<int:id>')
def delete(id: int) -> Response:
    """
    Delete an expense record from the database.

    Retrieves the expense by ID and removes it from the database.
    Displays a flash message upon successful deletion.

    Args:
        id: The unique identifier of the expense to delete.

    Returns:
        Response: Redirects to the index page after deletion.

    Raises:
        404: If no expense with the given ID exists.
    """
    expense: Expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'danger')
    return redirect(url_for('index'))


@app.route('/categories')
def categories() -> str:
    """
    Render the categories page with expense breakdown by category.

    Retrieves all expenses and aggregates the total amount spent
    per category for visualization.

    Returns:
        str: Rendered HTML template displaying category totals
            and visualization.
    """
    expenses: list[Any] = Expense.query.all()
    categories_dict: dict[str, float] = {}

    for expense in expenses:
        if expense.category in categories_dict:
            categories_dict[expense.category] += expense.amount
        else:
            categories_dict[expense.category] = expense.amount

    return render_template('categories.html', categories=categories_dict)


@app.route('/api/expenses')
def api_expenses() -> Response:
    """
    Return all expenses as a JSON API response.

    Retrieves all expenses from the database, ordered by date in
    descending order, and returns them as a JSON array.

    Returns:
        Response: JSON response containing a list of expense objects.
            Each object contains: id, title, amount, category, date,
            and description.

    Example Response:
        [
            {
                "id": 1,
                "title": "Grocery Shopping",
                "amount": 150.75,
                "category": "Food",
                "date": "2025-05-01",
                "description": "Weekly groceries"
            }
        ]
    """
    expenses: list[Any] = Expense.query.order_by(Expense.date.desc()).all()
    result: list[dict[str, Any]] = []

    for expense in expenses:
        result.append({
            'id': expense.id,
            'title': expense.title,
            'amount': expense.amount,
            'category': expense.category,
            'date': expense.date.strftime('%Y-%m-%d'),
            'description': expense.description
        })

    return jsonify(result)


# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)