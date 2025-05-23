from odoo import models, fields, api, _
from odoo.exceptions import UserError

class LoanApplicationDocument(models.Model):
    _name = 'loan.application.document'
    _description = 'Loan Application Document'
    _order = 'sequence, id'

    name = fields.Char(string='Documents', required=True)
    application_id = fields.Many2one('loan.application', string='Application')
    attachment = fields.Binary(string='Attachment')
    type_id = fields.Many2one('loan.application.document.type', string='Type')
    state = fields.Selection(
        [
            ('new', 'New'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        string='State',
        required=True,
        default='new'
    )
    sequence = fields.Integer(string='Sequence', default=10)

    # Botones de acción
    def action_approve_document(self):
        for rec in self:
            rec.state = 'approved'

    def action_reject_document(self):
        for rec in self:
            rec.state = 'rejected'

    @api.onchange('attachment')
    def _onchange_attachment(self):
        for rec in self:
            rec.state = 'new'