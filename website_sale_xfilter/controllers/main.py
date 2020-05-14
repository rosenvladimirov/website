# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute

import logging
_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values):
        attr = []
        ids = []
        website_filter = request.httprequest.environ.get('HTTP_X_ODOO_WEBSITEFILTER')
        domain =  super()._get_search_domain(search, category, attrib_values)
        if search:
            domain.insert(1, "|")
            domain += [('barcode', 'ilike', search), ('seller_ids.product_code', 'ilike', search), ('seller_ids.product_name', 'ilike', search)]
            attr = request.env["product.attribute.line"].name_search(name=search)
            ids = [x[0] for x in attr]
            if ids:
                return [('attribute_line_ids', 'in', ids)]
        if website_filter:
            ids = request.env['product.website.filter'].search([('filter_name', '=', website_filter)])
            if len(ids) > 0:
                domain += [('product_variant_ids.website_filter_ids', 'in', [x.id for x in ids])]
        #_logger.info("Filter %s:%s:%s:%s" % (attrib_values, domain, attr, ids))
        return domain

