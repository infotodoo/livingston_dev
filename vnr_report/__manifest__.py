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
    'depends': ['account','stock','sale_management'],
  
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/report_view.xml',
        'views/menuitem.xml',
    ],
}