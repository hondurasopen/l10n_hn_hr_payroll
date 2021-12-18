# -*- coding: utf-8 -*-
from odoo import models, fields, api 


class HrWageHistorical(models.Model):
	_name = "hr.gross.wage.historical"

	contract_id = fields.Many2one("hr.contract", "Contrato")
	gross_salary = fields.Float("Salario Bruto")
	payment_date = fields.Date("Fecha")
	payroll_id = fields.Many2one("hr.wage.paying", "Nómina")
	month = fields.Char("Mes")

