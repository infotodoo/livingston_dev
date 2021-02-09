{
    'name': 'Modify Purchase Requisition',
    'version': '1.0',
    'summary': """This module allow your employees/users to create Purchase Requisitions.""",
    'description': """
    Module to modify Material Purchase Requisition
    """,
    'author': 'Todoo S.A.S.',
    'website': 'http://www.todoo.com',
    'images': [''],
    'category': 'Requisition',
    'depends': ['material_purchase_requisitions','stock','manufacture_masive_block','account_accountant'],
    'data':[
        'views/material_purchase_requisition.xml',
        'views/stock_picking_view.xml',
    ],
    'installable' : True,
    'application' : False,
}