# -*- coding: utf-8 -*-
from odoo import http, SUPERUSER_ID
from odoo import api, fields, models, _
from odoo.http import request


class website(models.Model):
	_inherit='website'

	def get_product_attachements(self, product=None, datasheet=False,context=None):
		data=[]
		if product and not datasheet:
			domain = [('res_model','=','product.template'),('res_id','=',product.id)]
			attachement_ids = self.env['ir.attachment'].sudo().search(domain)
			if attachement_ids:
				return attachement_ids
		if product and datasheet:
			if product.product_variant_count > 0:
				domain = [
					'&', ('res_model', '=', 'product.product'), ('res_id', 'in', product.product_variant_ids.ids)]
			else:
				domain = [
					'&', ('res_model', '=', 'product.product'), ('res_id', '=', product.product_variant_id.id)]
			attachement_ids = self.env['product.manufacturer.datasheets'].sudo().search(domain)
			if attachement_ids:
				return attachement_ids
		return data
