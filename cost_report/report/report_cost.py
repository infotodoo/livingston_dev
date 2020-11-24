# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, tools, api,_
from datetime import datetime
from odoo.osv import expression
from odoo.tools import date_utils

_logger = logging.getLogger(__name__)

    
class ZppReportLine(models.Model):
    _name = 'report.cost'
    _auto = False
    _description = 'This is the lines in the cost report'
    
    name = fields.Char('Code',readonly=True)
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_vnr')
        query = """
        CREATE or REPLACE VIEW report_vnr AS(
        
        select 
        row_number() OVER (ORDER BY mp.id) as id,
        mp.code as name,
        (
            select mw.name
            from mrp_workcenter
            left join mrp_routing_workcenter mpw
            on mpw.workcenter_id = mw.id
            left join mrp_routing mr on
            mr.id = mpw.routing_id
            left join mrp_workorder mwo
            on mwo.routing_id = mr.id
        )
        from mrp_production mp
        where 1=1
        );
        """
        self.env.cr.execute(query)