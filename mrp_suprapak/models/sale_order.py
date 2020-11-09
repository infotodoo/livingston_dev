from odoo import models,fields,api,_

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    manufacture_id = fields.Many2one('mrp.production','Manufacture Order',compute='_compute_manufacture_id',store=True)
    
    @api.depends('name')
    def _compute_manufacture_id(self):
        for record in self:
            order_obj = record.env['mrp.production'].search([('origin','=',record.name)],limit=1)
            if order_obj:
                record.manufacture_id = order_obj.id
            else:
                record.manufacture_id = False