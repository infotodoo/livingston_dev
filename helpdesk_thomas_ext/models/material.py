# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskMaterial(models.Model):
    _name = 'helpdesk.material'

    name = fields.Char(string= 'Nombre')
    material_ids = fields.Many2one('helpdesk.ticket', invisible=1)