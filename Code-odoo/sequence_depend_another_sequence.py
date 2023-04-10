def generate_barcode(self):
        lst = []
        for record in self.env["product.product"].browse(
            self._context.get("active_ids")
        ):
            if not self.overwrite and record.barcode:
                continue

            if self.generate_type == "date":
                bcode = self.env["barcode.nomenclature"].sanitize_ean(
                    "%s%s" % (record.id, datetime.now().strftime("%d%m%y%H%M"))
                )
            elif self.generate_type == "default":
                c = 1
                if lst:
                    c+=int(lst[-1])
                    record.default_code = c
                
                    bcode = str(record.product_tmpl_id.year_id.code) + str(record.product_tmpl_id.barcode_new) + '-' + str(record.default_code)
                    lst.append(record.default_code)
                else:
                    record.default_code = c
                    bcode = str(record.product_tmpl_id.year_id.code) + str(record.product_tmpl_id.barcode_new) + '-' + str(record.default_code)
                    lst.append(record.default_code)
                # print('rrrrrrrrrrrrrrrrr')
                # new_bar = str(record.year_id) + self.env['ir.sequence'].get('product.number') + '-' + self.env[
                #     'ir.sequence'].get('product.code')
                # bcode = str(record.product_tmpl_id.year_id.code) + str(record.product_tmpl_id.barcode_new) # new sequence add barcode + attribyte_value_ids for variant
                # self.env['ir.sequence'].get('product.code') old >>> sequence by product code
               


            else:
                number_random = int("%0.13d" % random.randint(0, 999999999999))
                bcode = self.env["barcode.nomenclature"].sanitize_ean(
                    "%s" % (number_random)
                )
            ean = BytesIO()
            # generate("ean13", u"{}".format(bcode), writer=ImageWriter(), output=ean)
            ean.seek(0)
            jpgdata = ean.read()
            imgdata = base64.encodebytes(jpgdata)
            record.write({"barcode": bcode, "barcode_img": imgdata})
        return True
