# -*- coding: utf-8 -*-
from lxml import etree

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    payment_select = fields.Selection([
        ('first_payment', 'First Payment'),
        ('percent', 'Percentage%'),
        ('amount', 'Amount')]
    )
    percentage  = fields.Float(
        string='Percentage',
    )
    fixed_amount = fields.Float(
        string='Fixed Amount',
    )
    is_first_paied = fields.Boolean(
        string='First Paied',
    )
    count = fields.Integer(
        string='Counter',
    )

    purchase_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
    )

   