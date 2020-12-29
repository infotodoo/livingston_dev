# -*- coding: utf-8 -*-
from odoo import models,api,fields
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class AccountAnalyticTag(models.Model):
    _inherit = 'account.analytic.tag'
    
    fiscal_id = fields.Many2one('account.fiscal.year','Fiscal Year',required=True)
    

class AccountAnalyticDistribution(models.Model):
    _inherit = 'account.analytic.distribution'
    
    suggested_percentage = fields.Float('Suggested Percentage',compute="_compute_suggested_percentage")
    
    @api.depends('tag_id.fiscal_id')
    def _compute_suggested_percentage(self):
        for record in self:
            analytic_account_id = record.env['mrp.workcenter'].search([('account_analytic_real','=',record.account_id.id),limit=1])
            if record.tag_id.fiscal_id:
                date = record.tag_id.fiscal_id.date_to
                date = date.strftime("%Y-%m")
                date = str(date[0:7])
                _logger.error('*************************************\ndate\n**************************')
                _logger.error(date)
                percentage = record.env['report.distribution.assessment'].search([('name','=',analytic_account_id.name),('date_end','=',date)])
                record.suggested_percentage = percentage.percentage
            else:
                record.suggested_percentage = 0
            