# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date
from odoo.addons import decimal_precision as dp


class HrContract(models.Model):
    _inherit = "hr.contract"

    # COLUMNS
    #historical_ids = fields.One2many("hr.historical.contract", "contract_id", "Historial")
    #allowences_ids = fields.One2many("hr.contract.deduction.allowance", "contract_id", "Otros Beneficios y deducciones")
    #historical_gross_wage_ids = fields.One2many("hr.gross.wage.historical", "contract_id", "Salarios Brutos")

    #Settings IHSS
    ihss_fee = fields.Float("Cuota de seguro")
    #accumulated_amount_ihss = fields.Float("Monto acumulado Ihss")
    ihss_id = fields.Many2one("hr.ihss.settings", "Deducción IHSS")
    ihss_manual = fields.Boolean("IHSS manual")
    amount_ihss_manual = fields.Float("Monto IHSS Manual")
    
    #RAP Settings
    rap_manual = fields.Boolean("RAP Manual")
    amount_rap_manual = fields.Float("Monto RAP Manual")
    rap_fee = fields.Float("Cuota de RAP")
    rap_id =fields.Many2one("hr.rap", "Deducción RAP")
    #ISR Settings
    isr_fee = fields.Float("Cuota ISR")
    isr_id = fields.Many2one("hr.isr", "Deducción ISR")
    isr_ids = fields.One2many("hr.isr.employee.detail", "contract_id", "ISR")
    isr_residual = fields.Float("ISR por pagar")
    amount_membership = fields.Float("Monto de Colegiaturas")
    other_expenses_isr = fields.Float("Otros Gastos")


    @api.onchange("ihss_id")
    def onchange_ihss_id(self):
        if self.ihss_id:
            if self.wage >= self.ihss_id.limit_max_ihss:
                self.ihss_fee = self.ihss_id.ihss_fee_max
            else:
                self.ihss_fee = self.ihss_id.ihss_fee_min


    @api.onchange("rap_id")
    def onchange_rap_id(self):
        if self.rap_id:
            if self.wage > self.rap_id.techo_rap_max:
                self.rap_fee = self.rap_id.rap_fee_max
            elif self.wage > self.rap_id.techo_rap_min:
                self.rap_fee = (self.wage - self.rap_id.techo_rap_min) * (self.rap_id.rap_percentage / 100 )
            else:
                self.rap_fee = 0

