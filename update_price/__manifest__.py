# -*- coding: utf-8 -*-
{
    'name': "Update Price",

    'summary': "Update Price",

    'description': "Update Price",

    'author': "Todoo SAS",
    'contributors': "Livingston Arias Narváez la@todoo.co",
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invetory',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],
  
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/report_view.xml',
        'views/menuitem.xml',
    ],
}