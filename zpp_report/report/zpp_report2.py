import logging
from odoo import fields, models, tools, api,_
from datetime import datetime
from odoo.osv import expression
from odoo.tools import date_utils

_logger = logging.getLogger(__name__)

    
class ZppReportLine(models.Model):
    _name = 'report.zpp'
    _auto = False
    _description = 'This is the lines in the zpp report'
    
    name = fields.Char('Description',readonly=True)
    product_id = fields.Many2one('product.product','Product',readonly=True)
    product_qty = fields.Float('Product_qty',readonly=True)
    bom_id = fields.Many2one('mrp.bom','Bill of Material',readonly=True)
    description = fields.Char('Description',readonly=True)
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_zpp')
        query = """
        CREATE or REPLACE VIEW report_zpp AS(
        
        select row_number() OVER (ORDER BY wp.id) as id,mp.name from mrp_production as mp
        inner join wizard_zpp as wp on  
        mp.date_planned_start <= wp.start_date and mp.date_planned_finished >= wp.final_date
        
        );
        """
        self.env.cr.execute(query)