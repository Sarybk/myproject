# -*- coding: utf-8 -*-

import base64
import io
from odoo import models


class AcrrualInvoiceXLSX(models.AbstractModel):
    _name = 'report.tn_accrual_invoice_report.accrual_invoice_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        total_prv_year = 0
        total_next_year = 0
        total_jan = 0
        total_feb = 0
        total_mar = 0
        total_apr = 0
        total_may = 0
        total_jun = 0
        total_jul = 0
        total_aug = 0
        total_sep = 0
        total_oct = 0
        total_nov = 0
        total_dec = 0
        center = workbook.add_format({'align': 'center'})
        format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})
        format_1 = workbook.add_format({'bold': True, 'align': 'center'})

        sheet = workbook.add_worksheet('Rental Contarct')
        row = 7
        col = 2
        c = 0
        sheet.set_column('C:C',15)
        sheet.set_column('D:D',20)

        sheet.write(row-3, col, 'Date:'+' '+data['date'], center)
        sheet.merge_range(row-3, col+15, row-3, col+1, 'Accrual Invoice', format_1)
        sheet.write(row, col, 'Customer', format)
        sheet.write(row, col+1, 'Previouse balance', format)
        sheet.write(row, col+2, 'Jan', format)
        sheet.write(row, col+3, 'Feb', format)
        sheet.write(row, col+4, 'Mar', format)
        sheet.write(row, col+5, 'Apr', format)
        sheet.write(row, col+6, 'May', format)
        sheet.write(row, col+7, 'Jun', format)
        sheet.write(row, col+8, 'Jul', format)
        sheet.write(row, col+9, 'Aug', format)
        sheet.write(row, col+10, 'Sep', format)
        sheet.write(row, col+11, 'Oct', format)
        sheet.write(row, col+12, 'Nov', format)
        sheet.write(row, col+13, 'Dec', format)
        for ky in data['dict_year'].keys():
            c+=1
            col2 = 15
            sheet.write(row, col2+c, ky, format)
       
        for k in data['result'].keys():
            row+=1
            sheet.write(row, col, k, center)
            sheet.write(row+1,col, 'Total', center)
            previus = [line['previus'] for line in data['result'][k] if k == line['partner'] if 'previus' in line]
            sheet.write(row, col+1, sum(previus), center)
            for line in data['result'][k]:
                if k == line['partner']:
                    if 'jan' in line:
                        sheet.write(row, col+2, line['jan'], center)
                        total_jan+= line['jan']
                        sheet.write(row+1, col+2, total_jan, center)
                    
                    if 'feb' in line:
                        sheet.write(row, col+3, line['feb'], center)
                        total_feb+= line['feb']
                        sheet.write(row+1, col+3, total_feb, center)
                    
                    if 'mar' in line:
                        sheet.write(row, col+4, line['mar'], center)
                        total_mar+= line['mar']
                        sheet.write(row+1, col+4, total_mar, center)
                    
                    if 'apr' in line:
                        sheet.write(row, col+5, line['apr'], center)
                        total_apr+= line['apr']
                        sheet.write(row+1, col+5, total_apr, center)
                    
                    if 'may' in line:
                        sheet.write(row, col+6, line['may'], center)
                        total_may+= line['may']
                        sheet.write(row+1, col+6, total_may, center)
                    
                    if 'jun' in line:
                        sheet.write(row, col+7, line['jun'], center)
                        total_jun+= line['jun']
                        sheet.write(row+1, col+7, total_jun, center)
                    
                    if 'jul' in line:
                        sheet.write(row, col+8, line['jul'], center)
                        total_jul+= line['jul']
                        sheet.write(row+1, col+8, total_jul, center)
                    
                    
                    if 'aug' in line:
                        sheet.write(row, col+9, line['aug'], center)
                        total_aug+= line['aug']
                        sheet.write(row+1, col+9, total_aug, center)
                    
                    if 'sep' in line:
                        sheet.write(row, col+10, line['sep'], center)
                        total_sep+= line['sep']
                        sheet.write(row+1, col+10, total_sep, center)

                    if 'oct' in line:
                        sheet.write(row, col+11, line['oct'], center)
                        total_oct+= line['oct']
                        sheet.write(row+1, col+11, total_oct, center)
                    
                    if 'nov' in line:
                        sheet.write(row, col+12, line['nov'], center)
                        total_nov+= line['nov']
                        sheet.write(row+1, col+12, total_nov, center)
                    
                    if 'dec' in line:
                        sheet.write(row, col+13, line['dec'], center)
                        total_dec+= line['dec']
                        sheet.write(row+1, col+13, total_dec, center)

            for ky in data['dict_year'].keys():
                next_year =sum([line['amount'] for line in data['dict_year'][ky] if str(line['year']) in ky if k == line['partner']])
                c+=1
                col2 = 13
                sheet.write(row, col2+c, next_year, center)
                total_year = sum([line['amount'] for line in data['dict_year'][ky]])
                total_next_year=total_year
                sheet.write(row+1, col2+c, total_next_year, center)
                    
                    

            # sheet.write(row, col, 'Ali', center)
            # sheet.write(row, col+1, '2019', center)
            # sheet.write(row, col+2, '1', center)
            # sheet.write(row, col+3, '2', center)
            # sheet.write(row, col+4, '3', center)
            # sheet.write(row, col+5, '4', center)
        # center = workbook.add_format({'center': True})
        # format_1 = workbook.add_format({'center': True, 'align': 'center', 'bg_color': 'yellow'})

        # for obj in patients:
        #     sheet = workbook.add_worksheet(obj.name)
        #     row = 3
        #     col = 3
        #     sheet.set_column('D:D',20)
        #     sheet.set_column('E:E', 10)

        #     row+=1
        #     sheet.merge_range(row, col, row, col+1, 'ID Card', format_1)

        #     row += 1
        #     if obj.image:
        #         patient_image = io.BytesIO(base64.b64decode(obj.image))
        #         sheet.insert_image(row, col, "image.png", {'image_data': patient_image, 'x_scale': 0.5, 'y_scale': 0.5})

        #         row += 6
        #     sheet.write(row, col, 'Name', center)
        #     sheet.write(row, col + 1, obj.name)
        #     row += 1
        #     sheet.write(row, col, 'Age', center)
        #     sheet.write(row, col + 1, obj.age)
        #     row += 1
        #     sheet.write(row, col, 'Reference', center)
        #     sheet.write(row, col + 1, obj.reference)

        #     row += 2
        #     sheet.merge_range(row, col, row + 1, col + 1, '', format_1)





