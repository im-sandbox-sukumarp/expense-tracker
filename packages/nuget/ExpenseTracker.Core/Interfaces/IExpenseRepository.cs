using ExpenseTracker.Core.Models;

namespace ExpenseTracker.Core.Interfaces;

/// <summary>
/// Repository interface for expense operations
/// </summary>
public interface IExpenseRepository
{
    /// <summary>
    /// Get all expenses
    /// </summary>
    Task<IEnumerable<Expense>> GetAllAsync();

    /// <summary>
    /// Get an expense by its ID
    /// </summary>
    Task<Expense?> GetByIdAsync(Guid id);

    /// <summary>
    /// Get expenses by category
    /// </summary>
    Task<IEnumerable<Expense>> GetByCategoryAsync(string category);

    /// <summary>
    /// Get expenses within a date range
    /// </summary>
    Task<IEnumerable<Expense>> GetByDateRangeAsync(DateTime startDate, DateTime endDate);

    /// <summary>
    /// Add a new expense
    /// </summary>
    Task<Expense> AddAsync(Expense expense);

    /// <summary>
    /// Update an existing expense
    /// </summary>
    Task<Expense> UpdateAsync(Expense expense);

    /// <summary>
    /// Delete an expense
    /// </summary>
    Task<bool> DeleteAsync(Guid id);

    /// <summary>
    /// Get category summaries
    /// </summary>
    Task<IEnumerable<CategorySummary>> GetCategorySummariesAsync();
}

/// <summary>
/// Repository interface for category operations
/// </summary>
public interface ICategoryRepository
{
    /// <summary>
    /// Get all categories
    /// </summary>
    Task<IEnumerable<Category>> GetAllAsync();

    /// <summary>
    /// Get a category by its ID
    /// </summary>
    Task<Category?> GetByIdAsync(Guid id);

    /// <summary>
    /// Get a category by name
    /// </summary>
    Task<Category?> GetByNameAsync(string name);

    /// <summary>
    /// Add a new category
    /// </summary>
    Task<Category> AddAsync(Category category);

    /// <summary>
    /// Update an existing category
    /// </summary>
    Task<Category> UpdateAsync(Category category);

    /// <summary>
    /// Delete a category
    /// </summary>
    Task<bool> DeleteAsync(Guid id);
}
