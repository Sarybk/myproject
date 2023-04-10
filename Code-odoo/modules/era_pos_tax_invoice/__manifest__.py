# -*- coding: utf-8 -*-
{
    'name': "Electronic invoice KSA - POS Encoded | qrcode | ZATCA | vat | e-invoice | tax | Zakat",
    "version" : "14.0.0.3",
    "category" : "Accounting",
    'description': """
        Electronic invoice KSA - POS
    """,
    'author': "Era group",
    'email': "aqlan@era.net.sa ",
    'website': "https://era.net.sa",
    'category': 'accounting',
    'price': 0,  
    'currency': 'USD',
    'version': '0.1',
    'license': 'AGPL-3',
    'images': ['static/description/main_screenshot.png'],
    'depends': ['base', 'account', 'point_of_sale','pos_sale'],
    'data': [
	    'security/ir.model.access.csv',
        'security/pos_sessions_security.xml',
        "report/report_view.xml",
        "report/pos_order_report_template.xml",
        'views/pos_config.xml',
        'views/pos_session_view.xml',
        'views/pos_payment_method_view.xml',
	    'views/pos_payment_view.xml',
        'views/pos_hide_menue.xml',
        'wizard/pos_order_wizard_view.xml',
    ],
    'qweb': ['static/src/xml/pos.xml'],

}
