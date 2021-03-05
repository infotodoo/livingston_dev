# -*- coding: utf-8 -*-
{
    'name': "Mrp test",

    'summary': "- Variation Cost Mrp",

    'description': "- Variation Cost Mrp",

    'author': "Todoo SAS",
    'contributors':"Livingston",
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['mrp'],
    # always loaded
    'data': [
        'views/mrp_production_view.xml', 
    ],
    'application':True,
}

