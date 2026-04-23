describe('Acceptance tests - end user journeys', () => {
  it('solves a root using bisection from UI', () => {
    cy.intercept('POST', '**/api/bisection', {
      statusCode: 200,
      body: {
        status: 'success',
        error: null,
        message: 'Root found',
        root: 2,
        iterations: [
          [1, 1.5, -1.75, 0.5],
          [2, 2, 0, 0.25],
        ],
      },
    }).as('bisectionRequest');

    cy.visit('/bisection');

    cy.get('#leftBound').type('0');
    cy.get('#rightBound').type('3');
    cy.get('#tolerance').type('0.0001');
    cy.get('#maxIterations').type('50');
    cy.get('#functionExpression').type('x**2 - 4');
    cy.get('button[type="submit"]').contains('Submit').click();

    cy.wait('@bisectionRequest');
    cy.contains('Root found:').should('be.visible');
    cy.contains('2').should('be.visible');
  });

  it('calculates interpolation from UI and shows resulting polynomial', () => {
    cy.intercept('POST', '**/api/interpolation', {
      statusCode: 200,
      body: {
        polynom: 'x**2 + 1',
      },
    }).as('interpolationRequest');

    cy.visit('/interpolations');

    cy.get('#methodSelect').select('newton');
    cy.get('#matrixSize').clear().type('3');

    cy.get('input[placeholder="x1"]').clear().type('0');
    cy.get('input[placeholder="x2"]').clear().type('1');
    cy.get('input[placeholder="x3"]').clear().type('2');

    cy.get('input[placeholder="y1"]').clear().type('1');
    cy.get('input[placeholder="y2"]').clear().type('2');
    cy.get('input[placeholder="y3"]').clear().type('5');

    cy.contains('button', 'Calculate Interpolation').click();

    cy.wait('@interpolationRequest');
    cy.contains('Resulting Polynomial:').should('be.visible');
    cy.contains('x**2 + 1').should('be.visible');
  });
});
