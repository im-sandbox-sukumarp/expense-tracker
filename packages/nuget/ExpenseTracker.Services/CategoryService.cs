using ExpenseTracker.Core.Interfaces;
using ExpenseTracker.Core.Models;

namespace ExpenseTracker.Services;

/// <summary>
/// Service for managing categories
/// </summary>
public class CategoryService : ICategoryService
{
    private readonly ICategoryRepository _categoryRepository;

    public CategoryService(ICategoryRepository categoryRepository)
    {
        _categoryRepository = categoryRepository;
    }

    /// <inheritdoc />
    public async Task<IEnumerable<Category>> GetAllCategoriesAsync()
    {
        return await _categoryRepository.GetAllAsync();
    }

    /// <inheritdoc />
    public async Task<Category?> GetCategoryByIdAsync(Guid id)
    {
        return await _categoryRepository.GetByIdAsync(id);
    }

    /// <inheritdoc />
    public async Task<Category?> GetCategoryByNameAsync(string name)
    {
        return await _categoryRepository.GetByNameAsync(name);
    }

    /// <inheritdoc />
    public async Task<Category> CreateCategoryAsync(CreateCategoryRequest request)
    {
        // Check if category already exists
        var existing = await _categoryRepository.GetByNameAsync(request.Name);
        if (existing != null)
        {
            throw new ArgumentException($"Category '{request.Name}' already exists.");
        }

        var category = new Category
        {
            Name = request.Name,
            Description = request.Description,
            ColorCode = request.ColorCode
        };

        return await _categoryRepository.AddAsync(category);
    }

    /// <inheritdoc />
    public async Task<Category> UpdateCategoryAsync(Guid id, UpdateCategoryRequest request)
    {
        var category = await _categoryRepository.GetByIdAsync(id);
        if (category == null)
        {
            throw new ArgumentException($"Category with ID '{id}' not found.");
        }

        if (!string.IsNullOrEmpty(request.Name))
            category.Name = request.Name;
        
        if (request.Description != null)
            category.Description = request.Description;
        
        if (request.ColorCode != null)
            category.ColorCode = request.ColorCode;

        if (request.IsActive.HasValue)
            category.IsActive = request.IsActive.Value;

        return await _categoryRepository.UpdateAsync(category);
    }

    /// <inheritdoc />
    public async Task<bool> DeleteCategoryAsync(Guid id)
    {
        return await _categoryRepository.DeleteAsync(id);
    }
}

/// <summary>
/// Service interface for category operations
/// </summary>
public interface ICategoryService
{
    Task<IEnumerable<Category>> GetAllCategoriesAsync();
    Task<Category?> GetCategoryByIdAsync(Guid id);
    Task<Category?> GetCategoryByNameAsync(string name);
    Task<Category> CreateCategoryAsync(CreateCategoryRequest request);
    Task<Category> UpdateCategoryAsync(Guid id, UpdateCategoryRequest request);
    Task<bool> DeleteCategoryAsync(Guid id);
}

/// <summary>
/// Request model for creating a category
/// </summary>
public class CreateCategoryRequest
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public string? ColorCode { get; set; }
}

/// <summary>
/// Request model for updating a category
/// </summary>
public class UpdateCategoryRequest
{
    public string? Name { get; set; }
    public string? Description { get; set; }
    public string? ColorCode { get; set; }
    public bool? IsActive { get; set; }
}
