# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class Product(models.Model):
    _inherit = "product.template"

    website_meta_product_id = fields.Many2one("website.seo.product.metadata", string="Meta data")
    website_meta_title = fields.Char(related="website_meta_product_id.website_meta_title", string="Website meta title")
    website_meta_description = fields.Text(related="website_meta_product_id.website_meta_description", string="Website meta description")
    website_meta_keyword_ids = fields.Many2many("website.seo.product.metadata.keywords", relation="website_seo_rel")

class SeoProductsMetadata(models.Model):

    _name = 'website.seo.product.metadata'
    _description = 'SEO metadata for products'

    name = fields.Char("SEO name")
    website_meta_title = fields.Char("Website meta title", translate=True)
    website_meta_description = fields.Text("Website meta description", translate=True)
    display_name = fields.Char(compute='_compute_display_name')

    @api.depends('website_meta_title', 'website_meta_description')
    def _compute_display_name(self):
        for seo in self:
            seo.display_name = "[%s] %s" % (seo.name, seo.website_meta_title)

class SeoProductsKeywordsMetadata(models.Model):

    _name = 'website.seo.product.metadata.keywords'
    _description = 'SEO keywords metadata for products'

    name = fields.Char("Keyword name")
    website_meta_keywords = fields.Char("Website meta keywords", translate=True)
    display_name = fields.Char(compute='_compute_display_name')

    @api.depends('website_meta_keywords')
    def _compute_display_name(self):
        for seo in self:
            seo.display_name = "[%s] %s" % (seo.name, seo.website_meta_keywords)
