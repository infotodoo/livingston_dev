from odoo import models, api, fields

class MaterialPurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'

    responsable_area = fields.Char('Responsable Area')
    charge_to = fields.Selection([('order','Production Order'),('center','Cost Center')],'Charge To')
    production_id = fields.Many2one('mrp.production','Production Order')
    quantity_delivery = fields.Char('Quantity Delivery')
    unit = fields.Many2one('uom.uom','Unit of Measure')
    delivery_by = fields.Char('Delivery By',compute="_compute_delivery_by")
    recieved_by = fields.Char('recieved By',compute="_compute_recieve_by")
    security_aux = fields.Char('recieved By',compute="_compute_security_aux")
    

    def _compute_security_aux(self):
        for record in self:
            stock_id = record.env['stock.picking'].search([('name','=',record.origin),('state','=','assigned')],limit=1)
            if record.state == 'stock' and stock_id:
                record.security_aux = stock_id.security_aux_id.name
            else:
                record.security_aux = ''
    
    def _compute_recieve_by(self):
        for record in self:
            stock_id = record.env['stock.picking'].search([('name','=',record.origin),('state','=','assigned')],limit=1)
            if record.state == 'stock' and stock_id:
                record.recieved_by = stock_id.recieved_id.name
            else:
                record.recieved_by = ''
    
    def _compute_delivery_by(self):
        for record in self:
            stock_id = record.env['stock.picking'].search([('name','=',record.origin),('state','=','assigned')],limit=1)
            if record.state == 'stock' and stock_id:
                record.delivery_by = stock_id.delivery_id.name
            else:
                record.delivery_by = ''

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            self.responsable_area =  self.department_id.manager_id.name
        else:
            self.responsable_area = ''

class MaterialPurchaseRequisitionLine(models.Model):
    _inherit = 'material.purchase.requisition.line'

    inspection_state = fields.Char('Inspection State',compute="_compute_inspection_state")

    def _compute_inspection_state(self):
        for record in self:
            #stock_id = record.env['stock.move']
