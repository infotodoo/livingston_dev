# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    billing_cut = fields.Selection(string='billing cut day', related='partner_id.billing_cut_day')
    # is_tst = fields.Boolean('is_tst', related='company_id.is_tst')
