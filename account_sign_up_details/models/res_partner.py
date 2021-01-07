# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models, _

class ResPartner(models.Model):
	_inherit = 'res.partner'

	wk_dob = fields.Date( string='Date of Birth')

