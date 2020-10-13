#Luis Felipe Paternina--
# Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class Todoo(models.Model):
    _inherit = 'maintenance.equipment'

    brand_maintenance = fields.Char(string="Marca", trackinig=True)
    date_start_contract = fields.Date(related="partner_id.start_date_contract", string="Fecha Inicio de Contrato", trackinig=True)
    date_end = fields.Date(related="partner_id.end_date_contract", string="Fecha Fin de Contrato",trackinig=True)
    maintenance_value = fields.Integer(string="Valor del Mantenimiento Preventivo", tracking=True)
    maintenance_cant = fields.Integer(string="Cantidad de Mantenimientos", tracking=True)
    maintenance_total = fields.Integer(string="Valor Total del Mantenimiento", compute="_calculate_maintenance_total")
    maintenance_frequency = fields.Integer(string="Frecuencia del Mantenimiento", tracking=True)
    branch = fields.Many2one('res.city', string="Ciudad", tracking=True)
    inventory_plate = fields.Char(string="Placa de Inventario")
    address = fields.Char(string="Dirección de Sucursal")
    office_code = fields.Char(string="Código de Oficina - Sucursal")
    department = fields.Many2one('res.country.state', string="Departamento")
    branch_tst = fields.Char(string="Sucursal")
    maintenance_value_corrective = fields.Integer(string="Valor del Mantenimiento Correctivo")
    rental_contract = fields.Boolean(string="Máquina en Contrato de Alquiler")

    
    #Calcular total del matenimiento
    @api.depends('maintenance_cant','maintenance_value')
    def _calculate_maintenance_total(self):
        for record in self:
            record.maintenance_total = record.maintenance_cant * record.maintenance_value

    def action_view_stock_move_lines(self):
        self.ensure_one()
        action = self.env.ref('stock.stock_move_line_action').read()[0]
        lot_ids = self.env['stock.production.lot'].search([('name','=',self.serial_no)])
        if lot_ids:
            lot_ids = lot_ids.ids
        else:
            lot_ids = []    
        action['domain'] = [('lot_id', 'in', lot_ids)]
        return action

      
        