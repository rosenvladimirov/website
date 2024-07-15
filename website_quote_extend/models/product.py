# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp

from odoo.tools import pycompat
from odoo.tools.translate import html_translate
from odoo.tools import float_is_zero


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    website_list_price = fields.Float('Website public price', compute='_website_list_price', digits=dp.get_precision('Product Price'))

    def _website_list_price(self):
        self = self.filtered('product_variant_id')
        for template, product in pycompat.izip(self, self.mapped('product_variant_id')):
            template.website_list_price = product.website_list_price

class Product(models.Model):
    _inherit = "product.product"

    website_list_price = fields.Float('Website public price', compute='_website_list_price', digits=dp.get_precision('Product Price'))

    def _website_list_price(self):
        qty = self._context.get('quantity', 1.0)
        partner = self.env.user.partner_id
        current_website = self.env['website'].get_current_website()
        pricelist = current_website.get_current_pricelist()
        company_id = current_website.company_id

        context = dict(self._context, pricelist=pricelist.id, partner=partner)
        self2 = self.with_context(context) if self._context != context else self

        ret = self.env.user.has_group('sale.group_show_price_subtotal') and 'total_excluded' or 'total_included'

        for p, p2 in pycompat.izip(self, self2):
            taxes = partner.property_account_position_id.map_tax(p.sudo().taxes_id.filtered(lambda x: x.company_id == company_id))
            p.website_list_price = taxes.compute_all(p.list_price, pricelist.currency_id)[ret]
