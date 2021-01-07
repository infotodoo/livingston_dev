# -*- coding: utf-8 -*-
#################################################################################
#
# 
# 
#################################################################################
from odoo import api, fields, models, _

class ResPartner(models.Model):
	_inherit = 'res.partner'

	wk_dob = fields.Date( string='Date of Birth')
	document_type = fields.Selection([('1','Cédula'),('2','Pasaporte'),('3','Cédula de extranjería'),('4','Trajeta de identidad')])

