from odoo import models,fields,api,_

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    code = fields.Char(related='workcenter_id.code')
    hours = fields.Float('Hours')

