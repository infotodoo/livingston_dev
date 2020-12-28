# -*- coding: utf-8 -*-
from odoo import models,api,fields

class AccountAnalyticTag(models.Model):
    _inherit = 'account.analytic.tag'
    
    fiscal_id = fields.Many2one('account.fiscal.year','Fiscal Year')
    

class AccountAnalyticDistribution(models.Model):
    _inherit = 'account.analytic.distribution'
    
    suggested_percentage = fields.Float('Suggested Percentage')