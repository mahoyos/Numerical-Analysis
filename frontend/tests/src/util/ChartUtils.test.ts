import { describe, expect, it } from 'vitest';

import ExpressionUtils from '../../../src/util/ChartUtils';

describe('ChartUtils', () => {
  it('sanitizes exponent and implicit multiplication', () => {
    const result = ExpressionUtils.sanitizeExpression('2x**2 + x3');
    expect(result).toBe('2*x^2 + x*3');
  });

  it('keeps expression structure', () => {
    const result = ExpressionUtils.sanitizeExpression('(x+1)/(x-2)');
    expect(result).toBe('(x+1)/(x-2)');
  });
});
