from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    retained_warranty = fields.Float('Retained Warranty %')
    percentage = fields.Float('Percentage %')

# class SaleAdvancePaymentInv(models.TransientModel):
#     _inherit = "sale.advance.payment.inv"

#     def _prepare_invoice_values(self):
#         res = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(self, order, name, amount, so_line)
#         res.update({
#             'sale_order_id':self.id,
#             })
#         return res


