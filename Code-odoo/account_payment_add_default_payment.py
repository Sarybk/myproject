from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'


    transaction_date = fields.Datetime('Transaction Date')


class AccountRegisterPayment(models.TransientModel):
    _inherit = 'account.payment.register'


    transaction_date = fields.Datetime('Transaction Date')


    def _create_payment_vals_from_wizard(self):
        payment_vals = {
            'date': self.payment_date,
            'amount': self.amount,
            'payment_type': self.payment_type,
            'partner_type': self.partner_type,
            'ref': self.communication,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self.partner_bank_id.id,
            'payment_method_line_id': self.payment_method_line_id.id,
            'destination_account_id': self.line_ids[0].account_id.id,
            'indeal_ref': self.indeal_ref or "",
            'analytic_tag_ids': self.analytic_tag_ids.ids,
            'transaction_date': self.transaction_date
        }

        if not self.currency_id.is_zero(self.payment_difference) and self.payment_difference_handling == 'reconcile':
            payment_vals['write_off_line_vals'] = {
                'name': self.writeoff_label,
                'amount': self.payment_difference,
                'account_id': self.writeoff_account_id.id,
            }
        return payment_vals