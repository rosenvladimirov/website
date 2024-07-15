#  -*- coding: utf-8 -*-
#  Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from ipaddress import IPv4Network

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale as websitesale
from odoo.http import request

_logger = logging.getLogger(__name__)


class WebsiteSale(websitesale):

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        if 'HTTP_X_FORWARDED_FOR' in request.httprequest.environ:
            ip = request.httprequest.environ["HTTP_X_FORWARDED_FOR"]
        else:
            ip = request.httprequest.environ['REMOTE_ADDR'] if request else 'n/a'

        if not IPv4Network(ip).is_private and request.env.user._is_public() and not request.env['product.template'].search([('website_published', '=', True)]):
            _logger.info("Blocked shop page:%s Page not found 404 -", ip, )
            return request.render('website.404')
        return super().shop(page=page, category=category, search=search, ppg=ppg, **post)
