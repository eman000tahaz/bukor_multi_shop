# -*- coding: utf-8 -*-

from odoo import fields, models


class RestaurantPrinterInherit(models.Model):

    _inherit = 'restaurant.printer'

    name = fields.Char('Name', required=True, default='Printer', help='An internal identification of the printer')
    proxy_ip = fields.Char('IP Address', help="The IP Address or hostname of the Printer's hardware proxy")
    product_categories_ids = fields.Many2many('pos.category', 'printer_category_rel', 'printer_id', 'category_id', string='Product Categories')
    config_id = fields.Many2one('pos.config', name="Point Of Sale")


class PosConfigInherit(models.Model):
    
    _inherit = 'pos.config'

    iface_splitbill = fields.Boolean(string='Bill Splitting', help='Enables Bill Splitting in the Point of Sale')
    iface_printbill = fields.Boolean(string='Bill Printing', help='Allows to print the Bill before payment')
    iface_orderline_notes = fields.Boolean(string='Orderline Notes', help='Allow custom notes on Orderlines')
    printer_ids = fields.One2many('restaurant.printer', 'config_id', string='Order Printers')
