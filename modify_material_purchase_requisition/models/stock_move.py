# -*- coding: utf-8 -*-

from odoo import fields,api,models

class StockMoveLine(models.Model):
    _inherit = 'stock.move'

    inspection_state = fields.Selection([('according','According'),('released','Released'),('inspection','Without Inspection')],'Inspection State')
    
    product_id = fields.Many2one('product.product', 'Product',check_company=True,
        domain="[('type', 'in', ['product', 'consu','service']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", index=True, required=True,states={'done': [('readonly', True)]})
