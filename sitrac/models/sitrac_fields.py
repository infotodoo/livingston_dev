# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class Sitracfield(models.Model):
    _name = 'sitrac.field'
    _description = 'sitrac fields'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product',string='Product')
    sitrac_id = fields.Many2one('sitrac.interface')
    quantity = fields.Float('Quantity')