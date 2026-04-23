describe('Smoke tests - Numerical Analysis app', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('loads home and main navigation', () => {
    cy.contains('Welcome to Numerical Methods Calculator').should('be.visible');
    cy.contains('a, span', 'Home').should('exist');
    cy.contains('a, span', 'Non-Linear Equations').should('exist');
    cy.contains('a, span', 'Equations Systems').should('exist');
    cy.contains('a, span', 'Interpolations').should('exist');
  });

  it('navigates to key modules from sidebar', () => {
    cy.contains('a', 'Non-Linear Equations').click();
    cy.url().should('include', '/non-linear-equations');
    cy.contains('Non-Linear Equations').should('be.visible');

    cy.contains('a', 'Equations Systems').click();
    cy.url().should('include', '/equations-systems');
    cy.contains('Systems of Linear Equations').should('be.visible');

    cy.contains('a', 'Interpolations').click();
    cy.url().should('include', '/interpolations');
    cy.contains('Interpolation Methods').should('be.visible');
  });
});
