



#Compining duplicate product and get total product qty per product and groupby product and partner 
#code 1
point_group = visitors.visit_line_ids.read_group(domain=domain, fields=['product_qty'], groupby=['product_id','partner_id'],lazy=False)

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


#code2
for mapp in visitors.visit_line_ids.mapped('product_id'):
            total = 0.0
            for line in visitors.visit_line_ids:
                if mapp == line.product_id.id:
                   total += line.product_qty
                   print('PRODUCTttttttttttttt', line.product_qty)
            lst.append({'product_id':mapp.name,'product_qty': total})
        print(lst)