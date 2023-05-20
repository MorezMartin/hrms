# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
import itertools


def execute(filters=None):
	avs = get_avaibilities(filters)
	sos = get_sales_orders(filters)
	data = []
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
		{'fieldname' : 'shift_assignments', 'label': 'Shift Assignments', 'fieldtype': 'Link', 'options': 'Shift Assignment'},
		{'fieldname' : 'timesheets', 'label': 'Timesheets', 'fieldtype': 'Link', 'options': 'Timesheet'},
	]
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
	emps = [{'name': 'Employees', 'indent': 0}]
	for emp in employees:
		emps.append({'name': frappe.db.get_value('Employee', emp, 'employee_name'), 'employee': emp, 'indent': 1})
		for shift_av, shift_rq, shift_as, ts in itertools.zip_longest(shift_avs, shift_rqs, shift_ass, tss):
			shift_ave, shift_avn, shift_rqn, shift_asn, tsn = None, None, None, None, None
			if shift_av:
				if shift_av['employee'] == emp:
					shift_ave = shift_av['employee']
					shift_avn = shift_av['name']
			if shift_rq:
				if shift_rq['employee'] == emp:
					shift_rqn = shift_rq['name']
			if shift_as:
				if shift_as['employee'] == emp:
					shift_asn = shift_as['name']
			if ts:
				if ts['employee'] == emp:
					tsn = ts['name']
			emps.append({'employee': shift_ave or None, 'shift_avaibilities': shift_avn or None, 'shift_requests': shift_rqn or None, 'shift_assignments': shift_asn or None, 'timesheets': tsn, 'indent': 2})
	return emps

def get_sales_orders(filters=None):
	res = [{'name': 'Sales Order', 'indent': 0}]
	sos = frappe.db.get_all(
			'Sales Order',
			{
				'delivery_date': ['between', [filters.start, filters.end]],
				'docstatus': ['<', 2],
				},
			['name', 'delivery_date', 'customer', 'shipping_address_name']
			)
	for so in sos:
		items = frappe.db.get_all('Sales Order Item', {'parent': so['name']}, ['item_code', 'qty', 'uom', 'description'])
		human_needs = 0
		for item in items:
			qty_needed += item['qty']
		if so['shipping_address_name']:
			name = so['customer'] + so['shipping_address_name']
		else:
			name = so['customer']
		res.append({'name': so['customer'] + ' ' + so['shipping_address_name'], 'sales_order': so['name'], 'delivery_date': so['delivery_date'], 'qty_needed': qty_needed, 'indent': 1})
		for item in items:
			res.append({'human_needs': item['item_code'], 'qty_needed': item['qty'], 'uom': item['uom'], 'description': item['description'], 'indent': 2 }),
	return res

def get_sales_order_links(sales_order=None):
	sols = []
	srqs = frappe.get_all('Shift Request', {'sales_order': sales_order, 'docstatus' ['<', '2']})
	sass = frappe.get_all('Shift Assignment', {'sales_order': sales_order, 'docstatus' ['<', '2']})
	tss = frappe.get_all('Timesheet', {'sales_order': sales_order, 'docstatus' ['<', '2']})
	for srq, sas, ts in itertools.zip_longest(srqs, sass, tss):
		srqn, sasn, tsn = None, None, None
		if srq:
			srqn = srq['name']
		if sas:
			sasn = sa['name']
		if ts:
			tsn = ts['name']
		sols.append({'timesheets': tsn or None, 'shift_requests': srqn or None, 'shift_assignments': sasn or None})

