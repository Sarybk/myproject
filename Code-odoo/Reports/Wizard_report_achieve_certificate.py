# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _
from odoo.exceptions import ValidationError



class AchivementCertificate(models.TransientModel):
    """Defining TransientModel to move standard."""

    _name = 'achive.certificate'
    _description = "Achivement Certificate"

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To') 
    select_custom = fields.Selection([('cutom', 'Customer'), ('all', 'All Customers')])
    partner_id = fields.Many2many('res.partner', string='Customer')

  
    def action_print(self):
        domain = []
        partner_id = self.partner_id
        # print(prtner_id)
        if partner_id:
            domain+=[('partner_id', 'in', partner_id.ids)]
        date_from = self.date_from
        if date_from:
            domain+=[('date', '>=', date_from)]
        date_to = self.date_to
        if date_to:
            domain+=[('date', '<=', date_to)]

        visitors = self.env['crm.visitor'].search(domain)
        visitor_lst = []
        option_lst = []
        result = {}
        result2 = {}
        lst = []
        lst2 = []

        point_group = visitors.visit_line_ids.read_group(domain=domain, fields=['product_qty'], groupby=['product_id','partner_id'],lazy=False)
        option_group = visitors.visit_option_ids.read_group(domain=domain, fields=['product_qty'], groupby=['product_id','partner_id'],lazy=False)

        for point in point_group:
            product_id = point.get('product_id')
            partner_id = point.get('partner_id')
            total = point['product_qty']
            product_name = self.env['product.product'].browse(product_id[0])
            partner_name = self.env['res.partner'].browse(partner_id[0])
            lst.append({
                'partner_id':partner_name.name,
                'product_id':product_name.name,
                'uom_id': visitors.visit_line_ids.mapped('uom_id').name,
                'total':  point['product_qty'],
            })

        for option in option_group:
            product_id = option.get('product_id')
            partner_id = option.get('partner_id')
            total = option['product_qty']
            product_name = self.env['product.product'].browse(product_id[0])
            if partner_id:
               partner_name = self.env['res.partner'].browse(partner_id[0])
            lst2.append({
                'partner_id':partner_name.name,
                'product_id':product_name.name,
                'uom_id': visitors.visit_option_ids.mapped('uom_id').name,
                'total':  option['product_qty'],
            })


        # # for visitor in visitors:
        # for vis in visitors:
        #      point_group =  vis.visit_line_ids.read_group(domain=[('order_id.partner_id', '=', self.partner_id.id)], fields=['product_qty'], groupby=['product_id'])
        #      for point in point_group:
        #           print('POOOOOO', point)
        #           product_id = point.get('product_id')
        #           total = point['product_qty']
        #           # print(product_rec.id, '88888888888', total)
        #           product_name = self.env['product.product'].browse(product_id[0])
        #           vals = {
        #               'partner_id': vis.partner_id.name,
        #               'product_id':product_name.name,
        #               # 'uom_id': line.uom_id.name,
        #               'total':  point['product_qty'],
        #           }
        #           lst.append(vals)
        # print(lst)
                
               
                # vals = {
                #     'partner_id': visitor.partner_id.name,
                #     'product_id': line.product_id.name,
                #     'uom_id': line.uom_id.name,
                #     'product_qty': line.product_qty,
                # }
                # visitor_lst.append(vals)

        #     for option in visitor.visit_option_ids:
        #         vals = {
        #             'partner_id': visitor.partner_id.name,
        #             'product_id': option.product_id.name,
        #             'uom_id': option.uom_id.name,
        #             'product_qty': option.product_qty,
        #         }
        #         option_lst.append(vals)

        
        # dict_lst = visitor_lst + option_lst
        # print(dict_lst)
        
        res = lst+lst2
        if not res:
          raise ValidationError(_("There is no point of sales in these date!")) 
        for rec in res:
          if rec['partner_id'] not in result.keys():
            result[rec['partner_id']] = [rec]
          else:
            result[rec['partner_id']].append(rec)
        print('RESULT:::::::::::::::::', result)

        
            


        data = {
            'form_data': self.read()[0],
            'result': result,
        } 
        return self.env.ref('crm_visitor.report_achive_certificate').report_action(self, data=data)






















     
        # data = {
        #     'form_data': self.read()[0],
        # }   
        # # data = {
        # #     'result': result,
        # #     'prod_line': dic_line,
        # #     'date_from': self.date_from,
        # #     'date_to': self.date_to,
        # # }

        # # print(data, '444444444444444444444444444444444444444444444444444')
        # return self.env.ref('crm_visitor.report_achive_certificate').report_action(self, data=data)





            # done = set()
        # lst = []
        # for d in dict_lst:
        #     if d['product_id'] not in done:
        #         done.add(d['product_id'])  # note it down for further iterations
        #         lst.append(d)

        # for rec in res:
        #   if rec['product_id'] not in result2.keys():
        #     result2[rec['product_id']] = [rec]
        #   else:
        #     result2[rec['product_id']].append(rec)
        # print('5555555', result2)



  # def get_customer(self):
  #       self._cr.execute(""" SELECT res.id
  #               FROM crm_visitor visit, res_partner res
  #               where visit.partner_id = res.id
  #               group by res.id 
  #           """)
  #       res = self._cr.dictfetchall() or False

  #       lst = [list(record.values())[0] for record in res]
  #       return tuple(lst)



   # # All Customers
   #      # for rec in self.partner_id:

   #      if self.date_from and self.date_to and self.select_custom =='all':
   #          self._cr.execute("""SELECT res.name as res, templ.name, visit_line.product_qty
   #                  From  crm_visitor visitor, crm_visitor_line visit_line, product_product product, product_template templ, res_partner res
   #                  where visitor.id = visit_line.order_id AND visit_line.product_id = product.id AND product.product_tmpl_id = templ.id AND
   #                   visitor.partner_id = res.id AND visitor.date >= %s AND  visitor.date <= %s AND visitor.partner_id in %s ;
   #          """,(self.date_from, self.date_to,self.get_customer()))

   #      elif self.date_from and self.date_to:
   #          self._cr.execute(""" SELECT res.name as res, templ.name, visit_line.product_qty
   #                  From  crm_visitor visitor, crm_visitor_line visit_line, product_product product, product_template templ, res_partner res
   #                  where visitor.id = visit_line.order_id AND visit_line.product_id = product.id AND product.product_tmpl_id = templ.id AND
   #                   visitor.partner_id = res.id AND visitor.date >= %s AND  visitor.date <= %s AND visitor.partner_id = %s ;
   #          """,(self.date_from, self.date_to, self.partner_id.id))
   #      res = self._cr.dictfetchall()
   #      return res

   #  def get_option_product(self):

   #      # All Customers
   #      # for rec in self.partner_id:

   #      if self.date_from and self.date_to and self.select_custom =='all':
   #          self._cr.execute(""" SELECT res.name as res, templ.name , option_line.product_qty
   #                  From  crm_visitor visitor,crm_visitor_option option_line, product_product product, product_template templ, res_partner res
   #                  where visitor.id =option_line.option_id AND visitor.partner_id = res.id AND option_line.product_id = product.id AND 
   #                  product.product_tmpl_id = templ.id AND visitor.date >= %s AND  visitor.date <= %s AND visitor.partner_id = %s ;
   #          """,(self.date_from, self.date_to, self.partner_id.id))
   #      res = self._cr.dictfetchall()
   #      return res


   #  def action_print(self):
        # result = {}
        # dic_line = {}
        # res = self.get_certificate_customer()
        # print(res, 'REEEEEEEEEEEEEEEEEEEEEEEE')
        # lst2 = self.get_option_product()
        # res.extend(lst2)
        

        # for rec in res:
        #     # print(rec, 'REEEEEEEEEEEEEEEEEEEEEEEE')
        #     if rec['res'] not in result.keys():
        #         result[rec['res']] = [rec]
        #     else:
        #         result[rec['res']].append(rec)

        # for prod in res:
        #     if prod['name'] not in dic_line.keys():
        #         dic_line[prod['name']] = [prod]
        #         # print('recccccccc', result[rec['res']] )
        #     else:
        #          dic_line[prod['name']].append(prod)

        # for option in res2:
        #     if option['name'] not in result2.keys():
        #         result2[option['name']] = [option]
        #         # print('recccccccc', result[rec['res']] )
        #     else:
        #          result2[option['name']].append(option)
        # print('OPPPPPPPPPPPP', result2)
     