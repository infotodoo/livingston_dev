from odoo import models, api, fields
from material_purchase_requisitions import purchase_requisition

class MaterialPurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'

    responsable_area = fields.Char('Responsable Area',compute='_compute_responsable_area')
    charge_to = fields.Selection([('order','Production Order'),('center','Cost Center')],'Charge To')
    production_id = fields.Many2one('mrp.production','Production Order')
    cost_center_id = fields.Many2one('mrp.workcenter','Cost Center')

    @api.depends('department_id')
    def _compute_responsable_area(self):
        if self.department_id:
            self.responsable_area =  self.department_id.manager_id.name
        else:
            self.responsable_area = ''
    
    @api.model
    def _prepare_po_line(self, line=False, purchase_order=False):
        po_line_vals = {
                 'product_id': line.product_id.id,
                 'name':line.product_id.name,
                 'product_qty': line.qty,
                 'product_uom': line.uom.id,
                 'date_planned': fields.Date.today(),
                 'price_unit': line.product_id.standard_price,
                 'order_id': purchase_order.id,
                 'account_analytic_id': line.analytic_account_id.id,
                 'custom_requisition_line_id': line.id
        }
        return po_line_vals
            
    
class MaterialPurchaseRequisitionLine(models.Model):
    _inherit = 'material.purchase.requisition.line'

    inspection_state = fields.Char('Inspection State',compute="_compute_inspection_state")
    delivery_by = fields.Char('Delivery By',compute="_compute_delivery_by")
    recieved_by = fields.Char('recieved By',compute="_compute_recieve_by")
    security_aux = fields.Char('recieved By',compute="_compute_security_aux")
    analityc_acount_id = fields.Many2one('account.analytic.account','Cost Center')
    

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

    #def _compute_inspection_state(self):
        #for record in self:
            #stock_id = record.env['stock.move']
