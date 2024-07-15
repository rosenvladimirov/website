# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class WebsiteSaleCategory(models.TransientModel):
    _name = 'product.public.category.sort'
    _description = 'Auto sort by e-comerce category'

    sort_by_type = fields.Selection([('pub-category', 'E-Commerce category'), ('int-category', 'Internal category', 'alfa-beta', 'Sort by alphabetical order')])

    @api.multi
    def _process(self):
        if self.sort_by_type == 'pub-category':
            sequence = 0
            for category_id in self.env['product.public.category'].search([]):
                product_template = self.env['product.template'].search(["&", ('id', 'in', self._context.get('active_ids')), ('public_categ_ids', 'in', [category_id.id])])
                for product in product_template:
                    product.write({'sequence': sequence})
                    sequence += 1
        elif self.sort_by_type == 'int-category':
            sequence = 0
            for category_id in self.env['product.category'].search([]):
                product_template = self.env['product.template'].search(["&", ('id', 'in', self._context.get('active_ids')), ('categ_id', 'in', [category_id.id])])
                for product in product_template:
                    product.write({'sequence': sequence})
                    sequence += 1
        elif self.sort_by_type == 'alfa-beta':
            sequence = 0
            product_template = self.env['product.template'].search([('id', 'in', self._context.get('active_ids'))])
            for product in product_template:
                product.write({'sequence': sequence})
                sequence += 1
