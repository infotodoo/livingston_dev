###################################################################################
# 
#    Copyright (C) 2020 Todoo  SAS
#
#    
#    
#    
#    
#
#    
#    
#    
#    
#
#    
#    
#
###################################################################################

{
    "name": "Purchase Partner Certifications",
    "summary": """Certifications""",
    "version": "13.0",
    "category": "Purchase",
    "license": "AGPL-3",
    "website": "www.todoo.co",
    "author": "Todoo SAS",
    "contributors": [
        "Luis Felipe Paternina <lp@todoo.co>",
    ],
    "depends": [
        "account",
        "contacts",
        "purchase",
    ],
    "data": [
        "views/res_partner_view.xml",
        "views/purchase.xml",
        "reports/res_partner.xml",
        "security/ir.model.access.csv",
    ],
    "images": [
        'static/description/todoo.png'
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "application": False,
    "installable": True,
    "auto_install": False,
}
