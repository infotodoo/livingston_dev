# -*- coding: utf-8 -*-

import datetime
from odoo import models,api,fields, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def tracking_values(self):
        vals = []
        data = {}
        url = "http://45.239.115.198:8080/TrackingWS/tracking/save/mrroll"
        if self.move_ids_without_package:
            for record in self.move_ids_without_package:
                if record.product_id.is_tracking_papper_api:
                    date = ''
                    date = str(record.date_expected.date())
                    _logger.error('date \n')
                    _logger.error(date)
                    data = {
                        "dateReceived": date,
                        "idPaperType": record.product_id.id,
                        "msf": record.product_uom.name
                        #"serial": record.lot_id.name
                    }
                    vals.append(data)
                    _logger.error(date)
                else:
                    continue
            tracking = self.env['api.tracking'].api_Create(vals,url)
            return tracking
                    
    def validation_tracking(self):
        self.button_validate()
        self.tracking_values()
                    