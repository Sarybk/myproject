# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import timedelta, datetime, date


class HRContract(models.Model):
    _inherit = 'hr.contract'

    deserve_leave = fields.Selection([('one_year', 'One Year'), ('two_year', 'Two Years')], 'Deserve Leave Type')
    

   