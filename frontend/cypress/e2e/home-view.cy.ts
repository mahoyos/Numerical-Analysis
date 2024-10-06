describe('Urbam View', () => {
    beforeEach(() => {
        cy.visit('/');
    });

    it('should display the breadcrumb with Inicio link', () => {
        cy.contains('Inicio').should('exist');
    });

    it('should display the card header with "Urbam"', () => {
        cy.get('.card-header h6').should('have.text', 'Urbam');
    });

    it('should display the correct paragraphs in the card body', () => {
        cy.get('.card-body').within(() => {
            cy.contains('creamos entornos urbanos y rurales sostenibles').should('exist');
            cy.contains('Transformamos territorios emergentes').should('exist');
            cy.contains('conectar la academia con el mundo real').should('exist');
            cy.contains('centro las personas').should('exist');
        });
    });
});
