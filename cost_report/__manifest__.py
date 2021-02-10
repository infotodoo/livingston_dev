# -*- coding: utf-8 -*-
{
    'name': "Reporte Costos Preliminares",

    'summary': "Reporte Costos Preliminares",

    'description': "Reporte Costos Preliminares",

    'author': "Todoo SAS",
    'contributors': "Livingston Arias Narváez la@todoo.co",
    'website': "http://www.todoo.co",
    'category': 'Accounting',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['account','mrp_workorder','mrp_extended'],
  
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/report_view.xml',
        'views/menuitem.xml',
    ],
}