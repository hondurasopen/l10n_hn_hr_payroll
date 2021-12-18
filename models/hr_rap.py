# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class HrRap(models.Model):
	_name = "hr.rap"


	@api.multi
	def set_rap(self):
		self.fee_pay_max_rap = (self.techo_rap_max - self.techo_rap_min) * (self.rap_percentage / 100)
		if self.pay_periodicity == 'weekly':	
			self.rap_fee_max = self.fee_pay_max_rap / 4
		elif self.pay_periodicity == 'bi-weekly':
			self.rap_fee_max = self.fee_pay_max_rap / 2
		else:
			self.rap_fee_max = self.fee_pay_max_rap  
		self.write({'state': 'validated'})

	@api.multi
	def set_to_draft(self):
		self.write({'state': 'draft'})


	name = fields.Char("Descripcion", required=True)

	rap_percentage = fields.Float("Porcentaje Aplicar (%)", digits=(2, 4), required=True)
	techo_rap_max = fields.Float("Techo RAP Mäximo", digits=(2, 4), required=True)
	
	techo_rap_min = fields.Float("Techo RAP Mínimo", digits=(2, 4))

	fee_pay_max_rap = fields.Float("Valor Max a Pagar")

	pay_periodicity = fields.Selection([('weekly', 'Semanal'), ('bi-weekly', 'Quincenal'), ('monthly', 'Mensual')], "Periodicidad Pago", default='bi-weekly')
	state = fields.Selection([('draft','Borrador'), ('validated','Validado')], "Estado", default='draft')

	rap_fee_max = fields.Float("Cuota RAP") 