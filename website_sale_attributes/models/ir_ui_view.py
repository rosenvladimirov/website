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
        if values and (not values.get('category', False)):
            ids = set([])
            product = self.env['product.product'].search([('website_published', '=', True)])
            values['attributes_all'] = self.env['product.attribute'].search([('website_variant', '=', True), ('attribute_line_ids.product_tmpl_id', 'in', product.ids)])
            for x in values['attributes_all']:
                ids = ids | set([v.id for v in x.value_ids])
            values['attrib_visible_all'] = list(ids)
        if values and values.get('attributes'):
            ids = set([])
            for product in values['products']:
                for x in product.attribute_line_ids:
                    if x.attribute_id.website_variant:
                        ids = ids | set([v.id for v in x.value_ids])
            values['attrib_visible'] = list(ids)
            product = self.env['product.product'].search([('website_published', '=', True)])
            values['attributes_all'] = self.env['product.attribute'].search([('website_variant', '=', True), ('attribute_line_ids.product_tmpl_id', 'in', product.ids)])
            #values['attributes_all'] = values.get('attributes')
        #_logger.info("Values %s" % values)
        return super(IrUiView, self).render(values=values, engine=engine)
