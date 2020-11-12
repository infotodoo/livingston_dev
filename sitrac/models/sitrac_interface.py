# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class SitracInterface(models.Model):
    _name = 'sitrac.interface'
    _description = 'sitrac interface'

    name = fields.Char(string='Name',required=True)
    date_import = fields.Datetime(string='Date import')
    production_id = fields.Many2one('mrp.production', string='Porduction Order',required=True)