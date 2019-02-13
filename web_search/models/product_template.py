# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _

import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    description_sale = fields.Text(string='Sale Description', index=True)
    description = fields.Text(string='Description', index=True)
    #rang_id = fields.Many2many(string="Rang Key", comodel_name="product.template.rang", relation="rang_product_template_rel",)

    def __init__(self, pool, cr):
        cr.execute("SELECT set_limit(0.2);")
        return super(ProductTemplate, self).__init__(pool, cr)

class ProductTemplateRang(models.Model):
    _name = "product.template.rang"
    _description = "Product template rang"
    _order = "rang desc"

    rang = fields.Integer("Product Template Rang", index=True)
    key = fields.Char("Key", index=True)
    #product_id = fields.Many2many(string="Product Template", comodel_name="product.template")

    @api.multi
    def write(self, vals):
        res = super(ProductTemplateRang, self).write(vals)
        if vals.get('key'):
            vals['rang'] = res.rang+1
        return res
