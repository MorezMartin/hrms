# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
import itertools


def execute(filters=None):
	columns = [
		{'fieldname' : 'name', 'label': 'Name', 'fieldtype': 'Data'},
		{'fieldname' : 'sales_order', 'label': 'Sales Order', 'fieldtype': 'Link', 'options': 'Sales Order'},
		{'fieldname' : 'delivery_date', 'label': 'Delivery Date', 'fieldtype': 'Datetime'},
		{'fieldname' : 'human_needs', 'label': 'Human Needs', 'fieldtype': 'Data'},
		{'fieldname' : 'qty_needed', 'label': 'Quantity Needed', 'fieldtype': 'Data'},
		{'fieldname' : 'uom', 'label': 'UoM', 'fieldtype': 'Data'},
		{'fieldname' : 'description', 'label': 'Description', 'fieldtype': 'Text Editor'},
		{'fieldname' : 'employee', 'label': 'Employee', 'fieldtype': 'Link', 'options': 'Employee'},
		{'fieldname' : 'shift_avaibilities', 'label': 'Shift Avaibilities', 'fieldtype': 'Link', 'options': 'Shift Avaibility'},
		{'fieldname' : 'shift_requests', 'label': 'Shift Requests', 'fieldtype': 'Link', 'options': 'Shift Request'},
		{'fieldname' : 'shift_assignments', 'label': 'Shift Assignments', 'fieldtype': 'Data'},
		{'fieldname' : 'timesheets', 'label': 'Timesheets', 'fieldtype': 'Data'},
	]
	avs = get_avaibilities(filters)
	sos = get_sales_orders(filters)
	columns, data = [], []
	data += avs
	data += sos
	return columns, data

def get_avaibilities(filters=None):
	shift_avs = frappe.db.get_all(
			'Shift Avaibility',
			{
				'docstatus': ['=', 1],
				'from_date': ['<=', filters.end],
				'to_date': ['>=', filters.start],
				},
			['name', 'employee'],
			)
	shift_rqs = frappe.db.get_all(
			'Shift Request',
			{
				'from_date': ['<=', filters.end],
				'to_date': ['>=', filters.start],
				},
			['name', 'employee']
			)
	shift_ass = frappe.db.get_all(
			'Shift Assignment',
			{
				'start_date': ['<=', filters.end],
				'end_date': ['>=', filters.start],
				},
			['name', 'employee']
			)
	tss = frappe.db.get_all(
			'Timesheet',
			{
				'start_date': ['<=', filters.end],
				'end_date': ['>=', filters.start],
				},
			['name', 'employee']
			)
	employees = [av['employee'] for av in shift_avs]
	employees = set(employees)
	emps = []
	for emp in employees:
		emps.append({'name': frappe.db.get_value('Employee', emp, 'employee_name'), 'employee': emp, 'indent': 1})
		for shift_av, shift_rq, shift_as, ts in itertools.zip_longest(shift_avs, shift_rqs, shift_ass, tss):
			if shift_av:
				shift_ave = shift_av['employee']
				shift_avn = shift_av['name']
			if shift_rq:
				shift_rqn = shift_rq['name']
			if shift_as:
				shift_asn = shift_as['name']
			if ts:
				tsn = ts['name']
			emps.append({'employee': shift_ave, 'shift_avaibilities': shift_avn, 'shift_requests': shift_rqn, 'shift_assignments': shift_asn, 'timesheets': tsn, 'indent': 2})
	return emps

def get_sales_orders(filters=None):
	res = []
	sos = frappe.db.get_all(
			'Sales Order',
			{
				'delivery_date': ['between', [filters.start, filters.end]],
				'docstatus': ['<', 2],
				},
			)
	for so in sos:
		items = frappe.db.get_all('Sales Order Item', {'parent': so['name']}, ['item_code', 'qty', 'uom', 'description'])
		res.append({'name': 'Sales Order', 'sales_order': so['name'], 'delivery_date': so['delivery_date'], 'human_needs': 3})
		for item in items:
			res.append({'human_needs': item['item_code'], 'qty_needed': item['qty'], 'uom': item['uom'], 'description': item['description'], 'indent': 1 }),
	return res
