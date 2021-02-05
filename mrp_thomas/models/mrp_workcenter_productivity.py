# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(company_id, date_start, date_end, workorder_id, loss_id)',
         "The duration must be unique for loss"),
    ]

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_start > record.date_end:
                raise UserError(_("The start date cannot be greater than the end date"))

    activity_vat = fields.Char('Activity VAT')
    activity_code = fields.Char('Activity code')
    # date_start = fields.Datetime(copy=False)
    import_date = fields.Datetime('Import date')
