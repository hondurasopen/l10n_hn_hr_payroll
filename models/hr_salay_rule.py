# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class HrSalaryRule(models.Model):
	_inherit = "hr.salary.rule"

	generate_historical = fields.Boolean("Generar Histórico")
	generate_accounting = fields.Boolean("Generar Contabilidad")
