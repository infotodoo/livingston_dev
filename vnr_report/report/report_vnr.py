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
    _rec_name = 'description'
    
    name = fields.Char('Mayor Cte',readonly=True)
    default_code = fields.Char('Material',readonly=True)
    description = fields.Char('Description',readonly=True)
    total_stock = fields.Float('Total Stock',readonly=True)
    total = fields.Float('Total Value',readonly=True)
    unit_price = fields.Float('Unit Value',readonly=True)
    price_unit = fields.Float('Sale Value Unitary',readonly=True)
    sale_price = fields.Float('Sale price',readonly=True)
    cost_by_sale = fields.Float('Cost by sale Unitary',readonly=True)
    vnr_estimate = fields.Float('VNR estimate')
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_vnr')
        query = """
        CREATE or REPLACE VIEW report_vnr AS(
        
        select 
        row_number() OVER (ORDER BY pp.id) as id,
        --(
          --  select aa.code from
            --account_account aa letf join product_category pc 
            --on (pc.property_account_creditor_price_difference_categ = aa.id)
            --where pp.categ_id = pc.id
        --)as name,
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
        )as unit_price,
        --(
          --  select sol.price_unit
            --from sale_order_line sol
            --where pp.id = sol.product_id
        --)as price_unit
        (
            select sum(ppi.fixed_price)/count(ppi.product_id)
            from product_pricelist_item ppi
            where pp.id = ppi.product_id
        )as sale_price,
        (
            select sum(ppi.cost_by_sale)/count(ppi.product_id)
            from product_pricelist_item ppi
            where pp.id = ppi.product_id
        )as cost_by_sale,
        (
            select sum(value)
            from (
               select sum(ppi.fixed_price)/count(ppi.product_id) as value
               from product_pricelist_item ppi
               where pp.id = ppi.product_id

                UNION ALL
                
                select (sum(ppi.cost_by_sale)/count(ppi.product_id)) * (-1) as value
                from product_pricelist_item ppi
                where pp.id = ppi.product_id
                )as vnr
        )as vnr_estimate
        from product_product pp
        --left join stock_valuation_layer svl on (svl.product_id = pp.id)
        where 1=1
        );
        """
        self.env.cr.execute(query)