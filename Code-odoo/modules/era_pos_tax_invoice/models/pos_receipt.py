from odoo import models, fields, api
from odoo.http import request
import qrcode
import base64
from io import BytesIO


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    
    def generate_qr_code(url):
        qr = qrcode.QRCode(
                 version=1,
                 error_correction=qrcode.constants.ERROR_CORRECT_L,
                 box_size=20,
                 border=4,
                 )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_img = base64.b64encode(temp.getvalue())
        return qr_img

    qr_image = fields.Binary("QR Code", compute='_generate_qr_code')
    qr_in_report = fields.Boolean('إظهار رمز QR',default=True, required=True,)


    def _generate_qr_code(self):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (self._origin.id, self._name)
        self.qr_image = self.generate_qr_code()


    def get_qr_code_data(self):
        customer_name = ""
        customer_vat = ""
        
        sellername = str(self.team_id.partner_id.name)
        seller_vat_no = self.team_id.partner_id.vat or ''
        if self.partner_id.company_type == 'company':
            customer_name = self.partner_id.name
            customer_vat = self.partner_id.vat
    
        currency_id = self.currency_id
        qr_code = " إسم البائع :" + sellername+"\n"
        qr_code += " الرقم الضريبي للبائع :" + seller_vat_no+"\n" if seller_vat_no else " "+"\n"
        qr_code += " التاريخ : " + str(self.date_order)+"\n" if self.date_order else " التاريخ: " + str(self.create_date.date())+"\n"
        qr_code += " الضريبة على القيمة المضافة: " + str(round(self.amount_tax, 2)) +" "+ str(currency_id.symbol)+"\n"
        qr_code += " إجمالي المبلغ المطلوب: " + str(round(self.amount_total, 2))+" "+ str(currency_id.symbol)
        if customer_name:
            qr_code += " | Customer Name: " + customer_name
        if customer_vat:
            qr_code += " | Customer Vat: " + customer_vat
        # print(qr_code)
        return qr_code

    qr_code = fields.Binary(string="QR Code", attachment=True, store=True)
