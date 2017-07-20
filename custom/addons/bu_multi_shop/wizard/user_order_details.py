# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class UserOrderDetails(models.TransientModel):
    _name = 'user.order.details.wizard'

    def _get_user_domain(self):
        current_user = self.env['res.users'].search([('id', '=', self.env.uid)])
        if current_user.shop_id:
            return [('shop_id', '=', current_user.shop_id.id)]


    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    user_id = fields.Many2one('res.users', string='UserOrderDetails', domain=_get_user_domain)

    @api.onchange('end_date')
    def _onchange_end_date(self):
    	# if not self.start_date:
    	# 	raise ValidationError('Please Enter Start Date First !')
        if self.end_date and self.end_date < self.start_date:
        	raise ValidationError('End Date Is greater Than Start Date !')

    @api.multi
    def generate_report(self):
        data = {'date_start': self.start_date, 'date_stop': self.end_date, 'user_id': self.user_id.id}
        return self.env['report'].get_action(
            [], 'bu_multi_shop.report_user_saledetails', data=data)
