from odoo import models, fields

class LoanApplicationTag(models.Model):
    _name = 'loan.application.tag'
    _description = 'Loan Application Tag'
    _order = 'name'
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Tag name must be unique.')
    ]

    name = fields.Char(string='Documents', required=True)
    color = fields.Integer(string='Tags')