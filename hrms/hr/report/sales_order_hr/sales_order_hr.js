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
		if (column.id == 'shift_requests' && value > 0) {
			value = "<div style='font-weight:bold'>" + value + "</div>";
		};
		if (column.id == 'shift_assignments' && value > 0) {
			value = "<div style='font-weight:bold'>" + value + "</div>";
		};
		if (column.id == 'timesheets' && value > 0) {
			value = "<div style='font-weight:bold'>" + value + "</div>";
		};
	return value;
	}
};
