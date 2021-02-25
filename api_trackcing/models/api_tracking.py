# -*- coding: utf-8 -*-

from odoo import models,api,fields, _
from odoo.exceptions import ValidationError
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class ApiTracking(models.TransientModel):
    _name = 'api.tracking'
    _description = 'api tracking'
    
    def api_Create(self,vals,url):
        _logger.error('vals \n url')
        _logger.error(url)
        _logger.error(vals)
        if vals and url:
            resp = requests.post(
                url=url,
                data=json.dumps(vals),
            )
            if resp.ok:
                #if not vals:
                res = resp.json()
                resp.close
                return res
            else:
                resp.close
                raise ValueError("Api ERROR: %s." % (resp.json()))
            #else:
                #resp.close
                #raise ValueError("Bad response: %s." % (resp.json()))
        else:
            raise ValueError("You must write lots")