from odoo import models, fields, api, _
from odoo.exceptions import UserError

class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_application desc'

    name = fields.Char(string='Application Number', required=True)
    sale_order_id = fields.Many2one('sale.order', string='Related Sale Order')
    sale_order_total = fields.Monetary(
        string='Sale Order Total',
        related='sale_order_id.amount_total',
        store=True,
        readonly=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='sale_order_id.currency_id',
        store=True,
        readonly=False
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        related='sale_order_id.partner_id',
        store=True,
        readonly=False
    )
    user_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        related='sale_order_id.user_id',
        store=True,
        readonly=False
    )
    product_template_id = fields.Many2one('product.product', string='Product')
    date_application = fields.Date(string='Application Date', readonly=True, copy=False)
    date_approval = fields.Date(string='Approval Date', readonly=True, copy=False)
    date_rejection = fields.Date(string='Rejection Date', readonly=True, copy=False)
    date_signed = fields.Datetime(string='Signed On', readonly=True, copy=False)
    down_payment = fields.Monetary(
        string='Downpayment',
        required=True,
        currency_field='currency_id'
    )
    loan_amount = fields.Monetary(
        string='Loan Amount',
        compute='_compute_loan_amount',
        inverse='_inverse_loan_amount',
        store=True,
        currency_field='currency_id'
    )
    interest_rate = fields.Float(
        string='Interest Rate (%)',
        required=True,
        digits=(5, 2)
    )
    loan_term = fields.Integer(
        string='Loan Term (Months)',
        required=True,
        default=36
    )
    rejection_reason = fields.Text(string='Rejection Reason', copy=False)
    state = fields.Selection(
        string='Status',
        selection=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('review', 'Credit Check'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('signed', 'Signed'),
            ('cancel', 'Canceled')
        ],
        default='draft',
        copy=False,
        tracking=True
    )
    notes = fields.Html(string='Notes', copy=False)
    document_ids = fields.One2many(
        'loan.application.document',
        'application_id',
        string='Documents'
    )
    tag_ids = fields.Many2many(
        'loan.application.tag',
        string='Tags'
    )
    document_count = fields.Integer(
        string='Document Count',
        compute='_compute_document_counts',
        store=True
    )
    document_count_approved = fields.Integer(
        string='Approved Document Count',
        compute='_compute_document_counts',
        store=True
    )

    # Display Name
    @api.depends('partner_id', 'product_template_id')
    def _compute_display_name(self):
        for rec in self:
            partner = rec.partner_id.name or ''
            product = rec.product_template_id.name or ''
            rec.display_name = f"{partner} - {product}" if partner and product else partner or product or rec.name

    display_name = fields.Char(compute='_compute_display_name', store=True)

    # SQL Constraints
    _sql_constraints = [
        ('down_payment_positive', 'CHECK(down_payment >= 0)', 'Down payment must be positive.'),
        ('loan_amount_positive', 'CHECK(loan_amount >= 0)', 'Loan amount must be positive.'),
    ]

    @api.depends('sale_order_id.amount_total', 'down_payment')
    def _compute_loan_amount(self):
        for rec in self:
            if rec.sale_order_id:
                rec.loan_amount = rec.sale_order_total - rec.down_payment
            else:
                rec.loan_amount = 0.0

    def _inverse_loan_amount(self):
        for rec in self:
            if rec.sale_order_id:
                rec.down_payment = rec.sale_order_total - rec.loan_amount

    @api.depends('document_ids.state')
    def _compute_document_counts(self):
        for rec in self:
            rec.document_count = len(rec.document_ids)
            rec.document_count_approved = len(rec.document_ids.filtered(lambda d: d.state == 'approved'))

    @api.constrains('down_payment', 'sale_order_total')
    def _check_down_payment(self):
        for rec in self:
            if rec.down_payment > rec.sale_order_total:
                raise UserError(_('Down payment cannot exceed the sale order total.'))

    # Botones de acción
    def action_send_for_approval(self):
        for rec in self:
            if not rec.document_ids or any(doc.state != 'approved' for doc in rec.document_ids):
                raise UserError(_('All documents must be approved before sending for approval.'))
            rec.state = 'sent'
            rec.date_application = fields.Date.today()

    def action_approve_loan(self):
        for rec in self:
            rec.state = 'approved'
            rec.date_approval = fields.Date.today()

    def action_reject_loan(self):
        for rec in self:
            if not rec.rejection_reason:
                raise UserError(_('Please provide a rejection reason.'))
            rec.state = 'rejected'
            rec.date_rejection = fields.Date.today()

    # Sobrescritura de create para crear documentos automáticamente
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        doc_type_model = self.env['loan.application.document.type']
        doc_types = doc_type_model.search([('active', '=', True)])
        for rec in records:
            for doc_type in doc_types:
                self.env['loan.application.document'].create({
                    'name': doc_type.name,
                    'application_id': rec.id,
                    'type_id': doc_type.id,
                })
        return records