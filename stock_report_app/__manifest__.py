# -*- coding: utf-8 -*-
{
    "name": "Cuadro de Stock",
    "version": "13.0.1.0.0",
    'depends': ['stock', 'web_dashboard', 'web_cohort', 'web_map', 'web_grid', 'sale_stock_ap','product'],
    "category": "Warehouse Management",
    "installable": True,
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        #"report/stock_enterprise_templates.xml",
        "report/report_stock_availability.xml",
        "views/product_view.xml",
        "report/stock_report_view.xml",
    ],
}
