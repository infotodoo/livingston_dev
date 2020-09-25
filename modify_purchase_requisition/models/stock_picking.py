from odoo import models, api, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_id = fields.Many2one('res.users','Delivery By')
    recieved_id = fields.Many2one('res.users','Decieved By')
    security_aux_id = fields.Many2one('res.users','Security Auxiliar')