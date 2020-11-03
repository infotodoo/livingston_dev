from odoo import _, api, fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    cost_zero = fields.Boolean('Location manage cost?')