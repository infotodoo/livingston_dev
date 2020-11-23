# -*- coding: utf-8 -*-

import logging
from odoo import fields, models, tools, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    sold_out = fields.Boolean('Producto Agotado')