# -*- coding: utf-8 -*-
from odoo import fields,models,api

class ResCompany(models.Model):
    _inherit = "res.company"

    management_id = fields.Many2one('account.analytic.account','Operation Management')
    laboratory_id = fields.Many2one('account.analytic.account','Laboratory')
    dispatch_id = fields.Many2one('account.analytic.account','Dispatch')
    maintenance_id = fields.Many2one('account.analytic.account','Maintenance')
    disused_assets_id = fields.Many2one('account.analytic.account','Disused Assets')
    alternative_center_id = fields.Many2one('account.analytic.account','Alternative Center')
    plan_department_id = fields.Many2one('account.analytic.account','Plan Department')
    shipping_department_id = fields.Many2one('account.analytic.account','Shipping Department')
    plant_maintenance_id = fields.Many2one('account.analytic.account','Plan Maintenance')    
    plant_overhead_id = fields.Many2one('account.analytic.account','Plan Overhead')
    transport_id = fields.Many2one('account.analytic.account','Transport Cost')
    rm_id = fields.Many2one('account.analytic.account','Rm Interv Consum')
    plant_support_id = fields.Many2one('account.analytic.account','Plant Support')
    proyect_id = fields.Many2one('account.analytic.account','Proyect Movie Plant')       
    warehouse_distribution_id = fields.Many2one('account.analytic.account','Warehouse')
    prepress_id = fields.Many2one('account.analytic.account','Prepress')    
    supplies_id = fields.Many2one('account.analytic.account','Supplies')   