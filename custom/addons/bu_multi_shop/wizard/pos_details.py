# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError
from lxml import etree

class PosDetailsInherit(models.TransientModel):
    _inherit = 'pos.details.wizard'

    @api.one
    def _get_current_shop_id(self):
        current_user = self.env['res.users'].search([('id', '=', self.env.uid)])
        if current_user.shop_id:
            return current_user.shop_id.id

    shop_id = fields.Many2one('shop', string='Shop', default=_get_current_shop_id)
    pos_config_ids = fields.Many2many('pos.config', 'pos_detail_configs', default="")

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(PosDetailsInherit, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])
        current_user = self.env['res.users'].search([('id', '=', self.env.uid)])
        if current_user.shop_id != False :
            for node in doc.xpath("//field[@name='shop_id']"):
                node.set('readonly', "1")
        if self.shop_id:
            for node in doc.xpath("//field[@name='pos_config_ids']"):
                node.set('domain', "[('shop_id', '=',"+self.shop_id.id+")]")
        res['arch'] = etree.tostring(doc)
        return res