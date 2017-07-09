# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from lxml import etree

class Shop(models.Model):
	_name = 'shop'

	name = fields.Char(string='shop')
	shop_type = fields.Selection([('store', 'Store'), ('restaurant', 'Restaurant')], string='Type')
	user_ids = fields.One2many('res.users', 'shop_id', string='Users', store=True)
	product_ids = fields.One2many('product.product', 'shop_id', string='Products', store=True)
	journal_ids = fields.One2many('account.journal', 'shop_id', string='Journals', store=True)
	image = fields.Binary('Image')

class ProductProductInherit(models.Model):
	_inherit = 'product.product'

	def _get_shop_id(self):
		if 'default_shop_id' in self.context:
			if self.context.default_shop_id:
				return self.context.default_shop_id

	shop_id = fields.Many2one('shop', string='Shop', default=_get_shop_id)

class AccountJournalInherit(models.Model):
	_inherit = 'account.journal'

	shop_id = fields.Many2one('shop', string='Shop')

class ResUsersInherit(models.Model):
	_inherit = 'res.users'

	shop_id = fields.Many2one('shop', string='Shop')
	shop_ids = fields.Char()	

class PosOrderLineInherit(models.Model):
    _inherit = "pos.order.line"

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    	res = super(PosOrderLineInherit, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    	doc = etree.XML(res['arch'])
    	current_user = self.env['res.users'].search([('id', '=', self.env.uid)])
        for node in doc.xpath("//field[@name='product_id']"):
        	node.set('domain', "[('shop_id', '=',"+current_user.shop_id.id+")]")
        res['arch'] = etree.tostring(doc)
        return res