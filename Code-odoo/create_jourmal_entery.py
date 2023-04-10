


    def action_journal_enteries(self):
        for rec in self:
            line_ids = []
            move = {
                'name': '/',
                'journal_id': rec.journal_id.id,
                'date': fields.date.today(),
                'ref': rec.employee_code,
                'move_type':'entry',
            }
            debit1 = rec.holiday_days
            debit2 = rec.remaining_amount
            credit = debit1 + debit2
            partner_id = self.employee_id.address_id.id

            line_ids +=[(0,0,{
                'account_id': rec.account_holiday_id.id,
                'name': 'Holiday Amount',
                'partner_id': partner_id,
                'debit':debit1,

            }), (0,0,{
                'account_id': rec.account_end_service_id.id,
                'name': 'End Service Amount',
                'partner_id': partner_id,
                'debit':debit2,
            }), 
            (0,0,{
                'account_id': rec.account_id.id,
                'name': 'Main account',
                'partner_id': partner_id,
                'credit': credit,
                })
            ]
            if line_ids:
                move.update({'line_ids':line_ids})
                print('MOVE::::::::', move)
                move_context = self.env['account.move'].with_context(check_move_validity=False)
                move_id = move_context.create(move)
                rec.account_move_id = move_id.id
            return True



def action_entry(self):
    for rec in self:
        move = {
            'name': '/',
            'journal_id': rec.journal_id.id,
            'date': rec.fecha,
            'ref': rec.name,
        }
        line_ids = []
        for line in rec.avg_landed_cost_lines:
            debit = line.average_landed_cost
            credit = line.average_landed_cost

            line_ids += [(0, 0, {
                'name': line.product_id.name or '/',
                'debit': debit,
                'account_id': line.product_id.property_account_expense_id.id,
                'partner_id': rec.order_id.partner_id.id
                }), (0, 0, {
                    'name': line.product_id.name or '/',
                    'credit': credit,
                    'account_id': line.product_id.property_account_income_id.id,
                    'partner_id': rec.order_id.partner_id.id
                    })
                ]
        if line_ids:
            move.update({'line_ids': line_ids})
            move_id = line.env['account.move'].create(move)
            move_id.post()
            rec.write({'state': 'progress', 'move_id': move_id.id})
    return True



 def action_journal_enteries(self):
        for rec in self:
            print('WELLLLLLLLLLLLLLLLLLLLLLLLLLLLLCOME')
            line_ids = []
            move = {
                'name': '/',
                'journal_id': 4,
                'date': fields.date.today(),
                'ref': rec.barcode,
                'move_type':'entry',
            }
            debit = 500
            debit1 = 300

            line_ids +=[(0,0,{
                'account_id': 4,
                'name': 'payslip entery',
                'debit':debit,

            }), (0,0,{
                'account_id': 5,
                'name': 'payslip entery2',
                'debit':debit1,
            }), 
            (0,0,{
                'account_id': 7,
                'name': 'Main account Recive',
                'credit':debit1+debit,
                })
            ]
            print('6666666666666666', line_ids)
            if line_ids:
                move.update({'line_ids':line_ids})
                
                move_context = self.env['account.move'].with_context(check_move_validity=False)
                move_id = move_context.create(move)
                
                move_id.post()
            return True








