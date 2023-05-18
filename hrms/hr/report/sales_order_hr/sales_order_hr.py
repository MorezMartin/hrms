# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
import itertools


def execute(filters=None):
	avs = get_avaibilities()
	columns, data = [], []
	return columns, data

def get_avaibilities(filters=None):
	shift_avs = frappe.db.get_all(
			'Shift Avaibility',
			{
				'docstatus': ['=', 1],
				'from_date': ['<=', filters['end']],
				'to_date': ['>=', filters['start']],
				},
			['name', 'employee'],
			)
	shift_rqs = frappe.db.get_all(
			'Shift Request',
			{
				'from_date': ['<=', filters['end']],
				'to_date': ['>=', filters['start']],
				},
			['name', 'employee']
			)
	shift_ass = frappe.db.get_all(
			'Shift Assignment',
			{
				'start': ['<=', filters['end']],
				'end': ['>=', filters['start']],
				},
			['name', 'employee']
			)
	tss = frappe.db.get_all(
			'Timesheet',
			{
				'start_date': ['<=', filters['end']],
				'end_date': ['>=', filters['start']],
				},
			['name', 'employee']
			)
	employees = [av['employee'] for av in shift_avs]
	employees = set(employees)
	emps = []
	for emp in employees:
		emps.append({'name': frappe.db.get_value('Employee', emp, 'employee_name'), 'employee': emp, 'indent': 1})
		for shift_av, shift_rq, shift_as in itertools.zip_longest(shift_avs, shift_rqs, shift_ass):
			emps.append({'employee': shift_av['employee'], 'shift_avaibilities': shift_av['name'], 'shift_requests': shift_rq['name'], 'shift_assignments': shift_as['name'] , 'indent': 2})
	return emps
