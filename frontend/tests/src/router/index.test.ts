import { describe, expect, it } from 'vitest';

import router from '../../../src/router';

describe('router', () => {
  it('registers the main routes', () => {
    const routeNames = router.getRoutes().map((route) => route.name);

    expect(routeNames).toContain('home');
    expect(routeNames).toContain('non-linear-equations');
    expect(routeNames).toContain('equations-systems');
    expect(routeNames).toContain('interpolations');
  });

  it('contains detail routes for non-linear methods', () => {
    const paths = router.getRoutes().map((route) => route.path);
    expect(paths).toContain('/fixed-point');
    expect(paths).toContain('/newton-raphson');
    expect(paths).toContain('/multiple-roots');
    expect(paths).toContain('/false-position');
    expect(paths).toContain('/bisection');
    expect(paths).toContain('/secant');
  });
});
