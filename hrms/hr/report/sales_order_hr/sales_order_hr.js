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

		let qty_needed = 0;
		if (column.id == 'qty_needed' && value > 0) {
				qty_needed = value;
				value = "<div style='font-weight:bold'>" + value + "</div>";
		};
		if (column.id == 'shift_requests' && value > 0) {
				if (value < qty_needed) {
					if (value >= 0.75 * qty_needed ) {
							value = "<div style='background-color:orange!important;font-weight:bold;width:100%'>" + value + "</div>";
					}
					else {
							value = "<div style='background-color:red!important;font-weight:bold;width:100%'>" + value + "</div>";
					}
				}
				else {
					value = "<div style='background-color:green!important;font-weight:bold;width:100%'>" + value + "</div>";
				}
		};
		if (column.id == 'shift_assignments' && value > 0) {
				if (value < qty_needed) {
					if (value >= 0.75 * qty_needed ) {
							value = "<div style='background-color:orange!important;font-weight:bold;width:100%'>" + value + "</div>";
					}
					else {
							value = "<div style='background-color:red!important;font-weight:bold;width:100%'>" + value + "</div>";
					}
				}
				else {
					value = "<div style='background-color:green!important;font-weight:bold;width:100%'>" + value + "</div>";
				}
		};
		if (column.id == 'timesheets' && value > 0) {
				if (value < qty_needed) {
					if (value >= 0.75 * qty_needed ) {
							value = "<div style='background-color:orange!important;font-weight:bold;width:100%'>" + value + "</div>";
					}
					else {
							value = "<div style='background-color:red!important;font-weight:bold;width:100%'>" + value + "</div>";
					}
				}
				else {
					value = "<div style='background-color:green!important;font-weight:bold;width:100%'>" + value + "</div>";
				}
		};
	return value;
	}
};
