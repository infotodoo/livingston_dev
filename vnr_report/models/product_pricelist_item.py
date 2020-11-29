# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, api,_

_logger = logging.getLogger(__name__)

    
class ProductPricelist(models.Model):
    _inherit = 'product.pricelist.item'
    
    cost_by_sale = fields.Float('Cost by sale',store=True)