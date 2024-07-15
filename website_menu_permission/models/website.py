# -*- coding: utf-8 -*-
from odoo import models, api, tools
from odoo.addons.website.models.website import Website as website
from odoo.http import request


class PermissionWebsite(models.Model):
    _inherit = "website"

    @api.model
    def get_current_website(self):
        domain_name = request and request.httprequest.environ.get('HTTP_HOST', '').split(':')[0] or None
        website_id = self.sudo()._get_current_website_id(domain_name)
        if request:
            request.context = dict(request.context, website_id=website_id)
        return self.browse(website_id)

website.get_current_website = PermissionWebsite.get_current_website
