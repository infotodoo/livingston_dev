# -*- coding: utf-8 -*-

from odoo import models,fields,api
import logging
_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = ["mrp.production"]
    
    def production_done(self):
        #self.action_confirm()
        #self.action_assign()
        produce_id = self.env['mrp.product.produce'].search([('production_id','=',self.id)])
        _logger.error(' produce -------------------------------\n')
        _logger.error(produce_id)
        for produce in produce_id:
            produce._record_production()
            self.button_mark_done()