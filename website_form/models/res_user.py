# -*- coding: utf-8 -*-
#################################################################################
#
# 
# 
#
#
#################################################################################
from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
	_inherit = 'res.users'

	@api.model
	def signup(self, values, token=None):
		
		
		if token:
			partner = self.env['res.partner']._signup_retrieve_partner(token, check_validity=True, raise_exception=True)
			partner_user = partner.user_ids and partner.user_ids[0] or False
			if partner_user:

				values['wk_dob'] = values.get('wk_dob')
		else:
			
			values['wk_dob'] = values.get('wk_dob')
		return super(ResUsers, self).signup(values, token)