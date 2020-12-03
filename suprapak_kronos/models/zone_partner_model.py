from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ZonePartnerSupraModel(models.Model):
    _name = 'res.zone.supra.model'
    
    name = fields.Char('Zona')
    code = fields.Char('codigo')
    
class ResSubSector(models.Model):
    _name = 'res.sub.sector'
    
    name = fields.Char('Zona')
    sector_id  = fields.Many2one('res.sector', 'Sector')
    
    
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    zone_s_id = fields.Many2one('res.zone.supra.model','Zona')
    sub_sector_id = fields.Many2one('res.sub.sector', 'Subsector')