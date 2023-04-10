
from odoo import api, fields, models, Command, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_compare, float_is_zero, date_utils, email_split, email_re, html_escape, is_html_empty
from odoo.tools.misc import formatLang, format_date, get_lang

from datetime import date, timedelta
from collections import defaultdict
from contextlib import contextmanager
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import ast
import json
import re
import warnings
class AccountMove(models.Model):


    _inherit = "account.move"

    payment_select = fields.Selection([
        ('first_payment', 'First Payment'),
        ('percent', 'Percentage%'),
        ('amount', 'Amount')], default='percent'
    )
    percentage  = fields.Float(
        string='Percentage',
    )
    fixed_amount = fields.Float(
        string='Fixed Amount',
    )
    is_payment = fields.Boolean('Advance Payment') # Advance Payment for Vendor Bill 

    is_first_paied = fields.Boolean(
        string='First Paied',
    )

    adv_payment = fields.Float(
        string='Advance Payment',
        compute="compute_all_payment",
        store=True,
       
    )

    discount_po = fields.Float(
        string='Discount',
    )
    retention = fields.Float(
        string='Retention',
    )

    net_invoice = fields.Float(
        string='Net Invoice',
    )
   
    ac_payment_id = fields.Many2one(
        'account.payment',
        string='Account Payment',
    )

    ac_purchase_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
    )
    # Total of Purchase Order line 
    purchase_amount = fields.Monetary(
        string='Purchase Amount',
        related='ac_purchase_id.amount_total',
    )
    purchase_untax_amount = fields.Float(
        string='Purchase Untax amount',
    )

    
    # test = fields.Boolean(
    #     string='Paied amount total',
    # )
    payment_total = fields.Float(
        string='Payment Total',
    )
    tax_id = fields.Many2one(
        'account.tax',
        string='Taxes',
    )
    advance_pay = fields.Float(
        string='Advance Payment',
    )
    is_invoiced = fields.Boolean(
        string='Create invoice',
    )
    



    @api.onchange('percentage')
    def _onchange_percentage(self):
        if self.ac_purchase_id:
            self.ac_purchase_id.percentage = self.percentage

        

    # @api.model
    # def default_get(self, value):
    # 	res = super(AccountMove, self).default_get(value)

    # 	for rec in self:
    # 		acc = rec.env['account.move'].search(['&',('purchase_id', '=', rec.ac_purchase_id.id),('is_payment', '=', True)])
    # 		rec.account_mv_id = acc.id
    # 	return res

    @api.onchange('ac_purchase_id', 'sale_order_id')
    def _onchange_untax_amount(self):
        for rec in self:
            if rec.purchase_amount:
                rec.purchase_untax_amount = rec.purchase_amount/1.15
                rec.ac_purchase_id.percentage = rec.percentage


    def percentage_validate(self):
        if self.percentage == 0:
            raise ValidationError(_("The percentage must be greater than zero!"))
    
    def invoice_line_validate(self):
        if self.invoice_line_ids:
            raise ValidationError(_("Already created invoice line"))

    def purchase_order_validate(self):
        if not self.ac_purchase_id:
            raise ValidationError(_("Select Purchase order before create"))



    def create_invoice_line(self):
        if self.move_type == 'in_invoice':
            self.create_bills_payemnt()
       

    def create_bills_payemnt(self):
        payment_product = self.env['ir.config_parameter'].sudo().get_param('custom_purchase_order.payment_product_id') or False
        retantion_product = self.env['ir.config_parameter'].sudo().get_param('custom_purchase_order.retantion_product_id') or False
        product = self.env['product.product']
        operation = self.ac_purchase_id.order_line
        price_rt_tax = 0
        price_adv_work = 0
        # print('ggggggggggggg', self.is_invoiced)
        if self.is_payment:
            self.advance_pay = (self.purchase_untax_amount*self.percentage) / 100
            self.invoice_line_validate()
            self.purchase_order_validate()
            self.percentage_validate()
        elif not self.is_payment and self.invoice_line_ids:
            self.advance_pay = self.invoice_line_ids.price_subtotal
            price_rt_tax+= self.advance_pay*self.ac_purchase_id.retained_warranty/100
            price_adv_work+= (self.advance_pay*self.ac_purchase_id.percentage) / 100 

        lst = [payment_product, retantion_product]
        lst2 = []
        vals = []
        c = 0
        if self.is_payment:
            lst2.append(lst[0])
        else:
            lst2 = lst
        
        for line in lst2:
            product_id = product.browse(int(line))
            c+=1
        # for operation in self.ac_purchase_id.order_line:
                # if group:
                #     name = repair.name + '-' + operation.name
                # else:
                #     name = operation.name
            account = product_id.property_account_expense_id
            if not account:
                raise UserError(_('No account defined for product "%s".', product_id.name))
            
            if line:                
                invoice_line_vals = {
                    'product_id': product_id.id,
                    'account_id': product_id.property_account_expense_id.id,
                    'analytic_account_id': self.ac_purchase_id.project_id.acc_analytic_id.id,
                    # 'quantity': operation.product_uom_qty,
                    'tax_ids': [(6, 0, operation.taxes_id.ids)],
                    'product_uom_id': product_id.uom_po_id.id,
                    'price_unit': self.advance_pay,
                    # 'purchase_line_id': operation.id,
                }

                if operation.company_id.currency_id:
                    balance = (operation.product_uom_qty * operation.price_unit)
                    invoice_line_vals.update({
                        'debit': balance > 0.0 and balance or 0.0,
                        'credit': balance < 0.0 and -balance or 0.0,
                    })
                # else:
                #     amount_currency = (operation.product_uom_qty * operation.price_unit)
                #     balance = currency._convert(amount_currency, company.currency_id, company, fields.Date.today())

                #         invoice_line_vals.update({
                #             'amount_currency': amount_currency,
                #             'debit': balance > 0.0 and balance or 0.0,
                #             'credit': balance < 0.0 and -balance or 0.0,
                #             'currency_id': currency.id,
                #         })
                if not self.is_payment:
                    if c == 1:
                         invoice_line_vals.update({
                            'price_unit': -price_adv_work,  
                        })

                    if c == 2:
                         invoice_line_vals.update({
                            'price_unit': -price_rt_tax, 
                            'tax_ids': False 
                        })


                vals.append((0, 0, invoice_line_vals))
        self.invoice_line_ids = vals
        self.compute_all_payment()


    
    @api.depends('ac_purchase_id', 'adv_payment', 'amount_total')
    def compute_all_payment(self):
    	for move in self:
            if move.ac_purchase_id.requisition_id:
                if move.move_type == 'in_invoice' and move.is_payment == True:
                    move.adv_payment = move.advance_pay
                    move.net_invoice = move.amount_total

               

            # ========= Create invoice from Purchase  Order ================================
                if move.move_type == 'in_invoice' and move.is_payment == False:
                    if move.invoice_line_ids:
                        move.adv_payment = [-line.price_unit for line in self.invoice_line_ids][1]
                        move.retention = (move.advance_pay*move.ac_purchase_id.retained_warranty)/100
                        move.net_invoice = move.amount_total

                        # percentage = (move.ac_purchase_id.account_move_id.percentage/100)*move.ac_purchase_id.account_move_id.adv_payment
                        # move.adv_payment = move.ac_purchase_id.account_move_id.adv_payment-percentage

                        

                    # if move.ac_purchase_id.account_move_id.payment_select == 'amount': 
                    #     move.adv_payment = move.ac_purchase_id.account_move_id.adv_payment - move.ac_purchase_id.account_move_id.fixed_amount
                    # # move.retention = move.ac_purchase_id.retained_warranty
                    #     move.discount_po = move.ac_purchase_id.discount_rate 
                    #     total = 0.0
                    #     for line in move.ac_purchase_id.order_line:
                    #         if line.price_unit > 0:
                    #             total+= line.price_unit/(line.retained_warranty/100)
                    #         move.retention = total
                    #     move.payment_total = move.adv_payment - move.retention

    # def _compute_amount(self):
    #     res = super(AccountMove, self)._compute_amount()
    #     for rec in self:
    #         rec.amount_total =  rec.amount_total - rec.payment_total
    #         rec.net_invoice = rec.amount_total         
    #     return res








  # def _prepare_invice_line(self):
    #     payment_product = self.env['ir.config_parameter'].sudo().get_param('custom_purchase_order.payment_product_id') or False
    #     tax_product = self.env['ir.config_parameter'].sudo().get_param('custom_purchase_order.tax_product_id') or False
    #     retantion_product = self.env['ir.config_parameter'].sudo().get_param('custom_purchase_order.retantion_product_id') or False
    #     product = self.env['product.product']
    #     # print('PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP', product.property_account_expense_id)
    #     lst = [payment_product, tax_product, retantion_product]
    #     for line in lst:
    #         if line:
    #             product_id = product.browse(int(line))
    #             dict_line = {
    #                      'product_id':product_id.id,
    #                      'account_id': product_id.property_account_expense_id.id,
    #                      # 'price_unit': 100.00,
    #                      'move_id': self.id
    #             }
    #             return dict_line






      #   		if mov.payment_select == 'first_payment':
    		# 		mov.adv_payment = mov.amount_total
      #               mov.net_invoice = mov.adv_payment
      #   		if mov.payment_select == 'percent':
      #   			mov.adv_payment = (mov.percentage/100)*mov.amount_total
      #   		if mov.ac_payment_id.payment_select == 'amount':
      #   			mov.adv_payment = move.amount_total - mov.amount                  
    		# 		# print('*********************Stop*********************')
    		# mov.retention = mov.ac_purchase_id.retained_warranty
    		# mov.discount_po = mov.ac_purchase_id.discount_rate
    		# mov.net_invoice = mov.amount_total - mov.adv_payment - mov.retention - mov.discount_po

   


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_create_invoice(self):
        res = super(PurchaseOrder, self).action_create_invoice()
        if self.requisition_id:
            obj_move = self.env['account.move'].browse(res['res_id'])
            obj_move.is_invoiced = True
            obj_move.create_invoice_line()
        # print('888888888888888888888888888888888888SARY', obj_move)
        return res

   
   
    

   
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"


    # purchase_id = fields.Many2one(
    #     'purchase.order',
    #     string='Purchase Order',
    # )

