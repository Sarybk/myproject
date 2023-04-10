
#Create record in field attachment_id 
#Sorry, you are not allowed to process this document.
 #Solve issue upload atachment in create record
#@attachments that are uploaded on a record that isn't saved yet are
#@created with res_id set to 0. In the case of attachments linked through
#@a m2m rather than the usual (res_model, res_id), 
@api.model
def create(self, vals):
    templates = super(HrEmployeeDocument,self).create(vals)
    # fix attachment ownership
    for template in templates:
        if template.doc_attachment_id:
            template.doc_attachment_id.write({'res_model': self._name, 'res_id': template.id})
    return templates