# -*- coding: utf-8 -*-


from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    #modify by livingston
    distribution_id = fields.Many2one('purchase.distribution','Distribution')
    
    
class PurchaseDistribution(models.Model):
    _name = 'purchase.distribution'
    _description = 'purchase distribution'
    
    #modify by livingston
    name = fields.Char()
