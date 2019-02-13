# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class WebsiteSaleCategory(models.TransientModel):
    _name = 'product.public.category.sort'
    _description = 'Auto sort by e-comerce category'

    sort_by_type = fields.Selection(selection=[('pub-category', 'E-Commerce category'),
                                               ('int-category', 'Internal category'),
                                               ('alfa-beta', 'Sort by alphabetical order')],
                                    string="Select type sort", default='pub-category')

    @api.multi
    def sort_process(self):
        def child(category, child_ids):
            for child in category.child_id.sorted(key=lambda r: sequence):
                if child.child_id:
                    child_ids = child(child, child_ids)
                else:
                    child_ids.append(child.id)
            return child_ids

        product_template_obj = self.env['product.template']
        if self.sort_by_type == 'pub-category':
            sequence = 0
            categs = request.env['product.public.category'].search([('parent_id', '=', False)], order="sequence asc")
            for caterory in categs:
                child_ids = []
                child_ids = child(child, child_ids)
                product_template = product_template_obj.search(["&", ('id', 'in', self._context.get('active_ids')), ('public_categ_ids', 'in', child_ids)], order="sequence desc")
                for product in product_template:
                    _logger.info('Sort %s:%s:%s:%s' % (category_id.name, product_template, product, sequence))
                    product.website_sequence = sequence
                    sequence += 1

#            for category_id in self.env['product.public.category'].search(["|", "&", ('parent_id', "=", False), ('child_id', '=', False), "&", ('parent_id', "!=", False), ('child_id', '=', False)], order="sequence asc"):
#                product_template = product_template_obj.search(["&", ('id', 'in', self._context.get('active_ids')), ('public_categ_ids', 'in', [category_id.id])], order="sequence desc")
#                for product in product_template:
#                    _logger.info('Sort %s:%s:%s:%s' % (category_id.name, product_template, product, sequence))
#                    product.website_sequence = sequence
#                    sequence += 1

        elif self.sort_by_type == 'int-category':
            sequence = 0
            for category_id in self.env['product.category'].search(["|", "&", ('parent_id', "=", False), ('child_id', '=', False), "&", ('parent_id', "!=", False), ('child_id', '=', False)], order="sequence asc"):
                product_template = self.env['product.template'].search(["&", ('id', 'in', self._context.get('active_ids')), ('categ_id', 'in', [category_id.id])])
                for product in product_template:
                    product.website_sequence = sequence
                    sequence += 1
        elif self.sort_by_type == 'alfa-beta':
            sequence = 0
            product_template = self.env['product.template'].search([('id', 'in', self._context.get('active_ids'))], order="name asc")
            for product in product_template:
                product.sequence  = sequence
                sequence += 1
