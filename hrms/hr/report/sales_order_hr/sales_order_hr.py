# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import get_datetime, datetime
import itertools
from erpnext.setup.doctype.item_group import item_group


def execute(filters=None):
	columns = get_columns()
	avs = get_avaibilities(filters)
	sos = get_sales_orders(filters)
	message = None
	chart = get_chart(sos['sos'], sos['needed_qties'], sos['sols_qties_list'], filters)
	report_summary = get_summary(filters)
	data = []
	data += avs
	data += sos['data']
	return columns, data, message, chart, report_summary

def get_columns():
	columns = [
		{'fieldname' : 'name', 'label': _('Name'), 'fieldtype': 'Data', 'width': 200},
		{'fieldname' : 'sales_order', 'label': _('Sales Order'), 'fieldtype': 'Link', 'options': 'Sales Order', 'width': 200},
		{'fieldname' : 'delivery_date', 'label': _('Delivery Date'), 'fieldtype': 'Datetime', 'width': 200},
		{'fieldname' : 'human_needs', 'label': _('Human Needs'), 'fieldtype': 'Data', 'width': 160},
		{'fieldname' : 'qty_needed', 'label': _('Quantity Needed'), 'fieldtype': 'Data', 'width': 40},
		{'fieldname' : 'uom', 'label': _('UoM'), 'fieldtype': 'Data', 'width': 60},
		{'fieldname' : 'description', 'label': _('Description'), 'fieldtype': 'Text Editor', 'width': 300},
		{'fieldname' : 'employee', 'label': _('Employee'), 'fieldtype': 'Link', 'options': 'Employee', 'width': 80},
		{'fieldname' : 'employee_name', 'label': _('Employee Name'), 'fieldtype': 'Data', 'width': 160},
		{'fieldname' : 'shift_avaibilities', 'label': _('Shift Avaibilities'), 'fieldtype': 'Link', 'options': 'Shift Avaibility', 'width': 80},
		{'fieldname' : 'shift_requests', 'label': _('Shift Requests'), 'fieldtype': 'Link', 'options': 'Shift Request', 'width': 80},
		{'fieldname' : 'shift_assignments', 'label': _('Shift Assignments'), 'fieldtype': 'Link', 'options': 'Shift Assignment', 'width': 80},
		{'fieldname' : 'shift_type', 'label': _('Shift Type'), 'fieldtype': 'Data', 'width': 80},
		{'fieldname' : 'activity_type', 'label': _('Activity Type'), 'fieldtype': 'Data', 'width': 120},
		{'fieldname' : 'timesheets', 'label': _('Timesheets'), 'fieldtype': 'Link', 'options': 'Timesheet', 'width': 80},
		{'fieldname' : 'from_time', 'label': _('From Time'), 'fieldtype': 'Datetime', 'width': 200},
		{'fieldname' : 'to_time', 'label': _('To Time'), 'fieldtype': 'Datetime', 'width': 200},
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
			['name', 'employee', 'from_date'],
			)
	if not isinstance(shift_avs, list):
		shift_avs = [shift_avs]
	shift_avs = sorted(shift_avs, key=lambda d: d['from_date'])
	shift_rqs = frappe.db.get_all(
			'Shift Request',
			{
				'docstatus': ['<', 2],
				'from_date': ['<=', filters.end],
				'to_date': ['>=', filters.start],
				},
			['name', 'employee', 'from_date'],
			order_by='shift_type asc'
			)
	if not isinstance(shift_rqs, list):
		shift_rqs = [shift_rqs]
	shift_rqs = sorted(shift_rqs, key=lambda d: d['from_date'])
	shift_ass = frappe.db.get_all(
			'Shift Assignment',
			{
				'docstatus': ['<', 2],
				'start_date': ['<=', filters.end],
				'end_date': ['>=', filters.start],
				},
			['name', 'employee', 'start_date'],
			order_by='shift_type asc'
			)
	if not isinstance(shift_ass, list):
		shift_ass = [shift_ass]
	shift_ass = sorted(shift_ass, key=lambda d: d['start_date'])
	tss = frappe.db.get_all(
			'Timesheet',
			{
				'docstatus': ['<', 2],
				'start_date': ['<=', filters.end],
				'end_date': ['>=', filters.start],
				'employee': ['!=', ''],
				},
			['name', 'employee'],
			order_by='start_date asc'
			)
	if not isinstance(tss, list):
		tss = [tss]
	employees = [av['employee'] for av in shift_avs]
	employees += [rq['employee'] for rq in shift_rqs]
	employees += [aas['employee'] for aas in shift_ass]
	employees += [ts['employee'] for ts in tss]
	employees = set(employees)
	employees = sorted(employees, key=lambda d: frappe.db.get_value('Employee', d, 'employee_name'))
	emps = [{'name': _('Employees'), 'indent': 0}]
	for emp in employees:
		savs, srqs, sas, ts_s = [], [], [], []
		emp_name = frappe.db.get_value('Employee', emp, 'employee_name')
		emp_list = [{'name': emp_name, 'employee': emp, 'employee_name': emp_name, 'indent': 1}]
#		emps.append({'name': emp_name, 'employee': emp, 'employee_name': emp_name, 'indent': 1})		
		for shift_av in shift_avs:
			if shift_av['employee'] == emp:
				savs.append({
					'employee': emp,
					'employee_name': emp_name,
					'shift_avaibilities': shift_av['name'],
				})
		for shift_rq in shift_rqs:
			if shift_rq['employee'] == emp:
				srqs.append({
					'employee': emp,
					'employee_name': emp_name,
					'shift_requests': shift_rq['name'],
					})
		for shift_as in shift_ass:
			if shift_as['employee'] == emp:
				sas.append({
					'employee': emp,
					'employee_name': emp_name,
					'shift_assignments': shift_as['name'],
					})
		for ts in tss:
			if ts['employee'] == emp:
				ts_s.append({
					'employee': emp,
					'employee_name': emp_name,
					'timesheets': ts['name']
					})
		for sav, srq, sa, ts, e in itertools.zip_longest(savs, srqs, sas, ts_s, emp_list):
			if sav == None:
				sav = {}
			if srq == None:
				srq = {}
			if sa == None:
				sa = {}
			if ts == None:
				ts = {}
			if e != None:
				line = {**e, **sav, **srq, **sa, **ts}
			else:
				line = {**sav, **srq, **sa, **ts, 'indent': 2}
			emps.append(line)
	return emps

def get_sales_orders(filters=None):
	res = [{'name': _('Sales Order'), 'indent': 0}]
	wigp = frappe.db.get_single_value('Selling Settings', 'workforce_item_group')
	wigs = item_group.get_child_item_groups(wigp)
	sos = frappe.db.get_all(
			'Sales Order',
			{
				'delivery_date': ['between', [filters.start, filters.end]],
				'docstatus': ['<', 2],
				},
			['name', 'delivery_date', 'customer', 'shipping_address_name'],
			order_by='delivery_date asc'
			)
	needed_qties = []
	sols_qties_list = []
	for so in sos:
		if filters.get('items'):
			items = frappe.db.get_all('Sales Order Item', 
							 {
								 'parent': so['name'], 
								 'item_code': ['in', filters.get('items')]
								 }, 
							 ['item_code', 'qty', 'uom', 'description'],
							 order_by='idx asc'
							 )
		else:
			items = frappe.db.get_all('Sales Order Item',
							 {
								 'parent': so['name'],
								 'item_code': ['in', get_working_items()]
								 }, 
							 ['item_code', 'qty', 'uom', 'description'],
							 order_by='idx asc'
							 )
		sols_dict = get_sales_order_links(so['name'], filters)
		sols = sols_dict['sols']
		sols_qties = sols_dict['qties']
		qty_needed = 0
		for item in items:
			qty_needed += item['qty']
		needed_qties.append(qty_needed)
		sols_qties_list.append(sols_qties)
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
	return {'data': res, 'sos': sos, 'needed_qties': needed_qties, 'sols_qties_list': sols_qties_list}

def get_sales_order_links(sales_order=None, filters=None):
	sols = []
	tss = []
	if filters.get('activity_type'):
		srqs = frappe.db.get_all(
				'Shift Request',
				{'sales_order': sales_order, 'docstatus': ['<', '2'], 'activity_type': ['in', filters.get('activity_type')]},
				['name', 'employee', 'shift_type', 'activity_type', 'from_date', 'to_date'],
				order_by='shift_type asc'
				)
		n_srqs = frappe.db.count(
				'Shift Request',
				{'sales_order': sales_order, 'docstatus': ['<', '2'], 'activity_type': ['in', filters.get('activity_type')]}
				)
		srqs = sorted(srqs, key=lambda d: d['from_date'])
		sass = frappe.db.get_all(
				'Shift Assignment',
				{'sales_order': sales_order, 'docstatus': ['<', '2'], 'activity_type': ['in', filters.get('activity_type')]},
				['name', 'employee', 'shift_type', 'activity_type', 'start_date', 'end_date'],
				order_by='shift_type asc'
				)
		n_sass = frappe.db.count(
				'Shift Assignment',
				{'sales_order': sales_order, 'docstatus': ['<', '2'], 'activity_type': ['in', filters.get('activity_type')]}
				)
		sass = sorted(sass, key=lambda d: d['start_date'])
		tls = frappe.db.get_all(
				'Timesheet Detail',
				{'sales_order': sales_order, 'docstatus': ['<', '2'], 'activity_type': ['in', filters.get('activity_type')]},
				['parent', 'activity_type', 'from_time', 'to_time'],
				order_by='from_time asc'
				)
		n_tls = frappe.db.count(
				'Timesheet Detail',
				{'sales_order': sales_order, 'docstatus': ['<', '2'], 'activity_type': ['in', filters.get('activity_type')]}
				)
	else:
		srqs = frappe.db.get_all(
				'Shift Request',
				{'sales_order': sales_order, 'docstatus': ['<', '2']},
				['name', 'employee', 'shift_type', 'activity_type', 'from_date', 'to_date'],
				order_by='shift_type asc'
				)
		n_srqs = frappe.db.count(
				'Shift Request',
				{'sales_order': sales_order, 'docstatus': ['<', '2']}
				)
		srqs = sorted(srqs, key=lambda d: d['from_date'])
		sass = frappe.db.get_all(
				'Shift Assignment',
				{'sales_order': sales_order, 'docstatus': ['<', '2']},
				['name', 'employee', 'shift_type', 'activity_type', 'start_date', 'end_date'],
				order_by='shift_type asc'
				)
		n_sass = frappe.db.count(
				'Shift Assignment',
				{'sales_order': sales_order, 'docstatus': ['<', '2']}
				)
		sass = sorted(sass, key=lambda d: d['start_date'])
		tls = frappe.db.get_all(
				'Timesheet Detail',
				{'sales_order': sales_order, 'docstatus': ['<', '2']},
				['parent', 'activity_type', 'from_time', 'to_time'],
				order_by='from_time asc'
				)
		n_tls = frappe.db.count(
				'Timesheet Detail',
				{'sales_order': sales_order, 'docstatus': ['<', '2']}
				)
	qties = {'shift_requests': n_srqs, 'shift_assignments': n_sass, 'timesheets': n_tls}
	for tl in tls:
		ts = frappe.get_all('Timesheet', {'name': tl['parent'], 'docstatus': ['<', '2']}, ['name', 'employee'])[0]
		ts.update({'from_time': tl['from_time'], 'to_time': tl['to_time'], 'activity_type': tl['activity_type']})
		tss.append(ts)
	employees = [rq['employee'] for rq in srqs]
	employees += [aas['employee'] for aas in sass]
	employees += [ts['employee'] for ts in tss]
	employees = set(employees)
	employees = sorted(employees, key=lambda d: frappe.db.get_value('Employee', d, 'employee_name'))
	for emp in employees:
		srq_s = []
		sa_s = []
		ts_s = []
		for srq in srqs:
			if srq['employee'] == emp:
				shift_type = srq['shift_type']
				sd = srq['from_date']
				ed = srq['to_date']
				from_time = None
				to_time = None
				if isinstance(sd, datetime.date):
					from_time = get_datetime(sd) + frappe.db.get_value('Shift Type', shift_type, 'start_time')
				if isinstance(ed, datetime.date):
					to_time = get_datetime(ed) + frappe.db.get_value('Shift Type', shift_type, 'end_time')
				srq_s.append({
					'employee': emp,
					'employee_name': frappe.db.get_value('Employee', srq['employee'], 'employee_name'),
					'shift_requests': srq['name'],
					'shift_type': shift_type,
					'activity_type': srq['activity_type'],
					'from_time': from_time,
					'to_time': to_time,
					})
		for sas in sass:
			if sas['employee'] == emp:
				shift_type = sas['shift_type']
				sd = sas['start_date']
				ed = sas['end_date']
				from_time = None
				to_time = None
				if isinstance(sd, datetime.date):
					from_time = get_datetime(sd) + frappe.db.get_value('Shift Type', shift_type, 'start_time')
				if isinstance(ed, datetime.date):
					to_time = get_datetime(ed) + frappe.db.get_value('Shift Type', shift_type, 'end_time')
				sa_s.append({
					'employee': emp,
					'employee_name': frappe.db.get_value('Employee', sas['employee'], 'employee_name'),
					'shift_assignments': sas['name'],
					'shift_type': shift_type,
					'activity_type': sas['activity_type'],
					'from_time': from_time,
					'to_time': to_time,
					})
		for ts in tss:
			if ts['employee'] == emp:
				ts_s.append({
					'employee': emp,
					'employee_name': frappe.db.get_value('Employee', ts['employee'], 'employee_name'),
					'timesheets': ts['name'],
					'activity_type': ts['activity_type'],
					'from_time': ts['from_time'],
					'to_time': ts['to_time'],
					})
		for srq, sa, ts in itertools.zip_longest(srq_s, sa_s, ts_s):
			if srq == None:
				srq = {}
			if sa == None:
				sa = {}
			if ts == None:
				ts = {}
			line = {**srq, **sa, **ts, 'indent': 2}
			sols.append(line)
		sols = sorted(sols, key=lambda d: d['from_time'])
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
	srqs, sass, tls, items = 0, 0, 0, 0
	human_needs = 0
	for so in sos:
		if filters.get('items'):
			items = frappe.db.get_all('Sales Order Item', {'parent': so['name'], 'item_code': ['in', filters.get('items')]}, ['qty'])
		else:
			items = frappe.db.get_all('Sales Order Item', {'parent': so['name'], 'item_code': ['in', get_working_items()]}, ['qty'])
		for item in items:
			human_needs += item['qty']
		srqs += frappe.db.count('Shift Request', {'sales_order': so['name'], 'docstatus': ['<', '2']})
		sass += frappe.db.count('Shift Assignment', {'sales_order': so['name'], 'docstatus': ['<', '2']})
		tls += frappe.db.count('Timesheet Detail', {'sales_order': so['name'], 'docstatus': ['<', '2']})
	res = [
		{'label': 'Sales Orders', 'value': lsos, 'indicator': 'Blue'},
		{'label': 'Human Needs', 'value': human_needs, 'indicator': 'Blue'},
		{'label': 'Shift Requests', 'value': srqs, 'indicator': get_indicator(srqs, human_needs)},
		{'label': 'Shift Assignments', 'value': sass, 'indicator': get_indicator(sass, human_needs)},
		{'label': 'Timesheet Log', 'value': tls, 'indicator': get_indicator(tls, human_needs)},
		]
	return res

def get_chart(sos, needed_qties, sols_qties_list, filters=None):
	so_labels = []
	for so in sos:
		desc = str(so.name) + ' ' + str(so.delivery_date) + '\n' + str(so.customer) + ' ' + str(so.shipping_address_name)
		so_labels.append(desc)
	srs = [qty['shift_requests'] for qty in sols_qties_list]
	sas = [qty['shift_assignments'] for qty in sols_qties_list]
	tss = [qty['timesheets'] for qty in sols_qties_list]
	chart = {
		'data': {
			'labels': so_labels,
			'datasets': [
				{'name': _('Qty Needed'), 'values': needed_qties},
				{'name': _('Shift Requests'), 'values': srs},
				{'name': _('Shift Assignments'), 'values': sas},
				{'name': _('Timesheets'), 'values': tss},
			]
		},
		'type': 'bar'
	}
	return chart

def get_indicator(value, ref):
	if value >= ref:
		color = 'Green'
	elif value >= 0.75 * ref:
		color = 'Orange'
	else:
		color = 'Red'
	return color

@frappe.whitelist()
def get_working_items():
	wigp = frappe.db.get_single_value('Selling Settings', 'workforce_item_group')
	wigs = item_group.get_child_item_groups(wigp)
	items = [item['name'] for item in frappe.db.get_all('Item', {'item_group': ['in', wigs]})]
	return items
