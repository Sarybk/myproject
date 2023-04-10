# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import timedelta, datetime, date
from dateutil import relativedelta
from odoo.exceptions import  UserError

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    rejoin_date = fields.Date(string='Rejoin Date', default=fields.Date.today())
    duration_deserve = fields.Float(string='Duration Deserve', digits=(12, 3))

    
    def create_employee_location(self):
        obj_emb = self.env['hr.employee']
        obj_location = self.env['hr.leave.allocation']
        leave_type = self.env['hr.leave.type'].search([('anul_leave', '=', True)])
        accrual_plan = self.env['hr.leave.accrual.plan'].search([('time_off_type_id.anul_leave', '=', True)])
        lst_emb = obj_emb.search([])
        
        for rec in lst_emb:
            if not accrual_plan:
                raise UserError(_('PLease in Time Off Type for accrual plan check anull leav field is True  '))
            if rec.rejoin_date and accrual_plan[0] and rec.contract_id.state == 'open':
                duration_contract = rec.calculate_number_years(rec)
                for level in accrual_plan.level_ids:
                    if duration_contract < 5 and level.added_value == 1.875:
                        lst_date = rec.calculate_number_months(rec)
                        mont = level.added_value * lst_date[0]
                        days = (level.added_value / 30) * lst_date[1]
                        rec.duration_deserve = mont + days

                    elif duration_contract > 5 and level.added_value == 2.5:
                        lst_date = rec.calculate_number_months(rec)
                        mont = level.added_value * lst_date[0]
                        days = (level.added_value / 30) * lst_date[1]
                        rec.duration_deserve = mont + days

                if [location.employee_id.id for location in obj_location.search([('employee_id', '=', rec.id)])]:
                    pass
                else:
                    if rec.duration_deserve != 0:
                        vals = {
                            'name':rec.name,
                            'number_of_days': rec.duration_deserve,
                            'holiday_status_id': leave_type[0].id,
                            'employee_id': rec.id,
                            'employee_ids': [(6, 0, [rec.id])],
                            'state': 'confirm',
                        }
                        obj_location.create(vals)
                   
             
        

    def calculate_number_months(self, numb):
        date1 = datetime.strptime(str(numb.rejoin_date), '%Y-%m-%d')
        date2 = datetime.strptime(str(date.today()), '%Y-%m-%d')
        num_date = relativedelta.relativedelta(date2, date1)
        return num_date.months, num_date.days

    def calculate_number_years(self, numb):
        date1 = datetime.strptime(str(numb.contract_id.date_start), '%Y-%m-%d')
        date2 = datetime.strptime(str(date.today()), '%Y-%m-%d')
        num_date =  relativedelta.relativedelta(date2, date1)
        return num_date.years


 