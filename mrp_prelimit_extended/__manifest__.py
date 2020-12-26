# -*- coding: utf-8 -*-
{
    'name': "Mrp Prelimit Extended",

    'summary': "Mrp Prelimit Extended",

    'description': "Mrp Prelimit Extended",

    'author': "Todoo SAS",
    'contributors': "Livingston Arias Narváez la@todoo.co",
    'website': "http://www.todoo.co",
    'category': 'Accounting',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],
  
    # always loaded
    'data': [
        'security/ir.model.acces.csv',
        'views/mrp_prelimit_distribution_view.xml',
    ],
}