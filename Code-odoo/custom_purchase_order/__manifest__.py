# -*- coding: utf-8 -*-
{
    'name': "Custom Purchase order", 
    'version' : '1.2', 
    'summary': "Customization Purchase Order",
    'description': """
Purchase Order
==============
    """, 
    'author': "Sary Babiker",
    'category': 'Purchase',
    'depends': ['material_purchase_requisitions','purchase', 'account', 'purchase_discount_total', 'custom_project_manager'],
    'data': [
    'security/custom_purchase_groups.xml',
	'views/custom_purchase_order_view.xml',
    # 'views/custom_account_payment_view.xml',
    'views/custom_account_move_view.xml',
    'views/res_partner_view.xml',
    'views/res_config_settings_views.xml',
    'views/custom_report_invoice.xml'
    ],
}
