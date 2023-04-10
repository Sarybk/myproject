# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import timedelta, datetime, date


class HRLeaveAccrualLevel(models.Model):
    _inherit = 'hr.leave.accrual.level'

    added_value = fields.Float(
        "Rate", required=True,
        help="The number of hours/days that will be incremented in the specified Time Off Type for every period", digits=(12, 3))

    

   