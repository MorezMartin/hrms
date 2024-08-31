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
			if (value != "") {
				let v = $(value)[0];

			if (parseInt(v.getAttribute('data-value')) > 0) {
				v.setAttribute("style", "font-weight: bold");
				value = v.outerHTML;
			};
				frappe.call({
					method: 'frappe.client.get_value',
					args: {
						'doctype': 'Shift Request',
						'filters': {'name': v.getAttribute('data-value')},
						'fieldname': 'status'
					},
					async: false,
					callback : (r) => {
						if (r.message.status == 'Draft') {
							v.setAttribute("style", "background-color:orange")
						}
						else if (r.message.status == 'Rejected') {
							v.setAttribute("style", "background-color:red")
						}
						else if (r.message.status == 'Approved') {
							v.setAttribute("style", "background-color:green")
						}
					}
				})
				value = v.outerHTML;
			};
		};
		if (column.id == 'shift_assignments') {
			if (value > 0) {
				value = "<div style='font-weight:bold'>" + value + "</div>";
			}
			if (value != "") {
				let v = $(value)[0];

			if (parseInt(v.getAttribute('data-value')) > 0) {
				v.setAttribute("style", "font-weight: bold");
				value = v.outerHTML;
			};
				frappe.call({
					method: 'frappe.client.get_value',
					args: {
						'doctype': 'Shift Assignment',
						'filters': {'name': v.getAttribute('data-value')},
						'fieldname': 'sales_order'
					},
					async: false,
					callback : (r) => {
						console.log(r.message.sales_order);
						if ((r.message.sales_order != "" ) && (r.message.sales_order != null) && (typeof r.message.sales_order != 'undefined')) {
							v.setAttribute("style", "background-color:green")
						}
						else if (typeof r.message.sales_order != 'undefined') {
							v.setAttribute("style", "background-color:orange")
						}
					}
				})
				value = v.outerHTML;
			};
		};
		if (column.id == 'timesheets' && value > 0) {
			if (value > 0) {
				value = "<div style='font-weight:bold'>" + value + "</div>";
			}
			if (value != "") {
				let v = $(value)[0];

			if (parseInt(v.getAttribute('data-value')) > 0) {
				v.setAttribute("style", "font-weight: bold");
				value = v.outerHTML;
			};
				frappe.call({
					method: 'frappe.client.get_value',
					args: {
						'doctype': 'Timesheet',
						'filters': {'name': v.getAttribute('data-value')},
						'fieldname': 'status'
					},
					async: false,
					callback : (r) => {
						if (r.message.status == 'Draft') {
							v.setAttribute("style", "background-color:red")
						}
						else if (r.message.status == 'Sent') {
							v.setAttribute("style", "background-color:orange")
						}
						else if (r.message.status == 'Declared') {
							v.setAttribute("style", "background-color:green")
						}
					}
				})
				value = v.outerHTML;
			};
		};
	return value;
	}
};
