from odoo import models, fields

class LoanApplicationDocument(models.Model):
    _name = 'loan.application.document'
    _description = 'Loan Application Document'

    name = fields.Char(string='Document Name', required=True)
    application_id = fields.Many2one('loan.application', string='Loan Application')
    attachment = fields.Binary(string='Attachment')
    type_id = fields.Many2one('loan.application.document.type', string='Document Type')
    state = fields.Selection([
        ('new', 'New'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='State', default='new', required=True)
