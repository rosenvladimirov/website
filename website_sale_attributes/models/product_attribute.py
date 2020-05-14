# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    website_variant = fields.Boolean(default=True, help="Check this if you want to show variant for this attribute on website.")


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    website_variant = fields.Boolean(default=True, help="Check this if you want to show variant for this attribute on website.")

