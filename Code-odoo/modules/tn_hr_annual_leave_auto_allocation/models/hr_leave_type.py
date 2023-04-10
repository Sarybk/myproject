from odoo import models, fields, api, _
from datetime import timedelta, datetime, date


class HRLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    anul_leave = fields.Boolean(string='Anull Leave')