from odoo import _, api, fields, models


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    diff_motive = fields.Char('Difference Reason')