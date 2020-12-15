# -*- coding: utf-8 -*-
{
    'name': "Budget Comtrol",

    'summary': "",

    'description': "This is a module for control Budgets",

    'author': "Todoo",
    'website': "http://www.todoo.co",
    'contributors': "Livingston Arias la@todoo,co",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase','account_accountant','account_budget','l10n_co'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_view.xml',
        'views/crossovered_budget_lines_view.xml',
        'wizard/wizard_purchase_view.xml',
        'wizard/wizard_account_view.xml',
    ],
    # only loaded in demonstration mode
    'images': [],
    'application': True,
}