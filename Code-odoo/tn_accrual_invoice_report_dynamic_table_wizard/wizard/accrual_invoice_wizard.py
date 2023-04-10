from odoo import models, fields, _
from odoo.tools.translate import _
from datetime import date, datetime, timedelta
from dateutil.rrule import rrule, MONTHLY
import calendar
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import collections, functools, operator



class AccrualInvoice(models.TransientModel):
    _name = 'accrual.invoice'
    _description = "Accrual Invoice Wizard"

    date= fields.Date('Date')

    def action_print(self):
        rental_obj = self.env['rental.contract']
        current_year = fields.Date.today().year
        rentral_lst = rental_obj.search([('state', '=', 'confirmed')])
        contract_rental_ids = rentral_lst.filtered(lambda l: l.date_from == self.date)
        res = []
        res2 = []
        result = {}
        dict_year = {}
        total_prev = 0.0
        res2 = []
        for rec in contract_rental_ids:
            for line in rec.loan_line.filtered(lambda l: l.date.year == current_year):  #installment for currnt year
                if line.date.month == 1:
                    if line.amount_residual > 0:
                        res.append({'partner': line.loan_id.partner_id.name, 'jan':line.amount_residual})
                    elif line.amount_residual == 0 and line.payment_state != 'paid':
                        res.append({'partner': line.loan_id.partner_id.name, 'jan':line.amount})
                
                if line.date.month == 2:
                    if line.amount_residual > 0:
                        res.append({'partner': line.loan_id.partner_id.name,'feb':line.amount_residual})
                    elif line.amount_residual == 0 and line.payment_state != 'paid':
                        res.append({'partner': line.loan_id.partner_id.name,'feb':line.amount})
                
                if line.date.month == 3:
                    if line.amount_residual > 0:
                        res.append({'partner': line.loan_id.partner_id.name,'mar':line.amount_residual})
                    elif line.amount_residual == 0 and line.payment_state != 'paid':
                        res.append({'partner': line.loan_id.partner_id.name,'mar':line.amount})
                
                if line.date.month == 4:
                    if line.amount_residual > 0:
                        res.append({'partner': line.loan_id.partner_id.name,'apr':line.amount_residual})
                    elif line.amount_residual == 0 and line.payment_state != 'paid':
                        res.append({'partner': line.loan_id.partner_id.name,'apr':line.amount})
                
                if line.date.month == 5:
                    if line.amount_residual > 0:
                        res.append({'partner': line.loan_id.partner_id.name,'may':line.amount_residual})
                    elif line.amount_residual == 0 and line.payment_state != 'paid':
                        res.append({'partner': line.loan_id.partner_id.name,'may':line.amount})
                
                if line.date.month == 6:
                    if line.amount_residual > 0:
                        res.append({'partner': line.loan_id.partner_id.name,'jun':line.amount_residual})
                    elif line.amount_residual == 0 and line.payment_state != 'paid':
                        res.append({'partner': line.loan_id.partner_id.name,'jun':line.amount})
                
                if line.date.month == 7:
                    if line.amount_residual > 0:
                        res.append({'partner': line.loan_id.partner_id.name,'jul':line.amount_residual})
                    elif line.amount_residual == 0 and line.payment_state != 'paid':
                        res.append({'partner': line.loan_id.partner_id.name,'jul':line.amount})
                
                if line.date.month == 8:
                    if line.amount_residual > 0:
                        res.append({'partner': line.loan_id.partner_id.name,'aug':line.amount_residual})
                    elif line.amount_residual == 0 and line.payment_state != 'paid':
                        res.append({'partner': line.loan_id.partner_id.name,'aug':line.amount})
                
                if line.date.month == 9:
                    if line.amount_residual > 0:
                        res.append({'partner': line.loan_id.partner_id.name,'sep':line.amount_residual})
                    elif line.amount_residual == 0 and line.payment_state != 'paid':
                        res.append({'partner': line.loan_id.partner_id.name,'sep':line.amount})
                
                if line.date.month == 10:
                    if line.amount_residual > 0:
                        res.append({'partner': line.loan_id.partner_id.name,'oct':line.amount_residual})
                    elif line.amount_residual == 0 and line.payment_state != 'paid':
                        res.append({'partner': line.loan_id.partner_id.name,'oct':line.amount})
                
                if line.date.month == 11:
                    if line.amount_residual > 0:
                        res.append({'partner': line.loan_id.partner_id.name,'nov':line.amount_residual})
                    elif line.amount_residual == 0 and line.payment_state != 'paid':
                        res.append({'partner': line.loan_id.partner_id.name,'nov':line.amount})
                
                if line.date.month == 12:
                    if line.amount_residual > 0:
                        res.append({'partner': line.loan_id.partner_id.name,'dec':line.amount_residual})
                    elif line.amount_residual == 0 and line.payment_state != 'paid':
                        res.append({'partner': line.loan_id.partner_id.name,'dec':line.amount})
            
            for previus in rec.loan_line.filtered(lambda l: l.date.year < current_year):
                if previus.amount_residual > 0:
                    # total_prev += previus.amount_residual 
                    res.append({'partner': previus.loan_id.partner_id.name,'previus':previus.amount_residual })
                elif previus.amount_residual == 0 and previus.payment_state != 'paid':
                    # total_prev += previus.amount
                    res.append({'partner': previus.loan_id.partner_id.name,'previus':previus.amount})
            lst1 = []
            for line_next in rec.loan_line.filtered(lambda l: l.date.year > current_year):
                if line_next.date.year == line_next.date.year:
                    if line_next.amount_residual > 0:
                        res2.append(
                            {'partner': line_next.loan_id.partner_id.name,
                             'year':line_next.date.year,
                             'amount':line_next.amount_residua
                            })
                    elif line_next.amount_residual == 0 and line_next.payment_state != 'paid':
                        res2.append(
                            {'partner': line_next.loan_id.partner_id.name,
                             'year':line_next.date.year,
                             'amount':line_next.amount
                            })
                        

        # print('////////////////////////////////////',res2)

       

        for rec in res:
          if rec['partner'] not in result.keys():
            result[rec['partner']] = [rec]
          else:
            result[rec['partner']].append(rec)
        
        for rec in res2:
            if rec['year'] not in dict_year.keys():
                dict_year[rec['year']] = [rec]
            else:
                if res2[0]['year']:
                    dict_year[rec['year']].append(rec)
        # dic = {}
        # for sub in dict_year.values():
        #     print(sub[0])
        # #     for key, ele in sub[0].items():
        # #         dic[key] = ele + dic.get(key, 0)
        
        data = {
            'form_data': self.read()[0],
            'date': self.date,
            'result': result,
            'dict_year': dict_year,
            # 'partner': partner
        } 
        # print('DA>TEEEEEEEEEEEEEE',data)
        return self.env.ref('tn_accrual_invoice_report.report_accrual_invoice').report_action(self, data=data)