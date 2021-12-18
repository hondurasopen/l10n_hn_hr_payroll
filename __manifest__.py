# -*- coding: utf-8 -*-
{
    'name': "Honduras Payroll",
    'category': 'HR',
    "author": "César Alejandro Rodriguez, Grupo SIE",
    'version': '2.0',
    'depends': ['hr_payroll'],
    'data': [
        # Views
        #'security/ir.model.access.csv',
        "views/allowance_deduction_view.xml",
        "views/concept_deduction_allowances.xml",
        'data/sequence.xml',
        'data/data.xml',
        'views/hr_contract.xml',
        'views/hr_employee_view.xml',
        "views/ihss_settings.xml",
        "views/hr_rap.xml",
        "views/hr_salary_rule.xml",
        "views/hr_isr.xml",
        "views/hr_employee_isr.xml",
    ],

    'installable': True,
}
