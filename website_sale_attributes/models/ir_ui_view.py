# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import copy
import logging
from lxml import etree, html

from odoo.exceptions import AccessError
from odoo import api, fields, models
from odoo.tools import pycompat

_logger = logging.getLogger(__name__)


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    @api.multi
    def render(self, values=None, engine='ir.qweb'):
        if values == None:
            return super(IrUiView, self).render(values=values, engine=engine)
        values['attrib_visible'] = []
        values['attrib_visible_all'] = []
        value = self.env['product.attribute'].search([])
        for attributes in self.env['product.attribute'].search([('website_variant', '=', True)]):
            if attributes.website_variant:
                value |= attributes
        values['attributes_all'] = value or []
        if values and (not values.get('category', False)):
            ids = set([])
            for x in values['attributes_all']:
                ids = ids | set([v.id for v in x.value_ids if v.website_variant])
            values['attrib_visible_all'] = list(ids)
        if values and values.get('attributes') and values.get('categories'):
            ids = set([])
            # values['products']
            categ_ids = list(set([x.categ_id.id for x in values['products']]))
            product_all = self.env['product.template'].search([('categ_id', 'in', categ_ids)])
            #_logger.info("TMPL %s:%s:%s" % (product_all, values.get('category') and values['category'].id or '', values.get('products') and values['products'].mapped('categ_id') or ''))
            for product in product_all:
                #_logger.info("VARIANT %s" % product)
                for x in product.attribute_line_ids:
                    if x.attribute_id.website_variant:
                        ids = ids | set([v.id for v in x.value_ids if v.website_variant])
            values['attrib_visible'] = list(ids)
        #_logger.info("VALUE %s" % values)
        return super(IrUiView, self).render(values=values, engine=engine)
