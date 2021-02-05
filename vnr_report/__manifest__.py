# -*- coding: utf-8 -*-
{
    'name': "Calculo VNR",

    'summary': "Calculo VNR",

    'description': "Calculo VNR",

    'author': "Todoo SAS",
    'contributors': "Livingston Arias Narváez la@todoo.co",
    'website': "http://www.todoo.co",
    'category': 'Accounting',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['account','sale','stock_account'],
  
    # always loaded
    'data': [
        'views/product_pricelist_item_view.xml',
        'security/ir.model.access.csv',
        'views/report_view.xml',
        'views/menuitem.xml',
    ],
}