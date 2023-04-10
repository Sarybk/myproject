from odoo import models, fields, api

class PospaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    is_bank = fields.Boolean('Banck', store=True)
    bank_journal_id = fields.Many2one('account.journal',
        string='Banck Journal',
        domain=[('type', '=', 'bank')],
        ondelete='restrict')
    analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')

    @api.onchange('is_bank')
    def _onchange_is_bank(self):
        if not self.is_bank:
            self.bank_journal_id = False
        else:
            self.use_payment_terminal = False

