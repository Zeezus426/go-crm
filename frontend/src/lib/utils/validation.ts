export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function validatePhone(phone: string): boolean {
  const phoneRegex = /^\+?[\d\s-()]+$/;
  return phoneRegex.test(phone);
}

export function validateUrl(url: string): boolean {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

export function validateRequired(value: any): boolean {
  if (typeof value === 'string') {
    return value.trim().length > 0;
  }
  return value !== null && value !== undefined;
}

export function getValidationErrors(formData: Record<string, any>, rules: Record<string, (value: any) => boolean>): Record<string, string> {
  const errors: Record<string, string> = {};

  Object.entries(rules).forEach(([field, validator]) => {
    if (!validator(formData[field])) {
      errors[field] = `${field} is invalid`;
    }
  });

  return errors;
}