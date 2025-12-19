/**
 * Expense Validators Package
 * Provides validation functions for expense data
 */

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

export interface ExpenseInput {
  amount?: number;
  category?: string;
  description?: string;
  date?: string | Date;
}

const VALID_CATEGORIES = [
  'Food',
  'Transportation',
  'Entertainment',
  'Utilities',
  'Healthcare',
  'Shopping',
  'Other'
];

/**
 * Validate expense amount
 */
export function validateAmount(amount: number | undefined): ValidationResult {
  const errors: string[] = [];
  
  if (amount === undefined || amount === null) {
    errors.push('Amount is required');
  } else if (typeof amount !== 'number' || isNaN(amount)) {
    errors.push('Amount must be a valid number');
  } else if (amount <= 0) {
    errors.push('Amount must be greater than zero');
  } else if (amount > 1000000) {
    errors.push('Amount exceeds maximum allowed value');
  }
  
  return { isValid: errors.length === 0, errors };
}

/**
 * Validate expense category
 */
export function validateCategory(category: string | undefined): ValidationResult {
  const errors: string[] = [];
  
  if (!category || category.trim() === '') {
    errors.push('Category is required');
  } else if (!VALID_CATEGORIES.includes(category)) {
    errors.push(`Invalid category. Must be one of: ${VALID_CATEGORIES.join(', ')}`);
  }
  
  return { isValid: errors.length === 0, errors };
}

/**
 * Validate expense description
 */
export function validateDescription(description: string | undefined): ValidationResult {
  const errors: string[] = [];
  
  if (!description || description.trim() === '') {
    errors.push('Description is required');
  } else if (description.length < 3) {
    errors.push('Description must be at least 3 characters');
  } else if (description.length > 500) {
    errors.push('Description must not exceed 500 characters');
  }
  
  return { isValid: errors.length === 0, errors };
}

/**
 * Validate expense date
 */
export function validateDate(date: string | Date | undefined): ValidationResult {
  const errors: string[] = [];
  
  if (!date) {
    errors.push('Date is required');
  } else {
    const parsedDate = new Date(date);
    if (isNaN(parsedDate.getTime())) {
      errors.push('Invalid date format');
    } else if (parsedDate > new Date()) {
      errors.push('Date cannot be in the future');
    }
  }
  
  return { isValid: errors.length === 0, errors };
}

/**
 * Validate complete expense input
 */
export function validateExpense(expense: ExpenseInput): ValidationResult {
  const allErrors: string[] = [];
  
  const amountResult = validateAmount(expense.amount);
  const categoryResult = validateCategory(expense.category);
  const descriptionResult = validateDescription(expense.description);
  const dateResult = validateDate(expense.date);
  
  allErrors.push(...amountResult.errors);
  allErrors.push(...categoryResult.errors);
  allErrors.push(...descriptionResult.errors);
  allErrors.push(...dateResult.errors);
  
  return { isValid: allErrors.length === 0, errors: allErrors };
}

/**
 * Get list of valid categories
 */
export function getValidCategories(): string[] {
  return [...VALID_CATEGORIES];
}
