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
	pos_ids = fields.One2many('pos.config', 'shop_id', string='Points Of Sale', store=True)


class ProductProductInherit(models.Model):
	_inherit = 'product.product'

	shop_id = fields.Many2one('shop', string='Shop')
	shop_type = fields.Selection([('store', 'Store'), ('restaurant', 'Restaurant')], 
		related='shop_id.shop_type')
	food_type = fields.Selection([
		('sandwich', 'Sandwich'), 
		('box', 'Box'), 
		('creep', 'Creep'), 
		('drink', 'Drink'),
		('dessert', 'Dessert'),
		('pizza', 'Pizza'),
		('snacks', 'Snacks')], string='Food Type')
	basic = fields.Selection([('chicken', 'Chicken'), ('beef', 'Beef')], string='Basic')
	drink_type = fields.Selection([
		('s_drink', 'Soft Drinks'),
		('water', 'Water'),
		('juice', 'Juice')], string='Drink Type')
	size = fields.Selection([('large', 'Large'), ('small', 'Small')], string='Size')
	lettuce = fields.Boolean(string='Lettuce')
	tomato = fields.Boolean(string='Tomatoes')
	onion = fields.Boolean(string='Onions')
	bread = fields.Boolean(string='Bread')
	meal = fields.Boolean(string='Is Meal')
	ka_sauce = fields.Boolean(string='ketchup')
	hot_sauce = fields.Boolean(string='Hot Sauce')
	mayo = fields.Boolean(string='Mayonnaise')
	mustard = fields.Boolean(string='Mustard')
	garlic = fields.Boolean(string='Garlic')
	tast = fields.Selection([('spicy', 'Spicy'), ('normal', 'Normal')], string='Tast')
	extra_souce = fields.Boolean(string='Extra Souce')
	cheese = fields.Boolean(string='Cheese')

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

class PosConfigInherit(models.Model):
	_inherit = "pos.config"

	shop_id = fields.Many2one('shop', string='Shop')

class PosOrderInherit(models.Model):
	_inherit = "pos.order"

	def _get_shop_id(self):
		current_user = self.env['res.users'].search([('id', '=', self.env.uid)])
		if current_user.shop_id:
			return current_user.shop_id.id

	shop_id = fields.Many2one('shop', string='Shop', default=_get_shop_id)