from odoo import models, fields

class LoanApplicationTag(models.Model):
    _name = 'loan.application.tag'
    _description = 'Loan Application Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')
