# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    main = fields.Boolean("Set Main on Website")
    on_website = fields.Boolean("Hide on Website")
