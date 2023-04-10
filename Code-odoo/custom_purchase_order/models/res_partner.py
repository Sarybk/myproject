# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import timedelta, datetime, date


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_account_payment_id = fields.Many2one(
        'account.account',
        string='Account Payment',
    )