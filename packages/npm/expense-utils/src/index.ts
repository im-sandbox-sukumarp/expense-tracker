/**
 * Expense Utilities Package
 * Provides utility functions for expense tracking and calculations
 */

export interface Expense {
  id: string;
  amount: number;
  category: string;
  description: string;
  date: Date;
}

export interface CategorySummary {
  category: string;
  total: number;
  count: number;
  average: number;
}

/**
 * Calculate the total amount from a list of expenses
 */
export function calculateTotal(expenses: Expense[]): number {
  return expenses.reduce((sum, expense) => sum + expense.amount, 0);
}

/**
 * Group expenses by category and calculate summaries
 */
export function groupByCategory(expenses: Expense[]): CategorySummary[] {
  const groups = new Map<string, Expense[]>();
  
  expenses.forEach(expense => {
    const existing = groups.get(expense.category) || [];
    existing.push(expense);
    groups.set(expense.category, existing);
  });
  
  return Array.from(groups.entries()).map(([category, items]) => {
    const total = items.reduce((sum, e) => sum + e.amount, 0);
    return {
      category,
      total,
      count: items.length,
      average: total / items.length
    };
  });
}

/**
 * Filter expenses by date range
 */
export function filterByDateRange(
  expenses: Expense[],
  startDate: Date,
  endDate: Date
): Expense[] {
  return expenses.filter(expense => {
    const date = new Date(expense.date);
    return date >= startDate && date <= endDate;
  });
}

/**
 * Format amount as currency string
 */
export function formatCurrency(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency
  }).format(amount);
}
