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
    
    name = fields.Char('Production Order',readonly=True)
    centro = fields.Char('Code',readonly=True)
    operacion = fields.Char('Operation',readonly=True)
    centro_trabajo = fields.Char('Workcenter',readonly=True)
    ruta = fields.Char('Routing',readonly=True)
    horas = fields.Float('Hours',readonly=True)
    distribucion = fields.Float('Distribution', readonly=True)
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_cost')
        query = """
        CREATE or REPLACE VIEW report_cost AS( 
        with 
        mp as(select id,name,routing_id from mrp_production),
        mr as(select id,name  from mrp_routing),
        mrw as(select id,name,routing_id,workcenter_id from mrp_routing_workcenter),
        mw as(select id,name,code  from mrp_workcenter),
        ds as(select id,sum(costs_hour_real) as distribucion from mrp_workcenter group by id)
        select 
        row_number() OVER (ORDER BY mp.id) as id,mp.name,
        mrw.name AS operacion,mr.name AS ruta,mw.name as centro_trabajo,mw.costs_hour_real as horas,
        mw.code AS centro,(ds.distribucion*mw.costs_hour_real) as distribucion from  mp 
        join mrp_routing mr on mr.id = mp.routing_id 
        join mrp_routing_workcenter mrw on mrw.routing_id = mr.id 
        join mrp_workcenter mw on mw.id = mrw.workcenter_id
        join ds on mw.id = ds.id ORDER BY 1
        
        );
        """
        self.env.cr.execute(query)