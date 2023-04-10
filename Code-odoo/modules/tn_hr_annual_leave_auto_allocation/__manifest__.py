# -*- coding: utf-8 -*-
{
    'name': "HR Annual Leave Auto Allocation", 
    'version' : '1.2', 
    'summary': "HR Annual Leave Auto Allocation",
    'description': """
	HR Annual Leave Auto Allocation
Hr Locations
==============
    """, 
    'author': "Sary Babiker",
    'category': 'HR',
    'depends': ['hr', 'hr_contract', 'hr_holidays'],
    'data': [
        'data/location_cron_data.xml',
        'views/hr_employee_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_leave_type_views.xml',
    ],
}
