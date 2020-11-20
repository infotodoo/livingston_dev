# -*- coding: utf-8 -*-

from odoo import models,api,fields,_

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sync1 = fields.Binary(string='Sync 1')
    sync2 = fields.Binary(string='Sync 2')
    sync3 = fields.Binary(string='Sync 3')
    bool_wizard = fields.Boolean(compute='_compute_bool_wizard')


    @api.depends('picking_type_id')
    def _compute_bool_wizard(self):
        for record in self:
            if record.picking_type_id.warehouse_id.name == 'PRODUCTO SEMIELABORADO TGS COL':
                record.bool_wizard = True
            elif record.picking_type_id.warehouse_id.name == 'ALMACEN GENERAL TGS COL' and record.picking_type_id.name in ['Órdenes de Entrega','Fabricación']:
                record.bool_wizard = True
            else:
                record.bool_wizard = False
    
    def active_wizard_stock(self):
        super(StockPicking,self).action_assign()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking.wizard',
            'view_mode': 'form',
            'views': [(False,  'form')],
            'target': 'new',
        }
