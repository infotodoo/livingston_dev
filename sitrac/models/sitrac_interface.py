# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class SitracInterface(models.Model):
    _name = 'sitrac.interface'
    _description = 'sitrac interface'

    name = fields.Char(string='Name',required=True)
    date_import = fields.Datetime(string='Date import',required=True)
    production_id = fields.Many2one('mrp.production', string='Porduction Order',required=True)
    sitrac_ids = fields.One2many('sitrac.field','sitrac_id',string='Product Charge')
    
    def cargar(self):
        if len(self.sitrac_ids) > 0 and self.production_id:
            list = []
            for lines in self.sitrac_ids:
                dic={
                    'name':self.production_id.id,
                    'product_id':lines.product_id.id,
                    'product_uom':lines.product_id.uom_id.id,
                    'location_id':self.production_id.location_src_id.id,
                    'location_dest_id':self.production_id.location_dest_id.id,
                    'product_uom_qty': lines.quantity,
                    'quantity_done': lines.quantity,
                }
                list.append((0,0,dic))
                production_line_id = self.env['mrp.production'].browse(self.production_id.id)
                production_line_id.write({'move_raw_ids':list})
