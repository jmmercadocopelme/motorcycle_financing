from odoo import models, fields

class LoanApplicationTag(models.Model):
    _name = 'loan.application.tag'
    _description = 'Loan Application Tag'

    name = fields.Char(string='Documents', required=True)
    color = fields.Integer(string='Tags')