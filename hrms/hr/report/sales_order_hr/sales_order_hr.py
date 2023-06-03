# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
import itertools
from erpnext.setup.doctype.item_group import item_group


def execute(filters=None):
	columns = get_columns()
	avs = get_avaibilities(filters)
	sos = get_sales_orders(filters)
	message = None
	chart = get_chart(filters)
	report_summary = get_summary(filters)
	data = []
	data += avs
	data += sos
	return columns, data, message, chart, report_summary

def get_columns():
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
		{'fieldname' : 'shift_type', 'label': 'Shift Type', 'fieldtype': 'Data'},
		{'fieldname' : 'activity_type', 'label': 'Activity Type', 'fieldtype': 'Data'},
		{'fieldname' : 'timesheets', 'label': 'Timesheets', 'fieldtype': 'Link', 'options': 'Timesheet'},
		{'fieldname' : 'from_time', 'label': 'From Time', 'fieldtype': 'Data'},
		{'fieldname' : 'to_time', 'label': 'To Time', 'fieldtype': 'Data'},
	]
	return columns

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
				'employee': ['!=', ''],
				},
			['name', 'employee']
			)
	employees = [av['employee'] for av in shift_avs]
	employees += [rq['employee'] for rq in shift_rqs]
	employees += [aas['employee'] for aas in shift_ass]
	employees += [ts['employee'] for ts in tss]
	employees = set(employees)
	emps = [{'name': 'Employees', 'indent': 0}]
	for emp in employees:
		emp_name = frappe.db.get_value('Employee', emp, 'employee_name')
		emps.append({'name': emp_name, 'employee': emp, 'employee_name': emp_name, 'indent': 1})
		for shift_av, shift_rq, shift_as, ts in itertools.zip_longest(shift_avs, shift_rqs, shift_ass, tss):
			shift_avn, shift_rqn, shift_asn, tsn, employee, employee_name = None, None, None, None, None, None
			if shift_av:
				if shift_av['employee'] == emp:
					shift_avn = shift_av['name']
					employee = shift_av['employee']
					employee_name = frappe.db.get_value('Employee', employee, 'employee_name')
			if shift_rq:
				if shift_rq['employee'] == emp:
					shift_rqn = shift_rq['name']
					employee = shift_rq['employee']
					employee_name = frappe.db.get_value('Employee', emp, 'employee_name')
			if shift_as:
				if shift_as['employee'] == emp:
					shift_asn = shift_as['name']
					employee = shift_as['employee']
					employee_name = frappe.db.get_value('Employee', emp, 'employee_name')
			if ts:
				if ts['employee'] == emp:
					tsn = ts['name']
					employee = ts['employee']
					employee_name = frappe.db.get_value('Employee', emp, 'employee_name')
			if (shift_avn, shift_rqn, shift_asn, tsn, employee, employee_name) == (None, None, None, None, None, None):
				continue
			else:
				emps.append({
					'employee_name': employee_name,
					'shift_avaibilities': shift_avn,
					'shift_requests': shift_rqn,
					'shift_assignments': shift_asn,
					'timesheets': tsn, 'indent': 2
					})
	return emps

def get_sales_orders(filters=None):
	res = [{'name': 'Sales Order', 'indent': 0}]
	wigp = frappe.db.get_single_value('Selling Settings', 'workforce_item_group')
	wigs = item_group.get_child_item_groups(wigp)
	sos = frappe.db.get_all(
			'Sales Order',
			{
				'delivery_date': ['between', [filters.start, filters.end]],
				'docstatus': ['<', 2],
				},
			['name', 'delivery_date', 'customer', 'shipping_address_name']
			)
	for so in sos:
		items = frappe.db.get_all('Sales Order Item', {'parent': so['name'], 'item_group': ['in', wigs]}, ['item_code', 'qty', 'uom', 'description'])
		sols = get_sales_order_links(so['name'])['sols']
		sols_qties = get_sales_order_links(so['name'])['qties']
		qty_needed = 0
		for item in items:
			qty_needed += item['qty']
		name = so['customer']
		if so['shipping_address_name']:
			name += ' ' + so['shipping_address_name']
		res.append({
			'name': name,
			'sales_order': so['name'],
			'delivery_date': so['delivery_date'],
			'qty_needed': qty_needed,
			'shift_requests': sols_qties['shift_requests'],
			'shift_assignments': sols_qties['shift_assignments'],
			'timesheets': sols_qties['timesheets'],
			'indent': 1,
			})
		for item, sol in itertools.zip_longest(items, sols):
			if item:
				r = {
						'human_needs': item['item_code'],
						'qty_needed': item['qty'],
						'uom': item['uom'],
						'description': item['description'],
						'indent': 2,
						}
				if sol:
					r.update(sol)
			elif sol:
				r = sol
			else:
				continue
			res.append(r)
	return res

def get_sales_order_links(sales_order=None):
	sols = []
	tss = []
	qties = {}
	srqs = frappe.get_all('Shift Request', {'sales_order': sales_order, 'docstatus': ['<', '2']}, ['name', 'employee', 'shift_type', 'activity_type'])
	sass = frappe.get_all('Shift Assignment', {'sales_order': sales_order, 'docstatus': ['<', '2']}, ['name', 'employee', 'shift_type', 'activity_type'])
	tls = frappe.db.get_all('Timesheet Detail', {'sales_order': sales_order, 'docstatus': ['<', '2']}, ['parent','activity_type', 'from_time', 'to_time'])
	srq_qty, sas_qty, ts_qty = 0, 0, 0
	for tl in tls:
		ts = frappe.get_all('Timesheet', {'name': tl['parent'], 'docstatus': ['<', '2']}, ['name', 'employee'])[0]
		ts.update({'from_time': tl['from_time'], 'to_time': tl['to_time'], 'activity_type': tl['activity_type']})
		tss.append(ts)
	for srq, sas, ts in itertools.zip_longest(srqs, sass, tss):
		srqn, sasn, tsn, emp, emp_name, shift_type, activity_type, from_time, to_time = None, None, None, None, None, None, None, None, None
		if srq:
			srqn = srq['name']
			emp = srq['employee']
			emp_name = frappe.db.get_value('Employee', emp, 'employee_name')
			shift_type = srq['shift_type']
			activity_type = srq['activity_type']
			from_time = frappe.db.get_value('Shift Type', shift_type, 'start_time')
			to_time = frappe.db.get_value('Shift Type', shift_type, 'end_time')
			srq_qty += 1
		if sas:
			sasn = sas['name']
			emp = sas['employee']
			emp_name = frappe.db.get_value('Employee', emp, 'employee_name')
			shift_type = sas['shift_type']
			activity_type = sas['activity_type']
			from_time = frappe.db.get_value('Shift Type', shift_type, 'start_time')
			to_time = frappe.db.get_value('Shift Type', shift_type, 'end_time')
			sas_qty += 1
		if ts:
			tsn = ts['name']
			emp = ts['employee']
			emp_name = frappe.db.get_value('Employee', emp, 'employee_name')
			from_time = ts['from_time']
			to_time = ts['to_time']
			activity_type = ts['activity_type']
			ts_qty += 1
		if (srqn, sasn, tsn) == None:
			continue
		else:
			sols.append({
				'employee': emp,
				'employee_name': emp_name,
				'timesheets': tsn,
				'shift_requests': srqn,
				'shift_assignments': sasn,
				'shift_type': shift_type,
				'activity_type': activity_type,
				'from_time': from_time,
				'to_time': to_time,
				'indent': 2,
				})
			qties.update({'shift_requests': srq_qty, 'shift_assignments': sas_qty, 'timesheets': ts_qty})
	return { 'sols': sols, 'qties': qties }

def get_summary(filters=None):
	sos = frappe.db.get_all(
			'Sales Order',
			{
				'delivery_date': ['between', [filters.start, filters.end]],
				'docstatus': ['<', 2],
				},
			['name']
			)
	lsos = len(sos)
	srqs, sass, tls = 0, 0, 0
	for so in sos:
		srqs += len(frappe.get_all('Shift Request', {'sales_order': so, 'docstatus': ['<', '2']}))
		sass += len(frappe.get_all('Shift Assignment', {'sales_order': so, 'docstatus': ['<', '2']}))
		tls += len(frappe.get_all('Timesheet Detail', {'sales_order': so, 'docstatus': ['<', '2']}))
	res = [
		{'label': 'Sales Orders', 'value': lsos, 'indicator': 'Blue'},
		{'label': 'Shift Requests', 'value': get_indicator(srqs, lsos), 'indicator': 'Blue'},
		{'label': 'Shift Assignments', 'value': get_indicator(sass, lsos), 'indicator': 'Blue'},
		{'label': 'Timesheet Log', 'value': get_indicator(tls, lsos), 'indicator': 'Blue'},
		]
	return res

def get_chart(filters=None):
	pass

def get_indicator(value, ref):
	if value >= ref:
		color = 'Green'
	elif value >= 0.75 * ref:
		color = 'Orange'
	else:
		color = 'Red'
