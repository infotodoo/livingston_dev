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
    
    name = fields.Char('Production Order',readonly=True)
    product_id = fields.Many2one('product.product','Product',readonly=True)
    product_qty = fields.Float('Quantity Planned',readonly=True)
    bom_id = fields.Many2one('mrp.bom','Bill of Material',readonly=True)
    description = fields.Char('Description',readonly=True)
    sale = fields.Char('No.Order',readonly=True)
    amount_total = fields.Float('Sale Price',readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account','Account Analytic',readonly=True)
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_zpp')
        query = """
        CREATE or REPLACE VIEW report_zpp AS(
        
        select 
        row_number() OVER (ORDER BY mp.id) as id,
        mp.name,sol.name as description,mp.product_id,mp.product_qty
        ,so.name as sale,so.amount_total,so.analytic_account_id
        from mrp_production mp 
        inner join sale_order so on (so.manufacture_id = mp.id)
        inner join sale_order_line sol on(sol.order_id=so.id)
        
        );
        """
        self.env.cr.execute(query)