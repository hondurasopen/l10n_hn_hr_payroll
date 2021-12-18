# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class employeeInh(models.Model):
    _inherit = 'hr.employee'

    code_employee = fields.Char("Codigo de empleado")
    with_code = fields.Boolean(string="With Code")

    _sql_constraints = [('code_employee', 'unique(code_employee)', 'El código de empleado debe de ser único!')]

    @api.depends('birthday')
    def calculate_age(self):
        for employee in self:
            if employee.birthday:
                actual_year = datetime.now().year
                date = datetime.strptime(employee.birthday, '%Y-%m-%d')
                employee.age = actual_year - date.year


    def action_button_confirm(self):
        number = self.env['ir.sequence'].next_by_code('seq.code.employee')
        self.with_code = True
        self.code_employee = number

