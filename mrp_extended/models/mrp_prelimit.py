# -*- coding: utf-8 -*-
from odoo import models,fields,api,_
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class MrpPrelimit(models.Model):
    _name = 'mrp.prelimit'
    _description = 'mrp prelimit'
    _rec_name = 'workcenter_id'

    prelimit_code = fields.Char(related='workcenter_id.code')
    workcenter_id = fields.Many2one('mrp.workcenter','Workcenter')
    date_start = fields.Date()
    date_end = fields.Date()
    production_id = fields.Many2one('mrp.production','Production Order')
    hours = fields.Float('Hours')
    distribution = fields.Float(compute='_compute_distribution')
    distribution_percentage = fields.Float('% Distribution',compute='_compute_distribution_percentage')
    cost_mod = fields.Float(compute='_compute_cost_mod')
    cost_cif = fields.Float(compute='_compute_cost_cif')
    cost_maq = fields.Float(compute='_compute_cost_maq')
    
    
    @api.depends('workcenter_id')
    def _compute_distribution_percentage(self):
        for record in self:
            if record.workcenter_id and record.distribution != 0:
                account_obj = record.env['account.move']
                account_date = """
                               select to_char(date,'MM-YYYY') from account_move
                               group by to_char(date,'MM-YYYY');
                               """
                record.env.cr.execute(account_date, (tuple(account_obj.ids), ))
                for date in record.env.cr.fetchall():
                    _logger.error(record.date_end.strftime("%m-%Y"))
                    _logger.error(date)
                    for i in date:
                        if i == record.date_end.strftime("%m-%Y"):
                            record.distribution_percentage = record.hours/record.distribution
                        else:
                            _logger.error("--------------distribution-----------------------------------")
                            _logger.error(record.date_end.strftime("%m-%Y"))
                            _logger.error(date)
                            record.distribution_percentage = 0
            else:
                record.distribution_percentage = 0
    
    
    @api.depends('workcenter_id')
    def _compute_cost_maq(self):
        for record in self:
            record.cost_maq = 0
            prelimit = record.env['mrp.prelimit']
            if record.workcenter_id:
                account_id_maq = """
                                select to_char(am.date,'MM-YYYY'),sum(aml.debit) from account_move_line aml 
                                left join account_account aa on (aa.id = aml.account_id) 
                                left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id) 
                                left join mrp_workcenter wc on (wc.account_analytic_real 
                                = aml.analytic_account_id) 
                                left join account_account_account_tag aaat on 
                                (aaat.account_account_id = aa.id) 
                                left join account_move am on (am.id = aml.move_id) 
                                where aml.analytic_account_id = wc.account_analytic_real 
                                and aaat.account_account_tag_id = 11 and am.state = 'posted' 
                                and am.state = 'posted' group by to_char(am.date,'MM-YYYY'); 
                                """
                record.env.cr.execute(account_id_maq, (tuple(prelimit.ids), ))
                for date,debit in record.env.cr.fetchall():
                    if date == record.date_end.strftime("%m-%Y"):
                        account_maq = debit
                        record.cost_maq = record.distribution_percentage * account_maq
                    else:
                        record.cost_maq = 0
            else:
                record.cost_maq = 0
                
    
    @api.depends('workcenter_id')
    def _compute_cost_cif(self):
        for record in self:
            record.cost_cif = 0
            prelimit = record.env['mrp.prelimit']
            if record.workcenter_id:
                account_id_cif = """
                                select to_char(am.date,'MM-YYYY'),sum(aml.debit) from account_move_line aml 
                                left join account_account aa on (aa.id = aml.account_id) 
                                left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id) 
                                left join mrp_workcenter wc on (wc.account_analytic_real 
                                = aml.analytic_account_id) 
                                left join account_account_account_tag aaat on 
                                (aaat.account_account_id = aa.id) 
                                left join account_move am on (am.id = aml.move_id) 
                                where aml.analytic_account_id = wc.account_analytic_real 
                                and aaat.account_account_tag_id = 10 and am.state = 'posted' 
                                and am.state = 'posted' group by to_char(am.date,'MM-YYYY');  
                                """
                record.env.cr.execute(account_id_cif, (tuple(prelimit.ids), ))
                for date,debit in record.env.cr.fetchall():
                    if date == record.date_end.strftime("%m-%Y"):
                        _logger.error('-------------------------date----------------')
                        _logger.error(date)
                        account_cif = debit
                        record.cost_cif = record.distribution_percentage * account_cif
                    else:
                        record.cost_cif = 0
            else:
                record.cost_cif = 0
                
            
    @api.depends('workcenter_id')
    def _compute_cost_mod(self):
        for record in self:
            record.cost_mod = 0
            prelimit = record.env['mrp.prelimit']
            if record.workcenter_id:
                account_id_mod = """
                                select to_char(am.date,'MM-YYYY'),sum(aml.debit) from account_move_line aml 
                                left join account_account aa on (aa.id = aml.account_id) 
                                left join account_analytic_account aaa on (aaa.id = aml.analytic_account_id) 
                                left join mrp_workcenter wc on (wc.account_analytic_real 
                                = aml.analytic_account_id) 
                                left join account_account_account_tag aaat on 
                                (aaat.account_account_id = aa.id) 
                                left join account_move am on (am.id = aml.move_id) 
                                where aml.analytic_account_id = wc.account_analytic_real 
                                and aaat.account_account_tag_id = 10 and am.state = 'posted' 
                                and am.state = 'posted' group by to_char(am.date,'MM-YYYY'); 
                                """
                record.env.cr.execute(account_id_mod, (tuple(prelimit.ids), ))
                for date,debit in record.env.cr.fetchall():
                    if date == record.date_end.strftime("%m-%Y"):
                        account_mod = debit
                        record.cost_mod = record.distribution_percentage * account_mod
                    else:
                        record.cost_mod = 0
            else:
                record.cost_mod = 0
                
    
    @api.depends('hours')
    def _compute_distribution(self):
        for record in self:
            record.distribution = sum( record.env['mrp.prelimit'].search([('workcenter_id','=',record.workcenter_id.id),('date_end','=',record.date_end)]).mapped('hours'))
            #record.distribution = sum(record.env['mrp.prelimit'].browse([record.workcenter_id.id].mapped('hours')))
                
                
    def prelimit_journal(self):
        today = datetime.now()
        date = today.strftime("%d/%m/%Y")
        account_obj = self.env['account.move']
        for record in self:
            mod = []
            cif = []
            maq = []
            if record.cost_mod and record.workcenter_id and record.production_id:
                line = {
                        'name': record.production_id.name + ' - ' + record.workcenter_id.name+' - '+record.workcenter_id.account_analytic_real.name,
                        #'partner_id': partner_id,
                        'debit': record.cost_mod,
                        'credit': 0.00,
                        'account_id': record.workcenter_id.mod_account_id_real.id
                        }
                mod.append((0,0,line))
                line = {
                        'name': record.production_id.name + ' - ' + 'Contrapartida -' + record.workcenter_id.name+' - '+record.workcenter_id.account_analytic_real.name,
                        #'partner_id': partner_id,
                        'debit': 0.00,
                        'credit': record.cost_mod,
                        'account_id': record.workcenter_id.account_mod_id_real.id
                        }
                mod.append((0,0,line))
            if record.cost_cif and record.workcenter_id and record.production_id:
                line = {
                        'name': record.production_id.name + ' - ' + record.workcenter_id.name+' - '+record.workcenter_id.account_analytic_real.name,
                        #'partner_id': partner_id,
                        'debit': record.cost_cif,
                        'credit': 0.00,
                        'account_id': record.workcenter_id.mod_account_id_real.id
                        }
                cif.append((0,0,line))
                line = {
                        'name': record.production_id.name + ' - ' + 'Contrapartida -' + record.workcenter_id.name+' - '+record.workcenter_id.account_analytic_real.name,
                        #'partner_id': partner_id,
                        'debit': 0.00,
                        'credit': record.cost_cif,
                        'account_id': record.workcenter_id.account_cif_id_real.id
                        }
                cif.append((0,0,line))
            if record.cost_maq and record.workcenter_id and record.production_id:
                line = {
                        'name': record.production_id.name + ' - ' + record.workcenter_id.name+' - '+record.workcenter_id.account_analytic_real.name,
                        #'partner_id': partner_id,
                        'debit': record.cost_maq,
                        'credit': 0.00,
                        'account_id': record.workcenter_id.mod_account_id_real.id
                        }
                maq.append((0,0,line))
                line = {
                        'name': record.production_id.name + ' - ' + 'Contrapartida -' + record.workcenter_id.name+' - '+record.workcenter_id.account_analytic_real.name,
                        #'partner_id': partner_id,
                        'debit': 0.00,
                        'credit': record.cost_maq,
                        'account_id': record.workcenter_id.account_maq_id_real.id
                        }
                maq.append((0,0,line))
            acc_move_ids = []
            if mod:
                move = {
                        'journal_id': record.production_id.product_id.categ_id.property_stock_journal.id,
                        'line_ids': mod,
                        'date': fields.Date.today(),
                        'ref': record.production_id.name + ' - MOD'+' - '+record.workcenter_id.account_analytic_real.name,
                        'type': 'entry'
                        }
                account_move = account_obj.sudo().create(move)
                account_move.post()
                acc_move_ids.append(account_move.id)
            if cif:
                move = {
                        'journal_id': record.production_id.product_id.categ_id.property_stock_journal.id,
                        'line_ids': mod,
                        'date': fields.Date.today(),
                        'ref': record.production_id.name + ' - CIF'+' - '+record.workcenter_id.account_analytic_real.name,
                        'type': 'entry'
                        }
                account_move = account_obj.sudo().create(move)
                account_move.post()
                acc_move_ids.append(account_move.id)
            if maq:
                move = {
                        'journal_id': record.production_id.product_id.categ_id.property_stock_journal.id,
                        'line_ids': mod,
                        'date': fields.Date.today(),
                        'ref': record.production_id.name + ' - MAQ'+' - '+record.workcenter_id.account_analytic_real.name,
                        'type': 'entry'
                        }
                account_move = account_obj.sudo().create(move)
                account_move.post()
                acc_move_ids.append(account_move.id)