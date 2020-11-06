{
    'name': "Zpp Report",

    'summary': "Report ZPP",

    'description': "Report ZPP",

    'author': "Todoo SAS",
    'contributors': "Livingston Arias Narváez la@todoo.co",
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant','mrp_workorder'],
  
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/pyg_report_view.xml',
        'views/menu_view.xml',
    ],
}