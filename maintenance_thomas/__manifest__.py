# -*- coding: utf-8 -*-
{
    'name': "Maintenance Thomas",

    'summary': "Maintenance Thomas",

    'description': "Maintenance Thomas",

    'author': "Todoo SAS",
    'contributors': ['Carlos Guio fg@todoo.co','Livingston Arias Narváez la@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['maintenance','contacs_thomas'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_view.xml',
        'data/sequence.xml',
        'data/maintenance_data.xml',
        'views/maintenance_request_view.xml',
        'views/maintenance_equipment_view.xml',
        'wizard/wizard_activity_maintenance_view.xml',
        'report/report_cv_machine.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}