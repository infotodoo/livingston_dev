# -*- coding: utf-8 -*-
from odoo import fields,models,api,_

class MrpPrelimitDistribution(models.Model):
    _name = 'mrp.prelimit.distribution'
    _description = 'mrp prelimit distribution'

    #first option
    first_account_id = fields.Many2one('account.account','From')
    second_account_id = fields.Many2one('account.account','To')
    extra_account1 = fields.Many2one('account.account','MOD Account 1')
    extra_account2 = fields.Many2one('account.account','MOD Account 2')
    extra_account3 = fields.Many2one('account.account','MOD Account 3')

    #second option
    first_option_account_id = fields.Many2one('account.account','From')
    second_option_account_id = fields.Many2one('account.account','To')
    exclude_account1 = fields.Many2one('account.account','Exclude CIF Account 1')
    exclude_account2 = fields.Many2one('account.account','Exclude CIF Account 2')

    #third option
    maq_account1 = fields.Many2one('account.account','Maq Account 1')
    maq_account2 = fields.Many2one('account.account','Maq Account 2')