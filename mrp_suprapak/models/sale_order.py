from odoo import models,fields,api,_
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    manufacture_id = fields.Many2one('mrp.production',store=True)
                
                
class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    def create(self,values):
        _logger.error('este logger +++++++++++++++++++++++++++++++++++++++++++++++++')
        sale_obj = self.env['sale.order'].search([('name','=',values[0]['origin'])])
        res = super(MrpProduction,self).create(values)
        sale_obj.manufacture_id = res.id
        _logger.error('este logger imprime los vals de mrp produccion')
        _logger.error(values)
        return res