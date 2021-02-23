# -*- coding: utf-8 -*-


from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    #modify by livingston
    distribution_id = fields.Many2one('purchase.distribution','Distribution')
    bool = fields.Boolean(compute="_compute_bool")
    
    @api.depends('company_id')
    def _compute_bool(self):
        if self.company_id.id == 19:
            self.bool = True
        else:
            self.bool = False
    
    
class PurchaseDistribution(models.Model):
    _name = 'purchase.distribution'
    _description = 'purchase distribution'
    
    #modify by livingston
    name = fields.Char()

