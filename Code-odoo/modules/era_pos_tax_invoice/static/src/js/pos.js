odoo.define('era_tax_invoice.OrderReceipt', function(require) 
{
    'use strict';

    const OrderReceipt = require('point_of_sale.OrderReceipt');
    const Registries = require('point_of_sale.Registries');

//    models.load_fields('pos.config',['allow_qr_code']);
    var rpc = require('web.rpc');
    var module = require('point_of_sale.models');
    var models = module.PosModel.prototype.models;

    for(var i=0; i<models.length; i++){
        var model=models[i];
        if(model.model === 'res.partner'){
             model.fields.push('street');
             model.fields.push('street2');
             model.fields.push('city');
             model.fields.push('state_id');
             model.fields.push('country_id');

             // other field you want to pull from the res.company table.

        }

    }
    const PosQRCodeOrderReceipt = OrderReceipt =>
        class extends OrderReceipt {
            get receiptEnv () {
//                if (this.env.pos.allow_qr_code) {
                    let receipt_render_env = super.receiptEnv;
                    let order = this.env.pos.get_order();
                    receipt_render_env.receipt.company.street = this.env.pos.company.street;
                    
                    var branch_name = this.env.pos.config.branch_name;
                    var branch_name_vals = []
                    if (branch_name){
                        branch_name_vals = this.env.pos.db.get_partner_by_id(branch_name[0])
                    }
                    receipt_render_env.receipt.branch_name_id = branch_name_vals;
                    return receipt_render_env;
               }
    
        };

    Registries.Component.extend(OrderReceipt, PosQRCodeOrderReceipt);

    return OrderReceipt;
});
