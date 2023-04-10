from itertools import compress

def creare_crm_visitor(self):
        for rec in self:
            list_week = [1, 2, 3, 4, 5, 6, 7]
            days = [rec.sun, rec.mon, rec.tue, rec.wed, rec.thu, rec.fri, rec.sat]
            lst_order = list(compress(list_week, days))
            print('lst_orderlst_order', lst_order)
            lst = {
                'name': rec.contract_type_id.name,
                'partner_id': rec.partner_id.id,
                'driver_id' : rec.driver_id.id,
                'contract_type_id': rec.contract_type_id.id,
                'sale_order_id': rec.id,
            }
            for lin in lst_order:
                visit = self.env['crm.visitor'].create(lst)
                visit._onchange_consumable_product()
                visit._onchange_optional_product()
            return visit