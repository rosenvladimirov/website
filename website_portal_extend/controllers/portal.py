# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import math

from werkzeug import urls

from odoo import fields as odoo_fields, tools, _
from odoo.osv import expression
from odoo.exceptions import ValidationError
from odoo.http import Controller, request, route

from odoo.addons.portal.controllers.portal import CustomerPortal

import logging
_logger = logging.getLogger(__name__)


class CustomerPortal(CustomerPortal):
    MANDATORY_BILLING_FIELDS = ["name", "mobile", "email", "street", "city_id", "country_id"]
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name", "phone"]

    def _prepare_portal_layout_values(self):
        res = super()._prepare_portal_layout_values()
        res.update({
            'partner': request.env.user.partner_id,
            })
        return res

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, partner=None, **post):
        values = self._prepare_portal_layout_values()

        if partner:
            partner = request.env['res.partner'].browse([int(partner)])
        else:
            partner = request.env.user.partner_id
            #partner = request.env['res.partner'].browse([request.env.user.partner_id.id])
        values.update({
            'error': {},
            'error_message': [],
        })
        _logger.info("Partner %s" % partner)
        if post:
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                values.update({'zip': values.pop('zipcode', '')})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        cites = request.env['res.city'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'cites': cites,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

#portal._prepare_portal_layout_values = CustomerPortal._prepare_portal_layout_values
#portal.account = CustomerPortal.account
#portal = CustomerPortal
