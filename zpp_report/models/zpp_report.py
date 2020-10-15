from odoo import _, fields,api, models

class ZppReport(models.Model):
    _name = 'zpp.report'
    _description = 'This is the report ZPP'
    _inherit = ['mrp.production', 'mrp.workorder','account.analytic.account']