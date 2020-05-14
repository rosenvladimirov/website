# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import json
from difflib import SequenceMatcher

import logging
_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values):
        domain = request.website.sale_product_domain()
        if search and len(search.split(" "))>1:
            request.env.cr.execute("SELECT set_limit(0.3);")
            domain += [
                '|', '|', '|', ('name', '%', search), ('description', '%', search),
                ('description_sale', '%', search), ('product_variant_ids.default_code', '%', search)]
        elif search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', ('name', 'ilike', srch), ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch)]

        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]
        #request.set_cookie("key_rang", search)
        return domain

    @http.route(['/shop/get_suggest'], type='http', auth="public", methods=['GET'], website=True)
    def get_suggest_json(self, **kw):
        query = kw.get('query')
        results = []
        names = query.split(' ')
        domain = self._get_search_domain(query, '', '')
        #domain = super()._get_search_domain(".".join(names), '', '')
        products = request.env['product.template'].search(domain, limit=10)
        #_logger.info("Doamin ________ %s" % domain)
        if not products:
            attr = request.env["product.attribute.line"].name_search(name=".".join(names))
            ids = [x[0] for x in attr]
            if ids:
                products = request.env['product.template'].search([('attribute_line_ids', 'in', ids)])
        if not products:
            # second search for supplier code or barcode
            domain = ["|"] + [('seller_ids.product_code', 'ilike', ".".join(names))] + [('seller_ids.product_name', 'ilike', ".".join(names))]
            products = request.env['product.template'].search(domain)
        products = sorted(products, key=lambda x: SequenceMatcher(None, query.lower(), x.name.lower()).ratio(),
                          reverse=True)
        for product in products:
            results.append({'value': product.name, 'data': {'id': product.id, 'after_selected': product.name}})
        return json.dumps({
            'query': 'Unit',
            'suggestions': results
        })

