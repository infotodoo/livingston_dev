from odoo import models, fields, api

class IrCron(models.Model):
    _inherit = 'ir.cron'

    check_execute = fields.Boolean('Check execute accounts')

    
