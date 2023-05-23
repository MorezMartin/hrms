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
		{'fieldname' : 'employee_name', 'label': 'Employee Name', 'fieldtype': 'Data'},
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
				'docstatus': ['<', 2],
				'from_date': ['<=', filters.end],
				'to_date': ['>=', filters.start],
				},
			['name', 'employee']
			)
	shift_ass = frappe.db.get_all(
			'Shift Assignment',
			{
				'docstatus': ['<', 2],
				'start_date': ['<=', filters.end],
				'end_date': ['>=', filters.start],
				},
			['name', 'employee']
			)
	tss = frappe.db.get_all(
			'Timesheet',
			{
				'docstatus': ['<', 2],
				'start_date': ['<=', filters.end],
				'end_date': ['>=', filters.start],
				},
			['name', 'employee']
			)
	employees = [av['employee'] for av in shift_avs]
	employees = set(employees)
	emps = [{'name': 'Employees', 'indent': 0}]
	for emp in employees:
		emp_name = frappe.db.get_value('Employee', emp, 'employee_name')
		emps.append({'name': emp_name, 'employee': emp, 'indent': 1})
		for shift_av, shift_rq, shift_as, ts in itertools.zip_longest(shift_avs, shift_rqs, shift_ass, tss):
			shift_avn, shift_rqn, shift_asn, tsn, employee, employee_name = None, None, None, None, None, None
			if shift_av:
				if shift_av['employee'] == emp:
					shift_avn = shift_av['name']
					employee = emp
					employee_name = frappe.db.get_value('Employee', emp, 'employee_name')
			if shift_rq:
				if shift_rq['employee'] == emp:
					shift_rqn = shift_rq['name']
					employee = emp
					employee_name = frappe.db.get_value('Employee', emp, 'employee_name')
			if shift_as:
				if shift_as['employee'] == emp:
					shift_asn = shift_as['name']
					employee = emp
					employee_name = frappe.db.get_value('Employee', emp, 'employee_name')
			if ts:
				if ts['employee'] == emp:
					tsn = ts['name']
					employee = emp
			if (shift_avn, shift_rqn, shift_asn, tsn, employee, employee_name) == (None, None, None, None, None, None):
				continue
			else:
				emps.append({
					'employee': employee,
					'employee_name': employee_name,
					'shift_avaibilities': shift_avn,
					'shift_requests': shift_rqn,
					'shift_assignments': shift_asn,
					'timesheets': tsn, 'indent': 2
					})
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
		qty_needed = 0
		for item in items:
			qty_needed += item['qty']
		if so['shipping_address_name']:
			name = so['customer'] + so['shipping_address_name']
		else:
			name = so['customer']
		res.append({
			'name': name,
			'sales_order': so['name'],
			'delivery_date': so['delivery_date'],
			'qty_needed': qty_needed,
			'indent': 1
			})
		for item in items:
			res.append({
				'human_needs': item['item_code'],
				'qty_needed': item['qty'],
				'uom': item['uom'],
				'description': item['description'],
				'indent': 2,
				})
		sols = get_sales_order_links(so['name'])
		res += sols
	return res

def get_sales_order_links(sales_order=None):
	sols = []
	srqs = frappe.get_all('Shift Request', {'sales_order': sales_order, 'docstatus': ['<', '2']}, ['name', 'employee'])
	sass = frappe.get_all('Shift Assignment', {'sales_order': sales_order, 'docstatus': ['<', '2']}, ['name', 'employee'])
	tss = frappe.get_all('Timesheet', {'sales_order': sales_order, 'docstatus': ['<', '2']}, ['name', 'employee'])
	for srq, sas, ts in itertools.zip_longest(srqs, sass, tss):
		srqn, sasn, tsn, emp, emp_name = None, None, None, None, None
		if srq:
			srqn = srq['name']
			emp = srq['employee']
			emp_name = frappe.db.get_value('Employee', emp, 'employee_name')
		if sas:
			sasn = sas['name']
			emp = sas['employee']
			emp_name = frappe.db.get_value('Employee', emp, 'employee_name')
		if ts:
			tsn = ts['name']
			emp = ts['employee']
			emp_name = frappe.db.get_value('Employee', emp, 'employee_name')
		sols.append({
			'employee': emp,
			'employee_name': emp_name,
			'timesheets': tsn,
			'shift_requests': srqn,
			'shift_assignments': sasn,
			'indent': 2,
			})
	return sols
