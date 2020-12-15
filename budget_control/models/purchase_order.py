from odoo import models,api,fields
from odoo.exceptions import AccessDenied

import logging
_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    #product_account = fields.Many2one('account.account',compute='_compute_product_account')
    product_account = fields.Many2one('account.account', related='product_id.categ_id.property_account_expense_categ_id')
    
    @api.constrains('product_id')
    def _check(self):
        for record in self:
            if record.product_id:
                if not record.account_analytic_id:
                    if not record.analytic_tag_ids:
                        raise AccessDenied(("Debe seleccionar una cuenta analitica o una etiqueta analitica"))
            
    
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[('budget', 'Blocked to Approve')])
    bool_validation = fields.Boolean(compute='_compute_bool_validation')

    def _compute_bool_validation(self):
        user = self.env['res.users'].browse(self.env.uid)
        if user.has_group('budget_control.module_category_budget_control'):
            self.bool_validation = True
        else:
            self.bool_validation = False
    
    @api.onchange('date_order')
    def onchange_date_order(self):
        for line in self.order_line:
            line.date_planned = self.date_order

    def button_confirm_purchase(self):        
        if not self.validation():
            # res = self.action_create_activity()
            res = self.action_wizard_budget()
        else:
            for order in self:
                if order.state not in ['draft', 'sent','budget']:
                    continue
                order._add_supplier_to_product()
                # Deal with double validation process
                if order.company_id.po_double_validation == 'one_step'\
                        or (order.company_id.po_double_validation == 'two_step'\
                            and order.amount_total < self.env.company.currency_id._convert(
                                order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                        or order.user_has_groups('purchase.group_purchase_manager'):
                    order.button_approve()
                else:
                    order.write({'state': 'to approve'})
            res = True

        return res

    def validation(self):
        budget = self.env['crossovered.budget'].search([])
        for line in self.order_line:
            _logger.error("****************\nline: ")
            _logger.error(line.name)
            for record in budget.crossovered_budget_line:
                _logger.error("****************\ncrossovered_budget_line: ")
                total = 0
                _logger.error(record.name)
                if record.general_budget_id and record.analytic_account_id:
                    _logger.error("****************aqui es: *****************************")
                    _logger.error(record.analytic_account_id.name)
                    dic =  {}
                    account_ids = record.general_budget_id.account_ids.ids
                    
                    if line.product_account.id in account_ids and line.account_analytic_id == record.analytic_account_id:
                        _logger.error("\ncuenta encontrada: ")
                        purchase_ids = self.env['purchase.order.line'].search([('product_account','in',account_ids),
                            ('date_planned','>=',record.date_from),('date_planned','<=',record.date_to),('account_analytic_id','=',record.analytic_account_id.id)])
                        _logger.error(purchase_ids)

                        for purchase_obj in purchase_ids: 
                            if purchase_obj.order_id.state == 'purchase' or purchase_obj.order_id.state == 'done': 
                                total += purchase_obj.price_subtotal
                                dic['total'] = total 
                                print('Total ordenes confirmadas:',dic['total']) 
                                dic['date'] = purchase_obj.date_planned
                        _logger.error(total)    
                        if self.date_order.date() >= record.date_from and self.date_order.date() <= record.date_to:
                            for line2 in self.order_line:
                                if line2.product_account.id in account_ids:
                                    total += line.price_subtotal
                        _logger.error(total) 
                        if total > record.planned_amount:
                            return False

                elif record.general_budget_id and not record.analytic_account_id:
                    _logger.error("****************\n aqui es el que debo ver: ****************")
                    _logger.error(record.analytic_account_id.name)
                    dic =  {}
                    account_ids = record.general_budget_id.account_ids.ids
                    _logger.error("\ncuenta encontrada sin cuenta analitica: ")
                    if line.product_account.id in account_ids:
                        _logger.error("\ncuenta encontrada sin cuenta analitica: ")
                        purchase_ids = self.env['purchase.order.line'].search([('product_account','in',account_ids),
                            ('date_planned','>=',record.date_from),('date_planned','<=',record.date_to),('account_analytic_id','=',False)])
                        _logger.error(purchase_ids)

                        for purchase_obj in purchase_ids: 
                            if purchase_obj.order_id.state == 'purchase' or purchase_obj.order_id.state == 'done': 
                                total += purchase_obj.price_subtotal
                                dic['total'] = total 
                                print('Total ordenes confirmadas:',dic['total']) 
                                dic['date'] = purchase_obj.date_planned
                        _logger.error(total)    
                        if self.date_order.date() >= record.date_from and self.date_order.date() <= record.date_to:
                            for line2 in self.order_line:
                                if line2.product_account.id in account_ids and not line2.account_analytic_id:
                                    total += line.price_subtotal
                        _logger.error(total) 
                        if total > record.planned_amount:
                            return False
                    """for account in account_ids:
                        dic['account'] = account"""
        return True

    """def validation_budget(self, dic):
        flag = True
        #for record in self:
        if self.state != 'budget':
            domain = [('crossovered_budget_id.state', '=', 'done'), ('date_from', '<=', dic['date']),
                    ('date_to', '>=', dic['date']),('general_budget_id.account_ids','in',dic['account'])]
            lines = self.env['crossovered.budget.lines'].search(domain)
            for line in lines:
                if dic['total'] + self.amount_total > line.planned_amount:
                    flag = False  
        return flag"""

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
            wiz_id = self.env['wizard.purchase'].create(vals_wiz)
            action = imd.xmlid_to_object('budget_control.action_wizard_purchase')
            form_view_id = imd.xmlid_to_res_id('budget_control.view_wizard_purchase_form')
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