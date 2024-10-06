class ExpressionUtils {
  sanitizeExpression(expression: string): string {
    return expression.replace(/\*\*/g, '^');
  }
}

export default new ExpressionUtils();
