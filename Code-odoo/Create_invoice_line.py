 @api.onchange('is_payment')
    def _onchange_invoice_line(self):
        result = []

        for rec in self:
            if rec.is_payment == True:

               result.append((0, 0, rec._prepare_invice_line()))
               print(result, '7777777777777777777777')
               rec.invoice_line_ids = result
               rec._onchange_invoice_line_ids()
               rec._onchange_recompute_dynamic_lines()
               rec._onchange_tax_totals_json()
               # rec.line_ids = result
               # rec._onchange_invoice_line_ids()
               # # rec._onchange_recompute_dynamic_lines()
               # rec._onchange_tax_totals_json()

                line._get_computed_taxes()
                line._onchange_mark_recompute_taxes()
                line._onchange_mark_recompute_taxes_analytic()
                # line._onchange_product_id()
                line._onchange_uom_id()
                line._onchange_account_id()
                line._onchange_debit()
                line._onchange_credit()
                line._onchange_amount_currency()
                line._onchange_currency()


                                   
                   


    # def _prepare_account_invoice_line(self, move=False):
    #     for line in self.ac_purchase_id.order_line:
    #         aml_currency = move and move.currency_id or line.currency_id
    #         date = move and move.date or fields.Date.today()
    #         res = {
    #             'display_type': line.display_type,
    #             'sequence': line.sequence,
    #             'name': '%s: %s' % (line.order_id.name, line.name),
    #             'product_id': line.product_id.id,
    #             'product_uom_id': line.product_uom.id,
    #             'quantity': line.qty_to_invoice,
    #             'account_id': 2,
    #             'price_unit': line.currency_id._convert(line.price_unit, aml_currency, line.company_id, date, round=False),
    #             'tax_ids': [(6, 0, line.taxes_id.ids)],
    #             'analytic_account_id': line.account_analytic_id.id,
    #             'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
    #             'purchase_line_id': line.id,
    #             'move_id': self.id
    #         }
    #         if not move:
    #             return res

    #         if line.currency_id == move.company_id.currency_id:
    #             currency = False
    #         else:
    #             currency = move.currency_id

    #         res.update({
    #             'move_id': move.id,
    #             'currency_id': currency and currency.id or False,
    #             'date_maturity': move.invoice_date_due,
    #             'partner_id': move.partner_id.id,
    #         })
    #         return res

    @api.onchange('ac_purchase_id')
    def _onchange_field_name(self):
        for rec in self.invoice_line_ids:
            rec.price_unit = 50.00
        
    

    def create_invoice_line(self):
        print('WELOCOM/////////////////////////////')
        vals = []
        for operation in self.ac_purchase_id.order_line:
                # if group:
                #     name = repair.name + '-' + operation.name
                # else:
                #     name = operation.name
            
            account = operation.product_id.property_account_expense_id
            if not account:
                raise UserError(_('No account defined for product "%s".', operation.product_id.name))

            invoice_line_vals = {
                'product_id': operation.product_id.id,
                'account_id': account.id,
                'quantity': operation.product_uom_qty,
                'tax_ids': [(6, 0, operation.taxes_id.ids)],
                'product_uom_id': operation.product_uom.id,
                'price_unit': operation.price_unit,
                'purchase_line_id': operation.id,
            }

            if operation.company_id.currency_id:
                balance = (operation.product_uom_qty * operation.price_unit)
                invoice_line_vals.update({
                    'debit': balance > 0.0 and balance or 0.0,
                    'credit': balance < 0.0 and -balance or 0.0,
                })
            else:
                amount_currency = (operation.product_uom_qty * operation.price_unit)
                balance = currency._convert(amount_currency, company.currency_id, company, fields.Date.today())
                invoice_line_vals.update({
                    'amount_currency': amount_currency,
                    'debit': balance > 0.0 and balance or 0.0,
                    'credit': balance < 0.0 and -balance or 0.0,
                    'currency_id': currency.id,
                })
            vals.append((0, 0, invoice_line_vals))
        self.invoice_line_ids = vals
