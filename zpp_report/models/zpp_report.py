import logging
from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class ZppReport(models.TransientModel):
    _name = 'wizard.zpp'
    _description = 'This is the report ZPP'
    _rec_name = 'report_name'
    
    report_name = fields.Char('Report Name')
    start_date = fields.Datetime('Start Date')    
    final_date = fields.Datetime('Final Date')
    
   
    def action_report(self):
        _logger.error("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        _logger.error("siiiiiiiiiiiiiiiiiiiiii")
        return{
            'name': 'test',
            'view_type': 'tree',
            'view_mode': 'tree',
            #'view_id': ,
            'res_model': 'report.zpp',
            #'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.report',
            'target': 'current',
            'view_id': "zpp_report.zpp_report_view_tree",
        }