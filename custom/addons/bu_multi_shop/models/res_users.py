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

	@api.multi
	def write(self, values):
		if 1 in self._ids and self.env.uid != 1:
			raise exceptions.ValidationError("You have no access to edit Administrator!")
		return super(ResUsersSecondInherit, self).write(values)
