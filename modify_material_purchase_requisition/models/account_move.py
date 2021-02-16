# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import Warning, UserError


class AccountMove(models.Model):
    _inherit = 'account.move'


    charge_to = fields.Selection([('order','Production Order'),('center','Cost Center')],'Charge To')
    production_id = fields.Many2one('mrp.production','Production Order')#,domain=[('state','not in',('draft','done','cancel'))])

    def cargar(self):
        if self.charge_to == 'order':
            if len(self.invoice_line_ids) > 0 and self.production_id:
                list = []
                if self.production_id.bool_state == False:
                    for lines in self.invoice_line_ids:
                        dic={
                            'name':self.production_id.name,
                            'product_id':lines.product_id.id,
                            'product_uom':lines.product_id.uom_id.id,
                            'location_id':self.production_id.location_src_id.id,
                            'location_dest_id':self.production_id.location_dest_id.id,
                            'product_uom_qty': lines.quantity,
                            'quantity_done': 1,
                        }
                        list.append((0,0,dic))
                    production_line_id = self.env['mrp.production'].browse(self.production_id.id)
                    production_line_id.write({'move_raw_ids':list})
                    message = {
                           'type': 'ir.actions.client',
                           'tag': 'display_notification',
                           'params': {
                               'title': _('Warning!'),
                               'message': 'Productos cargados con exito',
                               'sticky': False, }
                            }
                else:
                    message = {
                           'type': 'ir.actions.client',
                           'tag': 'display_notification',
                           'params': {
                               'title': _('Warning!'),
                               'message': 'No puede cargar productos a una orden bloqueada',
                               'sticky': False, }
                            }
                return message