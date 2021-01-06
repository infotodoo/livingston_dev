# -*- coding: utf-8 -*-
from odoo import fields,models,api

class ResCompany(models.Model):
    _inherit = "res.company"

    # account analytic by search in report
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
    
    #bools to condition
    management = fields.Boolean(compute="_compute_management")
    laboratory = fields.Boolean(compute="_compute_laboratory")
    dispatch = fields.Boolean(compute="_compute_dispatch")
    maintenance = fields.Boolean(compute="_compute_maintenance")
    disused_assets = fields.Boolean(compute="_compute_disused_assests")
    alternative_center = fields.Boolean(compute="_compute_alternative_center")
    plan_department = fields.Boolean(compute="_compute_plan_department")
    shipping_department = fields.Boolean(compute="_compute_shipping_department")
    plant_maintenance = fields.Boolean(compute="_compute_plant_maintenance")
    plant_overhead = fields.Boolean(compute="_compute_plant_overhead")
    transport = fields.Boolean(compute="_compute_transport")
    rm = fields.Boolean(compute="_compute_rm")
    plant_support = fields.Boolean(compute="_compute_plant_support")
    proyect = fields.Boolean(compute="_compute_proyect")
    warehouse_distribution = fields.Boolean(compute="_compute_warehouse_distribution")
    prepress = fields.Boolean(compute="_compute_prespress")
    supplies = fields.Boolean(compute="_compute_supplies")
    
    #function
    @api.depends('management_id')
    def _compute_management(self):
        if self.management_id:
            self.management = True
        else:
            self.management = False
            
    @api.depends('laboratory_id')        
    def _compute_laboratory(self):
        if self.laboratory_id:
            self.laboratory = True
        else:
            self.laboratory = False
            
    @api.depends('dispatch_id')
    def _compute_dispatch(self):
        if self.dispatch_id:
            self.dispatch = True
        else:
            self.dispatch = False
            
    @api.depends('maintenance_id')
    def _compute_maintenance(self):
        if self.maintenance_id:
            self.maintenance = True
        else:
            self.maintenance = False
            
    @api.depends('disused_assets_id')
    def _compute_disused_assests(self):
        if self.disused_assets_id:
            self.disused_assets = True
        else:
            self.disused_assets = False
            
    @api.depends('alternative_center_id')
    def _compute_alternative_center(self):
        if self.alternative_center_id:
            self.alternative_center = True
        else:
            self.alternative_center = False
            
    @api.depends('plan_department_id')
    def _compute_plan_department(self):
        if self.plan_department_id:
            self.plan_department = True
        else:
            self.plan_department = False
            
    @api.depends('shipping_department_id')
    def _compute_shipping_department(self):
        if self.shipping_department_id:
            self.shipping_department = True
        else:
            self.shipping_department = False
            
    @api.depends('plant_maintenance_id')
    def _compute_plant_maintenance(self):
        if self.plant_maintenance_id:
            self.plant_maintenance = True
        else:
            self.plant_maintenance = False
            
    @api.depends('plant_overhead_id')
    def _compute_plant_overhead(self):
        if self.plant_overhead_id:
            self.plant_overhead = True
        else:
            self.plant_overhead = False
            
    @api.depends('transport_id')
    def _compute_transport(self):
        if self.transport_id:
            self.transport = True
        else:
            self.transport = False
            
    @api.depends('rm_id')
    def _compute_rm(self):
        if self.rm_id:
            self.rm = True
        else:
            self.rm = False
            
    @api.depends('plant_support_id')
    def _compute_plant_support(self):
        if self.plant_support_id:
            self.plant_support = True
        else:
            self.plant_support = False
        
    @api.depends('proyect_id')
    def _compute_proyect(self):
        if self.proyect_id:
            self.proyect = True
        else:
            self.proyect = False
            
    @api.depends('warehouse_distribution_id')
    def _compute_warehouse_distribution(self):
        if self.warehouse_distribution_id:
            self.warehouse_distribution = True
        else:
            self.warehouse_distribution = False
            
    @api.depends('prepress_id')
    def _compute_prespress(self):
        if self.prepress_id:
            self.prepress = True
        else:
            self.prepress = False
    
    @api.depends('supplies_id')
    def _compute_supplies(self):
        if self.supplies_id:
            self.supplies = True
        else:
            self.supplies = False
    