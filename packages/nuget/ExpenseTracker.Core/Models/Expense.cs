namespace ExpenseTracker.Core.Models;

/// <summary>
/// Represents an expense entry in the expense tracker
/// </summary>
public class Expense
{
    /// <summary>
    /// Unique identifier for the expense
    /// </summary>
    public Guid Id { get; set; } = Guid.NewGuid();

    /// <summary>
    /// The monetary amount of the expense
    /// </summary>
    public decimal Amount { get; set; }

    /// <summary>
    /// Category of the expense (e.g., Food, Transportation)
    /// </summary>
    public string Category { get; set; } = string.Empty;

    /// <summary>
    /// Description of the expense
    /// </summary>
    public string Description { get; set; } = string.Empty;

    /// <summary>
    /// Date when the expense occurred
    /// </summary>
    public DateTime Date { get; set; } = DateTime.UtcNow;

    /// <summary>
    /// Timestamp when the expense was created
    /// </summary>
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    /// <summary>
    /// Timestamp when the expense was last updated
    /// </summary>
    public DateTime? UpdatedAt { get; set; }
}

/// <summary>
/// Represents a category for organizing expenses
/// </summary>
public class Category
{
    /// <summary>
    /// Unique identifier for the category
    /// </summary>
    public Guid Id { get; set; } = Guid.NewGuid();

    /// <summary>
    /// Name of the category
    /// </summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// Description of the category
    /// </summary>
    public string? Description { get; set; }

    /// <summary>
    /// Color code for UI display
    /// </summary>
    public string? ColorCode { get; set; }

    /// <summary>
    /// Whether the category is active
    /// </summary>
    public bool IsActive { get; set; } = true;
}

/// <summary>
/// Summary of expenses by category
/// </summary>
public class CategorySummary
{
    /// <summary>
    /// Category name
    /// </summary>
    public string Category { get; set; } = string.Empty;

    /// <summary>
    /// Total amount spent in this category
    /// </summary>
    public decimal Total { get; set; }

    /// <summary>
    /// Number of expenses in this category
    /// </summary>
    public int Count { get; set; }

    /// <summary>
    /// Average expense amount in this category
    /// </summary>
    public decimal Average => Count > 0 ? Total / Count : 0;
}
