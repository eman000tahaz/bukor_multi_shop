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
		('creep', 'Crepe'), 
		('drink', 'Drink'),
		('dessert', 'Dessert'),
		('pizza', 'Pizza'),
		('snacks', 'Snacks'),
		('add', 'Addition')], string='Food Type')
	basic = fields.Selection([('chicken', 'Chicken'), ('beef', 'Beef')], string='Basic')
	drink_type = fields.Selection([
		('s_drink', 'Soft Drinks'),
		('water', 'Water'),
		('juice', 'Juice')], string='Drink Type')
	size = fields.Selection([('large', 'Large'), ('small', 'Small'), ('galon', 'Galon')], string='Size')
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

	@api.model
	def get_pos_ref(self):
		current_user = self.env['res.users'].search([('id', '=', self.env.uid)])
		res = {}
		if current_user.shop_id :
			shop_id = current_user.shop_id.id
			shop_name = current_user.shop_id.name
			shop_orders_count = self.env['pos.order'].search_count([('shop_id', '=', shop_id)])
			last_order = self.env['pos.order'].search([], limit=1, order='id desc')
			pos_reference = 'Order '+ shop_name +"-"+ str(shop_orders_count+1) +"-"+ str(last_order.id+1)
			today_orders_count = self.env['pos.order'].search_count([('shop_id', '=', shop_id), ('today_date', '=', fields.Date.today())])
			if not today_orders_count:
				customer_order_no = 100
			else:
				customer_order_no = 100 + today_orders_count
		else:
			shop_name = False
			last_order = self.env['pos.order'].search([], limit=1, order='id desc')
			pos_reference = 'Order Manager' + "-" + str(last_order.id+1)
			today_orders_count = self.env['pos.order'].search_count([('today_date', '=', fields.Date.today())])
			if not today_orders_count:
				customer_order_no = 200
			else:
				customer_order_no = 200 + today_orders_count
		res['pos_reference'] = pos_reference
		res['customer_order_no'] = customer_order_no
		res['shop_name'] = shop_name
		# if shop_name == "Turk\'s Burger":
		# 	shop_name ='Turk'
		return res


	shop_id = fields.Many2one('shop', string='Shop', default=_get_shop_id)
	name = fields.Char(string='Order Ref', required=True, readonly=False, copy=False, default='/')
	pos_reference = fields.Char(string='Receipt Ref', readonly=True, copy=False, store=True)
	today_date = fields.Date(string='Date', default=fields.Date.today(), store=True)
	customer_order_no = fields.Integer('Customer No.')
	
	@api.model
	def create(self, values):
		values['today_date'] = fields.Date.today()
		if values.get('session_id'):
			# set name based on the sequence specified on the config
			session = self.env['pos.session'].browse(values['session_id'])
			values['name'] = session.config_id.sequence_id._next()
			current_user = self.env['res.users'].search([('id', '=', self.env.uid)])
			if current_user.shop_id :
				shop_id = current_user.shop_id.id
				shop_name = current_user.shop_id.name
				shop_orders_count = self.env['pos.order'].search_count([('shop_id', '=', shop_id)])
				last_order = self.env['pos.order'].search([], limit=1, order='id desc')
				values['pos_reference'] = 'Order '+ shop_name +"-"+ str(shop_orders_count+1) +"-"+ str(last_order.id+1)
				today_orders_count = self.env['pos.order'].search_count([('shop_id', '=', shop_id), ('today_date', '=', fields.Date.today())])
				if not today_orders_count:
					values['customer_order_no'] = 100
				else:
					values['customer_order_no'] = 100 + today_orders_count
			else:
				last_order = self.env['pos.order'].search([], limit=1, order='id desc')
				values['pos_reference'] = 'Order Manager' + "-" + str(last_order.id+1)
				today_orders_count = self.env['pos.order'].search_count([('today_date', '=', fields.Date.today())])
				if not today_orders_count:
					values['customer_order_no'] = 200
				else:
					values['customer_order_no'] = 200 + today_orders_count
			values.setdefault('pricelist_id', session.config_id.pricelist_id.id)
		else:
			# fallback on any pos.order sequence
			values['name'] = self.env['ir.sequence'].next_by_code('pos.order')
		return super(PosOrderInherit, self).create(values)
	