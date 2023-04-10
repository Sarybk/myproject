from odoo import models, fields, api, _
from datetime import timedelta, datetime, date


class HRLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    number_of_days = fields.Float(
        'Number of Days', compute='_compute_from_holiday_status_id', store=True, readonly=False, tracking=True, default=1,
        help='Duration in days. Reference field to use when necessary.', digits=(12, 3))

    number_of_days_display = fields.Float(
        'Duration (days)', compute='_compute_number_of_days_display',
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
        help="If Accrual Allocation: Number of days allocated in addition to the ones you will get via the accrual' system.", digits=(12, 3))
