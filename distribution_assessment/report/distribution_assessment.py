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
    date_end = fields.Char('Date',readonly=True)
    hours = fields.Float('Hours',readonly=True)
    total_time = fields.Float('Total Times',readonly=True)
    percentage = fields.Float('%',readonly=True)
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
    check = fields.Boolean(related="company_id.laboratory")

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
                select 
                row_number() OVER (ORDER BY w.id)as id,mwp.company_id,
                w.name,sum(mwp.duration) as hours,to_char(mwp.date_end,'YYYY-MM') as date_end,
                (
                 select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp
                ) as total_time,
                (
                 sum(mwp.duration)/(select sum(p.duration) 
                 from mrp_workcenter_productivity p
                 where mwp.company_id = p.company_id)
                )as percentage,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join res_company rc on (rc.account_management_id = aml.account_id)
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 --left join res_company rc on (rc.management_id = aaa.id)
                 where rc.management_id = aaa.id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 --left join res_company rc on (rc.id = mwp.company_id))
                 )
                )as management,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.laboratory_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as laboratory,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.dispatch_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as dispatch,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.maintenance_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as maintenance,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.disused_assets_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as disused_assets,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.alternative_center_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as alternative_center,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.plan_department_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as plan_department_id,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.plan_department_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as shipping_department_id,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.plant_maintenance_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as plant_maintenance_id,
                 (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.plant_overhead_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as plant_overhead_id,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.transport_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as transport_id,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.rm_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as rm_id,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.plant_support_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as plant_support_id,
                 (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.proyect_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as proyect_id,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.warehouse_distribution_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as warehouse_distribution_id,
                 (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.prepress_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as prepress_id,
                (
                 (
                 select sum(aml.debit) 
                 from account_move_line aml
                 left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id)
                 left join res_company rc on (rc.supplies_id = aaa.id)
                 where rc.id = mwp.company_id
                 )
                 *
                 (
                 sum(mwp.duration)/(select sum(mwp.duration) 
                 from mrp_workcenter_productivity mwp)
                 )
                )as supplies_id,
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
                group by w.id, w.name, aaa.code, to_char(mwp.date_end,'YYYY-MM'), mwp.company_id
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
