class ExpressionUtils {
  sanitizeExpression(expression: string): string {
    let sanitized = expression.replace(/\*\*/g, '^');
    sanitized = sanitized.replace(/([0-9])([a-zA-Z])/g, '$1*$2');
    sanitized = sanitized.replace(/([a-zA-Z])([0-9])/g, '$1*$2');
    
    return sanitized;
  }
}

export default new ExpressionUtils();
