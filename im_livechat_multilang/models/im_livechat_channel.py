# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, modules, tools


class ImLivechatChannel(models.Model):
    _inherit = 'im_livechat.channel'

    button_text = fields.Char(translate=True)
    default_message = fields.Char(translate=True)
    input_placeholder = fields.Char(translate=True)
