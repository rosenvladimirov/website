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
        if values and values.get('attributes') and not values.get('category'):
            values['attributes'] = None
        #if values and isinstance(values.get('attributes'), type(None)) == False:
        #    values['attributes'] = values['attributes'].filtered(lambda r: r.create_variant == False)
        #    ids = set([])
        #    for product in values['products']:
        #        for x in product.attribute_line_ids:
        #            if x.attribute_id.create_variant == False:
        #                ids = ids | set([v.id for v in x.value_ids])
        #    if ids:
        #        for attr in values['attributes']:
        #            attr['value_ids'] = attr['value_ids'].filtered(lambda r: r.id in list(ids))
        return super(IrUiView, self).render(values=values, engine=engine)
