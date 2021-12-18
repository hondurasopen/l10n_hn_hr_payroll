# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class HrIhssSettings(models.Model):
	_name = "hr.ihss.settings"

	@api.multi
	def set_ihss(self):
		self.fee_pay_max_ihss = (self.limit_max_ihss * self.ihss_percentage /100) 
		self.fee_pay_min_ihss = (self.limit_min_ihss * self.ihss_percentage /100)
		if self.pay_periodicity == 'weekly':	
			self.ihss_fee_max = self.fee_pay_max_ihss / 4
			self.ihss_fee_min = self.fee_pay_min_ihss / 4
		elif self.pay_periodicity == 'bi-weekly':
			self.ihss_fee_max = self.fee_pay_max_ihss / 2
			self.ihss_fee_min = self.fee_pay_min_ihss / 2
		else:
			self.ihss_fee_max = self.fee_pay_max_ihss 
			self.ihss_fee_min = self.fee_pay_min_ihss 
		self.write({'state': 'validated'})


	@api.multi
	def set_to_draft(self):
		self.write({'state': 'draft'})

	code_ihss = fields.Char("Codigo", required=True)
	name = fields.Char("Nombre")
	ihss_percentage = fields.Float("Porcentaje",  digits=(2, 4))
	
	fee_pay_max_ihss = fields.Float("Valor Max a Pagar")
	fee_pay_min_ihss = fields.Float("Valor Min a Pagar")
	limit_max_ihss = fields.Float("Techo Maximo")
	limit_min_ihss = fields.Float("Techo Minimo")

	ihss_fee_max = fields.Float("Cuota IHSS Max")
	ihss_fee_min = fields.Float("Cuota IHSS Min")
	
	pay_periodicity = fields.Selection([('weekly', 'Semanal'), ('bi-weekly', 'Quincenal'), ('monthly', 'Mensual')], "Periodicidad Pago", default='bi-weekly')
	state = fields.Selection([('draft','Borrador'), ('validated','Validado')], "Estado", default='draft')
	#
	ihss_apply = fields.Selection([('nfd', 'No Definido'), ('porcentaje', 'Porcentaje'), ('manual', 'Manual')], "Aplicar IHSS", default='nfd')
