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
    month = fields.Integer('Date',readonly=True)
    year = fields.Integer('end',readonly=True)
    hours = fields.Float('Hours',readonly=True)
    total_time = fields.Float('Total Times',readonly=True)
    percentage = fields.Float('%',readonly=True,digits=(6,6))
    management = fields.Float('Operation Management',readonly=True)
    laboratory = fields.Float('Laboratory',readonly=True)
    dispatch = fields.Float('Dispatch',readonly=True)
    maintenance = fields.Float('Maintenance',readonly=True)
    disused_assets = fields.Float('Disused Assets',readonly=True)
    alternative_center = fields.Float('Alternative Center',readonly=True)
    code = fields.Char('Code',readonly=True)
    company_id = fields.Many2one('res.company',readonly=True)
    plan_department_id = fields.Float('Plan Department',readonly=True)
    shipping_department_id = fields.Float('Shipping Department',readonly=True)
    plant_maintenance_id = fields.Float('Plant Maintenance',readonly=True)
    plant_overhead_id = fields.Float('Plant Overhead',readonly=True)
    transport_id = fields.Float('Transport',readonly=True)
    rm_id = fields.Float('Rm',readonly=True)
    plant_support_id = fields.Float('Plant Support',readonly=True)
    proyect_id = fields.Float('Proyect',readonly=True)
    warehouse_distribution_id = fields.Float('Warehouse',readonly=True)
    prepress_id = fields.Float('Prepress',readonly=True)
    supplies_id = fields.Float('Supplies',readonly=True)
    date_end = fields.Char('Date End',compute='_compute_date_end')
    
    def _compute_date_end(self):
        for record in self:
            if record.year and record.month:
                record.date_end = str(int(record.year))+'-'+str(int(record.month))
            else:
                record.date_end = ''
    

    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_distribution_assessment')
        company_ids = self.env['res.company'].search([])
        query = """CREATE or REPLACE VIEW report_distribution_assessment AS("""
        count = 0
        for record in company_ids:
            if count:
                query += """UNION ALL"""
            count += 1
            
            query += """
                select row_number() OVER (ORDER BY subquery.id) as id,company_id,code,name,hours,month,year,total_time,
                (subquery.hours/(select (sum(p.duration)/60) 
                 from mrp_workcenter_productivity p where extract(month from p.date_end) = subquery.month and extract(year from p.date_end) = subquery.year)) as percentage,
                 (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.management_id = aml.analytic_account_id)
                 where rc.management_id = aml.analytic_account_id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year)
                 )
                )as management,
                (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.laboratory_id = aml.analytic_account_id)
                 where rc.laboratory_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'

                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year)
                 )
                )as laboratory,
                (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.dispatch_id = aml.analytic_account_id)
                 where rc.dispatch_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as dispatch,
                (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.maintenance_id = aml.analytic_account_id)
                 where rc.maintenance_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as maintenance,
                (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.disused_assets_id = aml.analytic_account_id)
                 where rc.disused_assets_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as disused_assets,
                (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.alternative_center_id = aml.analytic_account_id)
                 where rc.alternative_center_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as alternative_center,
                (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.plan_department_id = aml.analytic_account_id)
                 where rc.plan_department_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as plan_department_id,
                (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.shipping_department_id = aml.analytic_account_id)
                 where rc.shipping_department_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as shipping_department_id,
                (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.plant_maintenance_id = aml.analytic_account_id)
                 where rc.plant_maintenance_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as plant_maintenance_id,
                 (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.plant_overhead_id = aml.analytic_account_id)
                 where rc.plant_overhead_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as plant_overhead_id,
                (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.transport_id = aml.analytic_account_id)
                 where rc.transport_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as transport_id,
                (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.rm_id = aml.analytic_account_id)
                 where rc.rm_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as rm_id,
                (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.plant_support_id = aml.analytic_account_id)
                 where rc.plant_support_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as plant_support_id,
                 (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.proyect_id = aml.analytic_account_id)
                 where rc.proyect_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as proyect_id,
                (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.warehouse_distribution_id = aml.analytic_account_id)
                 where rc.warehouse_distribution_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as warehouse_distribution_id,
                 (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.prepress_id = aml.analytic_account_id)
                 where rc.prepress_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as prepress_id,
                (
                 (
                 select (sum(aml.debit)-sum(aml.credit)) 
                 from account_account_tag aat
                 left join account_account_account_tag aaat on (aaat.account_account_tag_id = aat.id)
                 left join account_account aa on (aa.id = aaat.account_account_id)
                 left join account_move_line aml on (aml.account_id = aa.id)                  
                 left join account_move am on (am.id = aml.move_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.supplies_id = aml.analytic_account_id)
                 where rc.supplies_id = aaa.id and ((aat.id = 7 or aat.id = 8 or aat.id = 9)) and extract(month from aml.date) = subquery.month and extract(year from aml.date) = subquery.year and am.state = 'posted'
                 )
                 *
                 (subquery.hours/(select (sum(p.duration)/60)                   
                 from mrp_workcenter_productivity p 
                 where extract(month from p.date_end) = subquery.month and 
                 extract(year from p.date_end) = subquery.year))
                )as supplies_id
                from (
                select 
                row_number() OVER (ORDER BY w.id) as id,mwp.company_id,
                w.name,
                sum(mwp.duration)/60 as hours,extract(MONTH from mwp.date_end) as month,extract(YEAR 
                from mwp.date_end) as year,
                (
                 select (sum(mwp.duration)/60)
                 from mrp_workcenter_productivity mwp
                ) as total_time,
                (
                 --select aaa.code 
                 --from account_analytic_account aaa
                 --left join mrp_workcenter w on (w.account_analytic_real = aaa.id)
                 --left join mrp_workcenter_productivity mwp on (mwp.workcenter_id = w.id)
                 --where mwp.workcenter_id = w.id
                 --group by w.id, w.name, aaa.code
                aaa.code ) as code
                from mrp_workcenter_productivity mwp
                left join mrp_workcenter w on (w.id = mwp.workcenter_id)
                left join account_analytic_account aaa on (aaa.id = w.account_analytic_real)
                where 1=1 and mwp.company_id = %s
                group by w.id, w.name, aaa.code, month, year, mwp.company_id) as subquery
                """ % (record.id)
        query += """);"""
        _logger.error(query)
        self.env.cr.execute(query)
    
#class MrpCostStructureSupra(models.AbstractModel):
 #   _name = 'report.distribution_assessment.distribution_assessment_structure'
  #  _description = 'MRP Distribution Assessment'

   # def get_lines(self, workorders):
    #    res = []
     #   workorder = []
      #  total_hours = []
       # query_str = """select row_number() OVER (ORDER BY w.id)as id,
        #                w.name as name,sum(mwp.duration)/60 as hours,sum(mwp.)
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
