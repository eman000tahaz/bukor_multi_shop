# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, exceptions

class ResUsersSecondInherit(models.Model):
	_inherit = 'res.users'

	@api.model
	def create(self, values):
		user_count = self.search_count([('id', '!=', 1)])
		if user_count >= 13:
			raise exceptions.ValidationError("You have exceeded the maximum number of users")
		return super(ResUsersSecondInherit, self).create(values)