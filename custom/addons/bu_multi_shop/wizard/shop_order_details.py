# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class ShopOrderDetails(models.TransientModel):
    _name = 'shop.order.details.wizard'

    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    shop_id = fields.Many2one('shop', string='Shop')

    @api.onchange('end_date')
    def _onchange_end_date(self):
    	# if not self.start_date:
    	# 	raise ValidationError('Please Enter Start Date First !')
        if self.end_date and self.end_date < self.start_date:
        	raise ValidationError('End Date Is greater Than Start Date !')

    @api.multi
    def generate_report(self):
        data = {'date_start': self.start_date, 'date_stop': self.end_date, 'shop_id': self.shop_id.id}
        return self.env['report'].get_action(
            [], 'bu_multi_shop.report_shop_saledetails', data=data)
