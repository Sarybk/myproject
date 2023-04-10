def action_show_invoice_customer(self):
        for rec in self:
            invoic_action = self.env.ref('account.action_move_out_invoice_type')
            invoic_action = invoic_action.read()[0]
            invoic_action['domain'] = str([('ref','=',rec.name)])
        return invoic_action




 @api.depends('is_contract')
    def _compute_customer_invoiced(self):
        for order in self:
            order.crm_invoice_count = self.env['account.move'].search_count([('ref', '=', order.name)])