# -*- coding: utf-8 -*-
from odoo import models, api, fields
import datetime
from odoo.exceptions import AccessDenied


class CrossoveredBudgetLines(models.Model):
    _inherit = 'crossovered.budget.lines'

    purchase_mount = fields.Float('Purchase Mount', compute="_compute_purchase_mount")

    def _compute_purchase_mount(self):
        for record in self:
            if record.general_budget_id and record.analytic_account_id:
                account_ids = record.general_budget_id.account_ids.ids
                purchase_ids = self.env['purchase.order.line'].search([('product_account','in',account_ids),
                ('date_planned','>=',record.date_from),('date_planned','<=',record.date_to),('account_analytic_id','=',record.analytic_account_id.id)])
                total = 0
                dic =  {}
                dic['total'] = 0
                for purchase_obj in purchase_ids:
                    if purchase_obj.order_id.state == 'purchase' or purchase_obj.order_id.state == 'done':
                        if purchase_obj.product_account.id in account_ids:    
                            total += purchase_obj.price_subtotal
                            dic['total'] = total
                            dic['date'] = purchase_obj.date_planned
                record.purchase_mount = dic['total'] if dic['total'] else 0

            elif record.general_budget_id and not record.analytic_account_id:
                account_ids = record.general_budget_id.account_ids.ids
                purchase_ids = self.env['purchase.order.line'].search([('product_account','in',account_ids),
                ('date_planned','>=',record.date_from),('date_planned','<=',record.date_to),('account_analytic_id','=',False)])
                total = 0
                dic =  {}
                dic['total'] = 0
                for purchase_obj in purchase_ids:
                    if purchase_obj.order_id.state == 'purchase' or purchase_obj.order_id.state == 'done':
                        if purchase_obj.product_account.id in account_ids:    
                            total += purchase_obj.price_subtotal
                            dic['total'] = total
                            dic['date'] = purchase_obj.date_planned
                record.purchase_mount = dic['total'] if dic['total'] else 0