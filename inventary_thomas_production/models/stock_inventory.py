from odoo import _, api, fields, models


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    diff_motive = fields.Char('Difference Reason')
    assigned_to = fields.Many2one('res.users','Assigned to')
    start_date = fields.Date('Date start programming')
    end_date = fields.Date('Date snd programming')
