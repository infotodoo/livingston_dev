from odoo import models, api, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_id = fields.Many2one('res.users','Delivery By')
    recieved_id = fields.Many2one('res.users','Decieved By')
    owner_id = fields.Many2one('res.users','Owner')
    security_aux_id = fields.Many2one('res.users','Security Auxiliar')
    area = fields.Char = ('Solicitant Area',related='custom_requisition_id.department_id.name')
    responsable = fields.Char = ('Responsable',related='custom_requisition_id.employee_id.name')
    charge_to = fields.Char = ('Charge To',related='custom_requisition_id.charge_to')
    cost_center_id = fields.Many2one('mrp.workcenter','Cost Center')
