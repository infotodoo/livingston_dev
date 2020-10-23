from odoo import _, fields,api, models
import logging

_logger = logging.getLogger(__name__)


class ZppReport(models.Model):
    _name = 'report.zpp'
    _description = 'This is the report ZPP'
    _rec_name = 'report_name'
    
    report_name = fields.Char('Report Name')
    start_date = fields.Datetime('Start Date')    
    final_date = fields.Datetime('Final Date')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company.id)
    
    def report(self):
        if self.start_date and self.final_date:
            zpp_line_obj = self.env['report.zpp.line']
            domain = [('date_planned_start','>=',self.start_date),('date_planned_finished','<=',self.final_date)]
            production_ids = self.env['mrp.production'].search([])#(domain)
            zpp_lines_ids = []
            for production_id in production_ids:
                if production_id:
                    vals = {
                        #'id': production_id.id,
                        'name': production_id.name,
                        'product_id': production_id.product_id.id or False,
                        'description': production_id.product_id.description_sale or False,
                        'product_qty': production_id.product_qty,
                        'bom_id': production_id.bom_id.id,
                        'product_uom_id': production_id.product_uom_id.id,
                        'company_id': self.company_id.id,
                        #'state': workorder.state,
                        #'cif_standard': cif_standard,
                        #'maq_standard': maq_standard,
                        #'mod_standard': mod_standard,
                        #'mod_real': mod_real,
                        #'cif_real': cif_real,
                        #'maq_real': maq_real,
                        #'mod_variation': mod_variation,
                        #'cif_variation': cif_variation,
                        #'maq_variation': maq_variation,
                    }
                    zpp_line = zpp_line_obj.create(vals)
                    _logger.error('****************************************1**************************')
                    _logger.error('++++++++++++++++++++++++++ zpp_line ++++++++++++++++++++++++++++++')
                    _logger.error(zpp_line)
                    zpp_lines_ids.append(zpp_line.id)
                    
            
        return {
            'type': 'ir.actions.act_window',
            'name': 'PYG Report Lines',
            'view_mode': 'tree',
            'res_model': 'report.zpp.line',
            'domain': [('id','in',zpp_lines_ids)],
            #'view_id': self.env.ref('zpp_report.zpp_report_view_tree').id,
            'target': 'current'
        }
        _logger.error('++++++++++++++++++++++++++ zpp_lines_ids +++++++++++++')
        _logger.error(zpp_lines_ids)
    
    
class ZppReportLine(models.Model):
    _name = 'report.zpp.line'
    _description = 'This is the lines in the zpp report'
    _inherit = ['mrp.production']
    
    description = fields.Char('Description')