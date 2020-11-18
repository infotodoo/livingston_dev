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
    date_planned_start = fields.Datetime('Start Date',readonly=True)
    date_planned_finished = fields.Datetime('End Date',readonly=True)
    product_id = fields.Many2one('product.product','Product',readonly=True)
    product_qty = fields.Float('Quantity Planned',readonly=True)
    bom_id = fields.Many2one('mrp.bom','Bill of Material',readonly=True)
    description = fields.Char('Description',readonly=True)
    sale = fields.Char('No.Order',readonly=True)
    amount_total = fields.Float('Sale Price',readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account','Description Account Analytic',readonly=True)
    product_delivery = fields.Float('Delivered quantity',readonly=True)
    product_requisition = fields.Char('Third Service',readonly=True)
    code = fields.Char('Account Analytic',readonly=True)
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_zpp')
        query = """
        CREATE or REPLACE VIEW report_zpp AS(
        
        select 
        row_number() OVER (ORDER BY mp.id) as id,
        mp.name,mp.date_planned_start,
        mp.date_planned_finished,sol.name as description,
        mp.product_id,mp.product_qty as product_qty,
        mp.product_qty as product_delivery
        ,so.name as sale,so.amount_total,so.analytic_account_id,
        aaa.code,mprl.product_id as product_requisition
        from mrp_production mp 
        inner join sale_order so on (so.manufacture_id = mp.id)
        inner join sale_order_line sol on(sol.order_id = so.id)
        inner join account_analytic_account aaa on(aaa.id = so.analytic_account_id)
        inner join material_purchase_requisition mpr on (mpr.production_id = mp.id)
        inner join material_purchase_requisition_line mprl on (mprl.requisition_id = mpr.id)
        
        );
        """
        self.env.cr.execute(query)
        #(select to_char(mp.date_planned_start,'mm')) as month,