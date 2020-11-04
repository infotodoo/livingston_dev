from odoo import _, api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    bool_cost = fields.Boolean(compute="_compute_bool_cost")
    
    @api.depends('location_dest_id')
    def _compute_bool_cost(self):
        if self.location_dest_id.cost_zero:
            self.bool_cost = True
        else:
            self.bool_cost = False