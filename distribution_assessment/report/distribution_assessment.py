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
    
    name = fields.Char('Workcenter',readonly=True)
    hours = fields.Float('Hours',readonly=True)
    total_time = fields.Float('Total Times',readonly=True)
    percentage = fields.Float('%',readonly=True)
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
            --with total_time as (select sum(mwp.duration) from mrp_workcenter_productivity mwp)
            select 
            row_number() OVER (ORDER BY w.id)as id,
            w.name,sum(mwp.duration) as hours,
            (
             select sum(mwp.duration) 
             from mrp_workcenter_productivity mwp
            ) as total_time,
            (
             sum(mwp.duration)/(select sum(mwp.duration) 
             from mrp_workcenter_productivity mwp)
            )as percentage
            from mrp_workcenter_productivity mwp
            left join mrp_workcenter w on (w.id = mwp.workcenter_id)
            --left join mrp_workorder mp on (mp.workcenter_id = w.id)
            where 1=1
            group by w.id, w.name
            );
            """
        self.env.cr.execute(query)
    
#class MrpCostStructureSupra(models.AbstractModel):
 #   _name = 'report.distribution_assessment.distribution_assessment_structure'
  #  _description = 'MRP Distribution Assessment'

   # def get_lines(self, workorders):
    #    res = []
     #   workorder = []
      #  total_hours = []
       # query_str = """select row_number() OVER (ORDER BY w.id)as id,
        #                w.name as name,sum(mwp.duration) as hours,sum(mwp.)
        #                from mrp_workcenter_productivity mwp
        #                left join mrp_workcenter w on (w.id = mwp.workcenter_id)
        #                in %s 
        #                group by w.id, w.name"""
        #self.env.cr.execute(query_str, (tuple(workorders.ids), ))
        #for name, hours in self.env.cr.fetchall():
        #    workorder.append([name,hours])
        #    for hour in workorders.duration:
        #        total_hour += hour
        #        total_hours.append([total_hour])
        #    res.append({
        #        'workorder':workorder,
        #        'total_hours':total_hours,
        #    })
        #return res
        
    #@api.model
    #def _get_report_values(self):
    #    workorders = self.env['mrp.workorder']
    #        res = self.get_lines(workorders)
    #    return {'lines': res}
    
    