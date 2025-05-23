from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    application_ids = fields.One2many('loan.application', 'partner_id', string='Loan Applications')
    application_count = fields.Integer(string='Loan Application Count', compute='_compute_application_count')

    def _compute_application_count(self):
        for rec in self:
            rec.application_count = len(rec.application_ids)

    def action_view_applications(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Loan Applications',
            'res_model': 'loan.application',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': dict(self.env.context),
        }