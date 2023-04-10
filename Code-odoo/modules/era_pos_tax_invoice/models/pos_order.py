
from odoo import models, fields, api

class POSConfigInherit(models.Model):
    _inherit = 'pos.config'

    allow_qr_code = fields.Boolean(string="Add QR Code in Receipt",default=True)
    shift_time = fields.Boolean(string="Morning/Evening Shift",default=True)
    priority = fields.Integer(string='Priority')
    branch_name = fields.Many2one('res.partner',related="crm_team_id.partner_id")
    closeThePOSSessionAt= fields.Datetime('تاريخ إغلاق الجلسة', required=True, default=lambda self: fields.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))




