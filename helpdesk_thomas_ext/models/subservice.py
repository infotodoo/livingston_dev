# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskSubServiceService(models.Model):
    _name = 'helpdesk.subservice'

    name = fields.Char(string="Nombre subservicio")
    service_id = fields.Many2one('helpdesk.service', string="Servicio relazionado")