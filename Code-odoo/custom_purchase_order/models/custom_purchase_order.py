# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import timedelta, datetime, date


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    

    state2 = fields.Selection([
        ('draft', 'New'),
        ('sent_rfq', 'Sent RFQ'),
        ('submit', 'Procurment and Contract'),
        ('procurment', 'Project Mananger'),
        ('project', 'Supply Chain Manager'),
        ('supply_chain', 'Chief Executive Officer'),
        ('ceo_approve', 'Confirm Purchase Order')],
        default='draft',
        tracking=True
    )
    retained_status = fields.Selection([
        ('no', 'Nothing to Retained'),
        ('to_retained', 'Availble Retained'),
    ], string='Retained Warrenty Status',compute='compute_retained_warnty', store=True)

    # in_project = fields.Boolean(
    #     string='In Project',
    # )
   
    is_requisition = fields.Boolean(
        string='Is Requisition',
        compute='_compute_agreement_powkf',
        store=True,
    )

    retained_warranty = fields.Float(
        string='Retained warranty %',
    )
    percentage = fields.Float(
        string='Percentage %',
    )
    account_move_id = fields.Many2one(
        'account.move',
        string='Account Move',
    )
    project_id = fields.Many2one(
        'project.manager',
        string='Project'
    )
    
    analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account'
    )
    
    
    def action_rfq_send(self):
        for rec in self:
            if rec.is_requisition == True:
                rec.state2 = 'sent_rfq'
        return super(PurchaseOrder, self).action_rfq_send()
   
    
    def button_submit(self):
        for rec in self:
            rec.state2 = 'submit'
            rec.state= 'draft'

    def button_procurment_contract(self):
        for rec in self:
            rec.state2 = 'procurment'

    def button_project_manager(self):
        for rec in self:
            rec.state2 = 'project'

    def button_supply_chain_manager(self):
        for rec in self:
            supply_amount = self.env['ir.config_parameter'].sudo().get_param('custom_purchase_order.supply_amount')
            if rec.amount_total < float(supply_amount):
                rec.button_confirm()
                rec.state2 = 'ceo_approve'
            else:
                rec.state2 = 'supply_chain'
            

    def button_chief_execute_officer(self):
        for rec in self:
            supply_amount = self.env['ir.config_parameter'].sudo().get_param('custom_purchase_order.supply_amount')
            if rec.amount_total >= float(supply_amount):
                rec.button_confirm()
                rec.state2 = 'ceo_approve'
            
   
    @api.onchange('retained_warranty', 'order_line')
    def _onchange_retained(self):
        for rec in self:
            for line in rec.order_line:
                line.retained_warranty = rec.retained_warranty
    
    @api.depends('order_line.qty_invoiced', 'order_line.qty_retained')
    def compute_retained_warnty(self):
        for rec in self:
            for line in rec.order_line:
                if line.qty_invoiced >= line.qty_retained:
                   rec.retained_status = 'to_retained'
                   line.qty_retained = line.qty_invoiced - line.qty_retained
                if line.qty_invoiced ==0:
                    line.qty_retained = 0

    @api.depends('requisition_id')
    def _compute_agreement_powkf(self):
        for rec in self:
            if rec.requisition_id:
                rec.is_requisition = True
            else:
                rec.is_requisition = False
            
                	

    def action_retained_warranty(self):
    # self.write({'stage_id': '2'})
    # self.write({'driver_custody': True})
        for record in self:
            for line in record.order_line:
                move = self.env['account.move'].create([
                    {
                        'move_type': 'in_invoice',
                        # 'invoice_date': record.Date.context_today(self),
                        'partner_id': record.partner_id.id,
                        'currency_id': record.currency_id.id,
                        # 'amount_total': record.delivery_total,
                        'invoice_line_ids': [
                            (0, 0, {
                                'product_id': line.product_id.id,
                                'name': 'Delivery Service Reverse Warntey ',
                                'quantity': line.qty_invoiced,
                                'price_unit': line.price_unit/ line.retained_warranty,
                                # 'purchase_line_id': line.id

                            }),
                        ],
                    },
                ])
                line.qty_retained +=1
                record.retained_status = 'no'             
        return self.action_view_invoice(move)

    # def action_create_invoice(self):
    #     res = super(PurchaseOrder, self).action_create_invoice()
    #     for rec in self:
    #         po_ids = self.env['account.move'].search(['&',('ac_purchase_id', '=', rec.id),('is_payment', '=', True)])
    #         rec.account_move_id = po_ids.id
    #     return res

    def _prepare_invoice(self):
        res = super(PurchaseOrder, self)._prepare_invoice()
        res.update({
            'ac_purchase_id':self.id,
            })
        return res



class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    retained_warranty = fields.Float(
        string='Retained warranty %', 
        store=True
    )
    # in_project = fields.Boolean(
    #     string='In Project',
    # )
    is_requisition = fields.Boolean(
        string='IS Requisition',
    )
    qty_retained = fields.Float(
        string='Qty Retained',
    )

 

    #Replace the method _prepare_account_move_line
    def _prepare_account_move_line(self, move=False):
        self.ensure_one()
        aml_currency = move and move.currency_id or self.currency_id
        date = move and move.date or fields.Date.today()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': '%s: %s' % (self.order_id.name, self.name),
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'price_unit': self.currency_id._convert(self.price_unit, aml_currency, self.company_id, date, round=False),
            'tax_ids': [(6, 0, self.taxes_id.ids)],
            'analytic_account_id': self.order_id.project_id.acc_analytic_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'discount':self.discount,
            'purchase_line_id': self.id,
        }
        if not move:
            return res

        if self.currency_id == move.company_id.currency_id:
            currency = False
        else:
            currency = move.currency_id

        res.update({
            'move_id': move.id,
            'currency_id': currency and currency.id or False,
            'date_maturity': move.invoice_date_due,
            'partner_id': move.partner_id.id,
        })
        return res
   