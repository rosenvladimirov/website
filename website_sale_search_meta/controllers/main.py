# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

import logging
_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values):
        attr = []
        ids = []
        domain =  super()._get_search_domain(search, category, attrib_values)
        if search:
            attr = request.env["website.seo.product.metadata.keywords"].name_search(name=search)
            ids = [x[0] for x in attr]
            if ids:
                return [('website_meta_keyword_ids', 'in', ids)]
        return domain
