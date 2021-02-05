# -*- coding: utf-8 -*-
from odoo import models,fields,api
import logging
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    prelimit_id = fields.Many2one('mrp.prelimit','Prelimit')
    
