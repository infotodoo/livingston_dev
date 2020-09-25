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
    'category': 'Warehouse',
    'depends': [
                'stock',
                'hr',
                'purchase',
                ],
    'data':[
        'views/stock_picking_view.xml',
    ],
    'installable' : True,
    'application' : False,
}