# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, tools, api,_
from datetime import datetime
from odoo.osv import expression
from odoo.tools import date_utils

_logger = logging.getLogger(__name__)

    
class DistributionAssessment(models.Model):
    _name = 'report.distribution.assessment'
    _auto = False
    _description = 'This is the lines in the Distribution Assessment report'
    _rec_name = 'description'
    
    name = fields.Char('Workcenter',readonly=True)
    #default_code = fields.Char('Material',readonly=True)
    #description = fields.Char('Description',readonly=True)
    #total_stock = fields.Float('Total Stock',readonly=True)
    #total = fields.Float('Total Value',readonly=True)
    #unit_price = fields.Float('Unit Value',readonly=True)
    #price_unit = fields.Float('Sale Value Unitary',readonly=True)
    #sale_price = fields.Float('Sale price',readonly=True)
    #cost_by_sale = fields.Float('Cost by sale Unitary',readonly=True)
    #vnr_estimate = fields.Float('VNR estimate')
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_distribution_assessment')
        query = """
        CREATE or REPLACE VIEW report_distribution_assessment AS(
        
        select 
        row_number() OVER (ORDER BY mp.id) as id,
        (
            select w.name from
            mrp_workcenter w
            where mp.worcenter_id = w.id
        )as name
        from mrp_workorder mp
        where 1=1
        );
        """
        self.env.cr.execute(query)