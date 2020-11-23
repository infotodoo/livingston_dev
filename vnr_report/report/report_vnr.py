# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, tools, api,_
from datetime import datetime
from odoo.osv import expression
from odoo.tools import date_utils

_logger = logging.getLogger(__name__)

    
class ZppReportLine(models.Model):
    _name = 'report.vnr'
    _auto = False
    _description = 'This is the lines in the VNR report'
    
    name = fields.Char('Mayor Cte',readonly=True)
    default_code = fields.Char('Material',readonly=True)
    description = fields.Char('Material',readonly=True)
    total_stock = fields.Float('Total Stock',readonly=True)
    total = fields.Float('Total Value',readonly=True)
    unit_price = fields.Float('Unit Value',readonly=True)
   
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_vnr')
        query = """
        CREATE or REPLACE VIEW report_zpp AS(
        
        select 
        row_number() OVER (ORDER BY id) as id,
        (
            select aa.code from
            account_account aa letf join product_category pc 
            on (pc.property_account_creditor_price_difference_categ = aa.id)
            where pp.categ_id = pc.id
        )as name,
        pp.default_code,
        (
            select pt.name from
            product_template pt
            where pp.product_tmpl_id = pt.id
        )as description,
        (
            select sum(svl.quantity)
            from stock_valuation_layer svl
            where pp.id = svl.product_id
        )as total_stock,
        (
            select sum(svl.value)
            from stock_valuation_layer svl
            where pp.id = svl.product_id
        )as total,
        (
            select sum(svl.value)/sum(svl.quantity)
            from stock_valuation_layer svl
            where pp.id = svl.product_id
        )as unit_price
        from product_product pp
        left join stock_valuation_layer svl on (svl.product_id = pp.id)
        where 1=1
        );
        """
        self.env.cr.execute(query)