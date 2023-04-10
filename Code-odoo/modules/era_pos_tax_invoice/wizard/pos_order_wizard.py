from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError



class PosOrderWizard(models.TransientModel):
	_name = 'pos.order.wizard'
	_description = 'Pos Order Wizard'

	date = fields.Datetime('Date')
	date_from = fields.Datetime('Date From')
	date_to = fields.Datetime('Date To')
	is_period = fields.Boolean('Is Period')
	branch_id = fields.Many2one('res.users', string='Branch')


 
	# def get_branch(self):
	# 	self._cr.execute("""SELECT res.id
 #                     FROM pos_order pos, crm_team crm, res_partner res
 #                     WHERE pos.crm_team_id = crm.id AND crm.partner_id = res.id
 #                     group by  res.id
 #        """)
	# 	res = self._cr.dictfetchall() or False
	# 	return res

	def get_branch(self):
		self._cr.execute("""SELECT res.id
						FROM pos_order pos, res_users res
						where pos.user_id = res.id 
						 group by res.id
			""")
		res = self._cr.dictfetchall() or False

		lst = [list(record.values())[0] for record in res]
		return tuple(lst)
		


	def get_pos_branch(self):

		if self.date:
			self._cr.execute("""SELECT res.login as res, pos.amount_total, pop.pos_tax, pop.amount_untax, ss.config_id, pm.name, pm.is_cash_count, pm.is_bank
								From  pos_order pos,  pos_session ss, pos_payment pop, pos_payment_method pm, res_users res
								where pos.date_order = %s AND  ss.id = pos.session_id And pop.pos_order_id = pos.id AND pos.user_id in %s And 
								res.id = pos.user_id and pop.payment_method_id = pm.id
			""",(self.date, self.get_branch()))
			

		if self.date and self.branch_id:
			self._cr.execute("""SELECT res.login as res, pos.amount_total, pop.pos_tax, pop.amount_untax, ss.config_id, pm.name, pm.is_cash_count, pm.is_bank
								From  pos_order pos,  pos_session ss, pos_payment pop, pos_payment_method pm, res_users res
								where pos.date_order = %s AND  ss.id = pos.session_id And pop.pos_order_id = pos.id AND pos.user_id = %s And 
								res.id = pos.user_id and pop.payment_method_id = pm.id
					""",(self.date, self.branch_id.id))

		if self.date_from and self.date_to:
			self._cr.execute("""SELECT res.login as res, pos.amount_total, pop.pos_tax, pop.amount_untax, ss.config_id, pm.name, pm.is_cash_count, pm.is_bank
								From  pos_order pos,  pos_session ss, pos_payment pop, pos_payment_method pm, res_users res
								where pos.date_order >= %s AND pos.date_order <= %s AND ss.id = pos.session_id And pop.pos_order_id = pos.id And
								pos.user_id in %s And res.id = pos.user_id and pop.payment_method_id = pm.id
			""",(self.date_from, self.date_to, self.get_branch()))

		if self.date_from and self.date_to and self.branch_id:
			self._cr.execute("""SELECT res.login as res, pos.amount_total, pop.pos_tax, pop.amount_untax, ss.config_id, pm.name, pm.is_cash_count, pm.is_bank
								From  pos_order pos,  pos_session ss, pos_payment pop, pos_payment_method pm, res_users res
								where pos.date_order >= %s AND pos.date_order <= %s AND ss.id = pos.session_id And pop.pos_order_id = pos.id And
								pos.user_id = %s And res.id = pos.user_id and pop.payment_method_id = pm.id
			""",(self.date_from, self.date_to, self.branch_id.id))
			
		res = self._cr.dictfetchall()
		# print(res , '88888888888888888888888888888888888')
		return res

	def action_print(self):
		result = {}
		res = self.get_pos_branch()
		# print(res, 'REEEEEEEEEEEEEEEEEEEEEEEE')
		if not res:
			raise ValidationError(_("There is no point of sales in these date!")) 
		for rec in res:
			if rec['res'] not in result.keys():
				result[rec['res']] = [rec]
			else:
				result[rec['res']].append(rec)
		# print(result, 'UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR')

				
		data = {
			'result': result,
			'date': self.date,
			'date_from': self.date_from,
			'date_to': self.date_to,
			'is_period': self.is_period
		}
	
		# print(data, '444444444444444444444444444444444444444444444444444')
		return self.env.ref('era_pos_tax_invoice.report_pos_order').report_action(self, data=data)
        












