# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskService(models.Model):
    _name = 'helpdesk.service'

    name = fields.Char(string= 'Nombre')
    team_id = fields.Many2one('helpdesk.team', string='Equipo')
    ticket_type = fields.Selection([('incidents', 'Incidente'),('request','Solicitud')], string='Ticket type')