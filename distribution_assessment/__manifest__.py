# -*- coding: utf-8 -*-
{
    'name': "Distribution Assessment",

    'summary': "Distribution Assessment",

    'description': "Distribution Assessment",

    'author': "Todoo SAS",
    'contributors': "Livingston Arias Narváez la@todoo.co",
    'website': "http://www.todoo.co",
    'category': 'Accounting',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['account','mrp_extended'],
  
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_company_view.xml',
        'views/account_analytic_view.xml',
        'views/report_distribution_assessment_view.xml',
        'views/menuitem.xml',
    ],
}