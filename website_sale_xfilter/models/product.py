# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _

import logging
_logger = logging.getLogger(__name__)

class ProductWebsiteFilters(models.Model):
    _name = "product.website.filter"
    _inherit = ["website.seo.metadata"]
    _description = "Website Product x-Filters"
    _order = "sequence, name"

    name = fields.Char(required=True, translate=True)
    filter_name = fields.Char(required=True)
    parent_id = fields.Many2one('product.website.filter', string='Parent Category', index=True)
    child_id = fields.One2many('product.website.filter', 'parent_id', string='Children Categories')
    sequence = fields.Integer(help="Gives the sequence order when displaying a list of product x-filters.")
    image = fields.Binary(attachment=True, help="This field holds the image used as image for the category, limited to 1024x1024px.")
    image_medium = fields.Binary(string='Medium-sized image', attachment=True,
                                 help="Medium-sized image of the category. It is automatically "
                                 "resized as a 128x128px image, with aspect ratio preserved. "
                                 "Use this field in form views or some kanban views.")
    image_small = fields.Binary(string='Small-sized image', attachment=True,
                                help="Small-sized image of the category. It is automatically "
                                "resized as a 64x64px image, with aspect ratio preserved. "
                                "Use this field anywhere a small image is required.")

    _sql_constraints = [('uniq_filter_name', 'unique(filter_name)', "The name of filter is be unique!")]


    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(ProductWebsiteFilters, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(ProductWebsiteFilters, self).write(vals)

    @api.constrains('parent_id')
    def check_parent_id(self):
        if not self._check_recursion():
            raise ValueError(_('Error ! You cannot create recursive filter.'))

    @api.multi
    def name_get(self):
        res = []
        for filter_name in self:
            names = [filter_name.name]
            parent_filter_name = filter_name.parent_id
            while parent_filter_name:
                names.append(parent_filter_name.name)
                parent_filter_name = parent_filter_name.parent_id
            res.append((filter_name.id, ' / '.join(reversed(names))))
        return res

class ProductTemplate(models.Model):
    _inherit = "product.template"

    website_filter_ids = fields.Many2many('product.website.filter', string='Website Product Filter',
                                        help="Header based filters to make different brands on the Shop page (online filtered by brand)")

    @api.multi
    def write(self, vals):
        if 'website_filter_ids' in vals:
            for product_template in self:
                for product in product_template.ensure_one().product_variant_ids:
                    product.write({'website_filter_ids': vals['website_filter_ids']})
        return super(ProductTemplate, self).write(vals)


class ProductProduct(models.Model):
    _inherit = "product.product"

    website_filter_ids = fields.Many2many('product.website.filter', string='Website Product Filter',
                                        help="Header based filters to make different brands on the Shop page (online filtered by brand)")
