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
        if values and values.get('attributes'):
            ids = set([])
            for product in values['products']:
                for x in product.attribute_line_ids:
                    if x.attribute_id.create_variant == False:
                        ids = ids | set([v.id for v in x.value_ids])
            values['attrib_visible'] = list(ids)
            values['attrib_visible_all'] = self.env['product.attribute'].search([])
        #_logger.info("Filters %s" % values)
        return super(IrUiView, self).render(values=values, engine=engine)
