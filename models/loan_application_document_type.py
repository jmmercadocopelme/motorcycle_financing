from odoo import models, fields

class LoanApplicationDocumentType(models.Model):
    _name = 'loan.application.document.type'
    _description = 'Loan Application Document Type'
    _order = 'name'
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Document type name must be unique.')
    ]

    name = fields.Char(string='Documents', required=True)
    active = fields.Boolean(string='Active', default=True)
    document_number = fields.Integer(string='Required Document Number')