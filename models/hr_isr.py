# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError

class HrISRSettings(models.Model):
	_name = "hr.isr"


	def set_isr(self):
		self.write({'state': 'validated'})


	def set_to_draft(self):
		self.write({'state': 'draft'})

	name = fields.Char("Descripcion", required=True)

	pay_periodicity = fields.Selection([('weekly', 'Semanal'), ('bi-weekly', 'Quincenal'), ('monthly', 'Mensual')], "Periodicidad Pago", default='bi-weekly')
	state = fields.Selection([('draft','Borrador'), ('validated','Validado')], "Estado", default='draft')

	exempt_salary = fields.Float("Salario Exento")

	medical_expense = fields.Float("Gastos Médicos")
	amount_rap = fields.Float("RAP")
	amount_ivm = fields.Float("Aportaciones Vejez y Muerte")

	isr_range_ids = fields.One2many("hr.isr.ranges", "parent_id", "Rangos")


	def unlink(self):
		for isr in self:
			if isr.state == 'validated':
				raise UserError(_('El registro se encuentra en estado validado, no se puede eliminar'))
		return super(HrISRSettings, self).unlink()


class HrISRSettings(models.Model):
	_name = "hr.isr.ranges"

	parent_id = fields.Many2one("hr.isr", "ISR")
	amount_from = fields.Float("Desde", required=True)
	amount_to = fields.Float("Hasta", required=True)
	rate = fields.Float("Tasa %", required=True)