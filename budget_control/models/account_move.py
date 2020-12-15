# -*- coding: utf-8 -*-
from odoo import models, api, fields
import datetime
from odoo.exceptions import AccessDenied
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    bool_validation = fields.Boolean(compute='_compute_bool_validation')

    def _compute_bool_validation(self):
        user = self.env['res.users'].browse(self.env.uid)
        if user.has_group('budget_control.module_category_budget_control'):
            self.bool_validation = True
        else:
            self.bool_validation = False
    
    def validation_invoices(self):
        _logger.error("****************\nlineeeeeeeeeeeeeeeeeeeeeeeeee: ")
        subtotal = 0
        for rec in self.invoice_line_ids:
            budget = self.env['crossovered.budget.lines'].search([('date_from','<=',rec.date),('date_to','>=',rec.date),('analytic_account_id','=',rec.analytic_account_id.id)])
            _logger.error(budget)
            for record in budget:
                count_ids = record.general_budget_id.account_ids.ids
                if rec.account_id.id in count_ids:
                    subtotal += rec.price_subtotal
                    if record.practical_amount*(-1) + subtotal > record.planned_amount:
                        _logger.error("****************\nline: ")
                        _logger.error(record.practical_amount*(-1))
                        self.action_wizard_budget()
                        self.action_post()
                    else:
                        _logger.error("****************\npost: ")
                        self.action_post()
                        return True

    def action_wizard_budget(self):
        imd = self.env['ir.model.data']
        for record in self:
            partners = record.message_follower_ids.partner_id.ids
            users = self.env['res.users'].search([('partner_id.id', 'in', partners)])
            ids = []
            for user in users:
                ids.append((4, user.id))
            vals_wiz = {
                'message': 'Superó el presupuesto estimado, por favor notifique con el area encargada',
                'users_ids': ids,
            }
            wiz_id = self.env['wizard.account'].create(vals_wiz)
            action = imd.xmlid_to_object('budget_control.action_wizard_account')
            form_view_id = imd.xmlid_to_res_id('budget_control.view_wizard_account_form')
            return {
                'name': action.name,
                'help': action.help,
                'type': action.type,
                'views': [(form_view_id, 'form')],
                'view_id': form_view_id,
                'target': action.target,
                'context': action.context,
                'res_model': action.res_model,
                'res_id': wiz_id.id,
            }