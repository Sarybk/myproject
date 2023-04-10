from datetime import timedelta
from odoo import api, fields, models, _

class PosSession(models.Model):
	_inherit = 'account.move.line'
	shift_time = fields.Boolean(string="Morning/Evening Shift",default=True)

class PosSession(models.Model):
	_inherit = 'pos.session'
	_order = 'priority'
	
	shift_time = fields.Boolean(related="config_id.shift_time", string="Morning/Evening Shift")
	priority = fields.Integer(related="config_id.priority", string="Priority")

	def _create_account_move(self):
		res = super(PosSession, self)._create_account_move()
		account_move = self.env['account.move'].search([('ref', '=', self.name)])
		for line in account_move.line_ids:
			line.partner_id = self.config_id.crm_team_id.partner_id.id
			line.shift_time = self.config_id.shift_time
		return res
