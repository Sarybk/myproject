# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    payment_product_id = fields.Many2one('product.product',string='Payment Product', config_parameter='custom_purchase_order.payment_product_id')
    # tax_product_id = fields.Many2one('product.product',string='Tax Product', config_parameter='custom_purchase_order.tax_product_id')
    retantion_product_id = fields.Many2one('product.product',string='Retantion Product', config_parameter='custom_purchase_order.retantion_product_id')

    # Confirm Purchase amount Supply Cahein Manager and CEO Manager
    supply_amount = fields.Float('Supply chain Less than', config_parameter='custom_purchase_order.supply_amount')
    ceo_amount = fields.Float('CEO limit above', config_parameter='custom_purchase_order.ceo_amount')



