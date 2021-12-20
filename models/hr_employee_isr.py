# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, UserError

class HrIsrEmployee(models.Model):
    _name = "hr.isr.employee"

    department_id = fields.Many2one("hr.department", "Departamento")
    employee_ids = fields.One2many("hr.isr.employee.detail", "parent_id", "Detail")
    state = fields.Selection([('draft','Borrador'), ('validated','Validado')], "Estado", default='draft')
    isr_id = fields.Many2one("hr.isr", "ISR", required=True)
    name = fields.Char("Año", required=True)
    exempt_salary = fields.Float("Salario Exento", related="isr_id.exempt_salary")
    pay_periodicity = fields.Selection([('bi-weekly', 'Quincenal'), ('monthly', 'Mensual')], "Periodicidad Pago", default='bi-weekly')
    start_date = fields.Date("Fecha Inicio")
    end_date = fields.Date("Fecha Final")
    pay_number = fields.Integer("# Pagos", default=24)

    def set_isr_contract(self):
        if self.employee_ids:
            for contract in self.employee_ids:
                self.calculate_isr()
                if contract.total_tax > 0:
                    contract.contract_id.isr_fee = contract.isr_fee
                    contract.contract_id.isr_id = self.isr_id.id
                    contract.contract_id.amount_membership = contract.amount_membership
                    contract.contract_id.isr_residual = contract.total_tax
                    contract.contract_id.other_expenses_isr = contract.other_expenses
                else:
                    contract.is_ok = False

            self.write({'state': 'validated'})


    def return_to_draft(self):
        self.write({'state': 'draft'})        


    def calculate_isr(self):
        if self.employee_ids:
            if self.pay_number > 0:
                for employee in self.employee_ids:
                    retention_total = 0
                    for l in self.isr_id.isr_range_ids:
                        if l.rate > 0:
                            if employee.total_base > l.amount_from:
                                if employee.total_base  < l.amount_to:
                                    retention_total += (( employee.total_base  - l.amount_from) * (l.rate / 100))
                                else:
                                    if l.amount_to > 0:
                                        retention_total += ((l.amount_to - l.amount_from) * (l.rate / 100) )
                                    else:
                                        retention_total += ((employee.total_base  - l.amount_from) * (l.rate / 100))
                    employee.total_tax = retention_total
                    employee.isr_fee = retention_total / self.pay_number
                    if employee.total_tax > 0:
                        employee.is_ok = True
                    else:
                        employee.is_ok = False
            else:
                raise ValidationError(_('El número de pagos debe de ser mayor que cero'))


    def get_employees(self):
        self.employee_ids.unlink()
        if not self.start_date or not self.end_date:
            raise ValidationError(_('Los campos fechas de inicio y fecha final no deben ser vacios'))
        date_1 = datetime.strptime(str(self.start_date), '%Y-%m-%d')
        date_2 = datetime.strptime(str(self.end_date), '%Y-%m-%d')
        rest = date_2.month - date_1.month + 1
        if self.department_id:
            contract_obj = self.env["hr.contract"].search([('state', '=', 'open'), ('wage', '>', self.isr_id.exempt_salary), ('department_id', '=', self.department_id)])
            for l in contract_obj:
                line_obj = self.env["hr.isr.employee.detail"]
                vals = {
    				'employee_id': l.employee_id.id,
                    'contract_id': l.id,
    				'parent_id': self.id,
    				'medical_expense': self.isr_id.medical_expense,
    				'total_incomes': l.wage * rest,
    				'amount_rap': self.isr_id.amount_rap,
    				'amount_ivm': self.isr_id.amount_ivm,
                }
                line_obj.create(vals)
        else:
            contract_obj = self.env["hr.contract"].search([('state', '=', 'open'), ('wage', '>', self.isr_id.exempt_salary)])
            for l in contract_obj:
                line_obj = self.env["hr.isr.employee.detail"]
                vals = {
                    'employee_id': l.employee_id.id,
                    'contract_id': l.id,
                    'parent_id': self.id,
                    'medical_expense': self.isr_id.medical_expense,
                    'total_incomes': l.wage * rest,
                    'amount_rap': self.isr_id.amount_rap,
                    'amount_ivm': self.isr_id.amount_ivm,
                }
                line_obj.create(vals)


class HrIsrEmployeeDetail(models.Model):
    _name = "hr.isr.employee.detail"


    @api.depends("total_incomes", "amount_membership", "medical_expense", "amount_rap", "amount_ivm", "other_expenses")
    def _compute_total_base(self):
    	self.total_base = self.total_incomes - self.amount_membership - self.medical_expense - self.amount_rap - self.amount_ivm - self.other_expenses

    parent_id = fields.Many2one("hr.isr.employee", "ISR Año")
    employee_id = fields.Many2one("hr.employee", "Empleado", required=True)
    contract_id = fields.Many2one("hr.contract", "Contrato")
    total_incomes = fields.Float("Total Ingresos")
    amount_membership = fields.Float("Colegiaturas")
    medical_expense = fields.Float("Gastos Médicos")
    amount_rap = fields.Float("RAP")
    amount_ivm = fields.Float("Invalidez Vejez y Muerte")
    other_expenses = fields.Float("Otros Gastos")

    total_base = fields.Float("Tota Base Impositiva", compute='_compute_total_base')
    total_tax = fields.Float("Total Impuesto")
    isr_fee = fields.Float("Deducción")
    actived = fields.Boolean("ISR Activo", default=True)
    start_date = fields.Date("Fecha Inicial", related="parent_id.start_date")
    end_date = fields.Date("Fecha Inicial", related="parent_id.end_date")
    pay_periodicity = fields.Selection([('bi-weekly', 'Quincenal'), ('monthly', 'Mensual')], "Periodicidad Pago",  default='bi-weekly', 
        related="parent_id.pay_periodicity")
    is_ok = fields.Boolean("A procesar/Procesado")
    pay_number = fields.Integer("# Pagos", related="parent_id.pay_number")
