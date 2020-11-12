# -*- coding: utf-8 -*-
{
    'name': "Sitrac Interface",

    'summary': "Sitrac Interface",

    'description': "Sitrac Interface",

    'author': "Todoo SAS",
    'contributors': ['Livingston Arias Narváez la@todoo.co'],
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['mrp_workorder'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sitrac_interface_view.xml',
        'views/sitrac_interface_menu.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}