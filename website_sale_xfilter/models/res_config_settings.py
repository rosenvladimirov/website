# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_logo = fields.Binary(string='Website Logo', related='website_id.website_logo')
    website_nav_menu = fields.Binary(string='Website Background for Menu', related='website_id.website_nav_menu')
    website_filter_id = fields.Many2one(string='Website Default Filter', related='website_id.website_filter_id', relation="product.website.filter", required=True)
