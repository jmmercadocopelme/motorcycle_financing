from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    loan_application_ids = fields.One2many('loan.application', 'sale_order_id', string='Loan Applications')
    is_financed = fields.Boolean(string='Is Financed')
    state = fields.Selection(selection_add=[('loan_requested', 'Solicitado Préstamo')])

    def action_apply_loan(self):
        self.ensure_one()
        product = self._get_motorcycle_product()
        context = self._prepare_loan_application_context(product)
        self.state = 'loan_requested'
        return {
            'type': 'ir.actions.act_window',
            'name': _('Loan Application'),
            'res_model': 'loan.application',
            'view_mode': 'form',
            'target': 'current',
            'context': context,
        }

    def _prepare_loan_application_context(self, product):
        self.ensure_one()
        return {
            'default_sale_order_id': self.id,
            'default_product_template_id': product.id,
            'default_name': f"{self.partner_id.name or ''} - {product.name or ''}",
        }

    def _get_motorcycle_product(self):
        self.ensure_one()
        motorcycle_lines = self.order_line.filtered(lambda l: l.product_id.categ_id.name == 'Motocicleta')
        if len(motorcycle_lines) > 1:
            raise UserError(_('Only one motorcycle can be financed per loan application.'))
        if not motorcycle_lines:
            raise UserError(_('No motorcycle product found in this sale order.'))
        return motorcycle_lines[0].product_id

    @api.onchange('is_financed')
    def _onchange_is_financed(self):
        for rec in self:
            motorcycle_lines = rec.order_line.filtered(lambda l: l.product_id.categ_id.name == 'Motocicleta')
            if rec.is_financed and len(motorcycle_lines) != 1:
                raise UserError(_('There must be exactly one motorcycle product in the sale order to request financing.'))