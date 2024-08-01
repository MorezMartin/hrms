// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Order HR"] = {
	"filters": [
		{
			fieldname: 'start',
			label: __('Start'),
			fieldtype: 'Date',
			options: 'Company',
		},
		{
			fieldname: 'end',
			label: __('End'),
			fieldtype: 'Date',
			options: 'Company',
		}
	],
	formatter:function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.id == 'qty_needed' && value > 0) {
			value = "<div style='font-weight:bold'>" + value + "</div>";
		};
		if (column.id == 'shift_requests') {
			if (value > 0) {
				value = "<div style='font-weight:bold'>" + value + "</div>";
			}
			else {
				frappe.call({
					method: 'frappe.client.get_value',
					args: {
						'doctype': 'Shift Request',
						'filters': {'name': value},
						'fieldname': 'status'
					},
					callback: function(r) {
						if (r.message.status == 'Draft') {
							value = "<div style='background-color:orange'>" + value + "</div>";
						}
						else if (r.message.status == 'Rejected') {
							value = "<div style='background-color:red'>" + value + "</div>";
						}
						else if (r.message.status == 'Approved') {
							value = "<div style='background-color: green'>" + value + "</div>";
						}
					}
				});
			}
		};
		if (column.id == 'shift_assignments') {
			if (value > 0) {
				value = "<div style='font-weight:bold'>" + value + "</div>";
			}
			else {
				frappe.call({
					method: 'frappe.client.get_value',
					args: {
						'doctype': 'Shift Assignment',
						'filters': {'name': value},
						'fieldname': 'sales_order'
					},
					callback: function(r) {
						if (r.message.sales_order != null) {
							value = "<div style='background-color:green'>" + value + "</div>";
						}
						else {
							value = "<div style='background-color:orange'>" + value + "</div>";
						}
					}
				});
			}
		};
		if (column.id == 'timesheets' && value > 0) {
			value = "<div style='font-weight:bold'>" + value + "</div>";
		};
	return value;
	}
};
