# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class Website(models.Model):
    _inherit = "website"

    website_filter_id = fields.Many2one('product.website.filter', string='Website Default Filter', required=True,
                                        help="Header based filters to make different brands on the Website pages (online filtered by brand)")
    website_filter_ids = fields.Many2many('product.website.filter', string='Website Product Filter',
                                        help="Header based filters to make different brands on the Website pages (online filtered by brand)")
    website_logo = fields.Binary(compute='_website_logo', store=True)
    website_nav_menu = fields.Binary(attachment=True, help="This field holds the image used as background menu image, limited to 1024x1024px.")


    @api.depends('website_filter_id', 'website_filter_id.image')
    def _website_logo(self):
        for website in self:
            website.website_logo = tools.image_resize_image(website.website_filter_id.image, (180, None))

    @tools.cache('domain_name')
    def _get_current_website_id(self, domain_name):
        domain_name_x = request and request.httprequest.environ.get('HTTP_HOST', '') or None

        website_filter = request.httprequest.environ.get('HTTP_X_ODOO_WEBSITEFILTER')
        domain = [('domain', '=', domain_name)]
        if self.website_filter_ids and website_filter:
            website_filter_ids = [x.id for x in self.website_filter_ids if x.filter_name == website_filter]
            domain += [('website_filter_ids', 'in', website_filter_ids)]
        website = self.search(domain, limit=1)
        _logger.info("x-Filter %s:%s:%s" % (domain, website_filter, domain_name_x))
        if not website:
            website = self.search([], limit=1)
        return website.id

