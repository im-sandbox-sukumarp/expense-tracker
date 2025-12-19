# Expense Tracker Packages

This directory contains reusable packages for the Expense Tracker application, designed for migration testing purposes.

## NPM Packages

### @im-sandbox-sukumarp/expense-utils (v1.0.0)
Utility functions for expense tracking and calculations.

**Features:**
- Calculate expense totals
- Group expenses by category
- Filter expenses by date range
- Format currency values

**Build:**
```bash
cd packages/npm/expense-utils
npm install
npm run build
```

### @im-sandbox-sukumarp/expense-validators (v1.2.0)
Validation utilities for expense data.

**Features:**
- Validate expense amounts
- Validate categories
- Validate descriptions
- Validate dates
- Complete expense validation

**Build:**
```bash
cd packages/npm/expense-validators
npm install
npm run build
```

## NuGet Packages

### im-sandbox-sukumarp.ExpenseTracker.Core (v1.0.0)
Core models and interfaces for the Expense Tracker application.

**Contents:**
- `Expense` model
- `Category` model
- `CategorySummary` model
- `IExpenseRepository` interface
- `ICategoryRepository` interface

**Build:**
```bash
cd packages/nuget/ExpenseTracker.Core
dotnet build
dotnet pack
```

### im-sandbox-sukumarp.ExpenseTracker.Services (v1.1.0)
Service layer implementations for the Expense Tracker application.

**Contents:**
- `ExpenseService` - Expense management operations
- `CategoryService` - Category management operations
- Request/Response DTOs

**Build:**
```bash
cd packages/nuget/ExpenseTracker.Services
dotnet build
dotnet pack
```

## Publishing

### NPM Packages
```bash
# Login to npm/GitHub Packages
npm login --registry=https://npm.pkg.github.com

# Publish
npm publish
```

### NuGet Packages
```bash
# Pack the project
dotnet pack -c Release

# Push to NuGet/GitHub Packages
dotnet nuget push "bin/Release/*.nupkg" --source "github"
```

## Migration Testing

These packages are designed for testing package migration scenarios:
- Registry migration (npm ↔ GitHub Packages)
- Version migration
- Dependency resolution
- Cross-package dependencies
