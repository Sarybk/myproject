 def action_register_payment(self):
        res = super(AccountMove, self).action_register_payment()
        res['context']['default_communication'] = ', '.join(rec.virtual_ref for rec in self)
        return res
