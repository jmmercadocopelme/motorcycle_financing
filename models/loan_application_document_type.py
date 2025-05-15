from odoo import models, fields

class LoanApplicationDocumentType(models.Model):
    _name = 'loan.application.document.type'
    _description = 'Loan Application Document Type'

    name = fields.Char(string='Document Type Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    document_number = fields.Integer(string='Required Document Number')
