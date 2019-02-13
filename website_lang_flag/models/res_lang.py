# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _

class Lang(models.Model):
    _inherit = "res.lang"

    country_id = fields.Many2one('res.country', string='National Language of', ondelete='restrict')
    image = fields.Binary(related="country_id.image")
