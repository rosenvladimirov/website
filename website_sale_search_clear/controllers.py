from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale as controller

import logging
_logger = logging.getLogger(__name__)

class WebsiteSale(controller):

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        if category and search:
            category = None
        return super(WebsiteSale, self).shop(page, category, search, ppg, **post)
