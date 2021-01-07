# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

import logging
from odoo.http import request
from odoo.exceptions import UserError
from odoo.addons.web.controllers.main import ensure_db, Home

_logger = logging.getLogger(__name__)

class AuthSignupHome(Home):
	def do_signup(self, qcontext):
		""" Shared helper that creates a res.partner out of a token """
		
		values = { key: qcontext.get(key) for key in ('login', 'name', 'password', 'wk_dob') }
		if not values:
			raise UserError(_("The form was not properly filled in."))
		if values.get('password') != qcontext.get('confirm_password'):
			raise UserError(_("Passwords do not match; please retype them."))
		supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
		lang = request.context.get('lang', '').split('_')[0]
		if lang in supported_lang_codes:
			values['lang'] = lang
		self._signup_with_values(qcontext.get('token'), values)
		request.env.cr.commit()
	
