# -*- coding: utf-8 -*-
{
    'name': "Accrual Invoice Real State Report",  # Module title
    'summary': "ManageAccrual Invoice Real State Report",  
    'description': """
Accrual Invoice Real State Report
==============
Accrual Invoice Real State Report
    """,  # Supports reStructuredText(RST) format
    'author': "Sary Babiker",
    'version': '15.0.1',
    'depends': ['base', 'itsys_real_estate','report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'report/menu_report_view.xml',
        'report/accrual_invoice_template.xml',
        'wizard/accrual_invoice_wizard_view.xml',
    ],
}



