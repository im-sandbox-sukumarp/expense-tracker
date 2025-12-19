using ExpenseTracker.Core.Interfaces;
using ExpenseTracker.Core.Models;

namespace ExpenseTracker.Services;

/// <summary>
/// Service for managing expenses
/// </summary>
public class ExpenseService : IExpenseService
{
    private readonly IExpenseRepository _expenseRepository;
    private readonly ICategoryRepository _categoryRepository;

    public ExpenseService(
        IExpenseRepository expenseRepository,
        ICategoryRepository categoryRepository)
    {
        _expenseRepository = expenseRepository;
        _categoryRepository = categoryRepository;
    }

    /// <inheritdoc />
    public async Task<IEnumerable<Expense>> GetAllExpensesAsync()
    {
        return await _expenseRepository.GetAllAsync();
    }

    /// <inheritdoc />
    public async Task<Expense?> GetExpenseByIdAsync(Guid id)
    {
        return await _expenseRepository.GetByIdAsync(id);
    }

    /// <inheritdoc />
    public async Task<Expense> CreateExpenseAsync(CreateExpenseRequest request)
    {
        // Validate category exists
        var category = await _categoryRepository.GetByNameAsync(request.Category);
        if (category == null)
        {
            throw new ArgumentException($"Category '{request.Category}' does not exist.");
        }

        var expense = new Expense
        {
            Amount = request.Amount,
            Category = request.Category,
            Description = request.Description,
            Date = request.Date
        };

        return await _expenseRepository.AddAsync(expense);
    }

    /// <inheritdoc />
    public async Task<Expense> UpdateExpenseAsync(Guid id, UpdateExpenseRequest request)
    {
        var expense = await _expenseRepository.GetByIdAsync(id);
        if (expense == null)
        {
            throw new ArgumentException($"Expense with ID '{id}' not found.");
        }

        if (request.Amount.HasValue)
            expense.Amount = request.Amount.Value;
        
        if (!string.IsNullOrEmpty(request.Category))
            expense.Category = request.Category;
        
        if (!string.IsNullOrEmpty(request.Description))
            expense.Description = request.Description;
        
        if (request.Date.HasValue)
            expense.Date = request.Date.Value;

        expense.UpdatedAt = DateTime.UtcNow;

        return await _expenseRepository.UpdateAsync(expense);
    }

    /// <inheritdoc />
    public async Task<bool> DeleteExpenseAsync(Guid id)
    {
        return await _expenseRepository.DeleteAsync(id);
    }

    /// <inheritdoc />
    public async Task<IEnumerable<Expense>> GetExpensesByDateRangeAsync(DateTime startDate, DateTime endDate)
    {
        return await _expenseRepository.GetByDateRangeAsync(startDate, endDate);
    }

    /// <inheritdoc />
    public async Task<IEnumerable<CategorySummary>> GetCategorySummariesAsync()
    {
        return await _expenseRepository.GetCategorySummariesAsync();
    }

    /// <inheritdoc />
    public async Task<decimal> GetTotalExpensesAsync()
    {
        var expenses = await _expenseRepository.GetAllAsync();
        return expenses.Sum(e => e.Amount);
    }

    /// <inheritdoc />
    public async Task<decimal> GetTotalExpensesByCategoryAsync(string category)
    {
        var expenses = await _expenseRepository.GetByCategoryAsync(category);
        return expenses.Sum(e => e.Amount);
    }
}

/// <summary>
/// Service interface for expense operations
/// </summary>
public interface IExpenseService
{
    Task<IEnumerable<Expense>> GetAllExpensesAsync();
    Task<Expense?> GetExpenseByIdAsync(Guid id);
    Task<Expense> CreateExpenseAsync(CreateExpenseRequest request);
    Task<Expense> UpdateExpenseAsync(Guid id, UpdateExpenseRequest request);
    Task<bool> DeleteExpenseAsync(Guid id);
    Task<IEnumerable<Expense>> GetExpensesByDateRangeAsync(DateTime startDate, DateTime endDate);
    Task<IEnumerable<CategorySummary>> GetCategorySummariesAsync();
    Task<decimal> GetTotalExpensesAsync();
    Task<decimal> GetTotalExpensesByCategoryAsync(string category);
}

/// <summary>
/// Request model for creating an expense
/// </summary>
public class CreateExpenseRequest
{
    public decimal Amount { get; set; }
    public string Category { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public DateTime Date { get; set; } = DateTime.UtcNow;
}

/// <summary>
/// Request model for updating an expense
/// </summary>
public class UpdateExpenseRequest
{
    public decimal? Amount { get; set; }
    public string? Category { get; set; }
    public string? Description { get; set; }
    public DateTime? Date { get; set; }
}
