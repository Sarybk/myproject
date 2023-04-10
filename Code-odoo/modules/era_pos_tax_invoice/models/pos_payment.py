from odoo import models, fields, api

class Pospayment(models.Model):
    _inherit = 'pos.payment'

    pos_tax = fields.Monetary(
              string='Tax', 
              currency_field='currency_id', 
              readonly=True, help="Total amount of the payment x (sale_tax)%"
    )

    amount_untax = fields.Monetary(
              string='Amount Without Tax', 
             )

    @api.model
    def create(self, vals):
        res = super(Pospayment, self).create(vals)
        tax_lst = self.env['account.tax'].sudo().search([('type_tax_use', '=', 'sale')], limit=1)
        res.pos_tax = (vals['amount']/(1.0+(tax_lst.amount/100)))-vals['amount']
        res.amount_untax = vals['amount'] - tax_lst.amount
        return res
    