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
			console.log(value)
				value = "<div style='font-weight:bold'>" + value + "</div>";
		}

		let ha = ['shift_requests', 'shift_assignments', 'timesheets'];
		ha.forEach(format);
		function format(h) {
			if (column.id == h && value > 0 && data['qty_needed'] > 0) {
				if (value < data['qty_needed']) {
					if (value >= 0.75 * data["qty_needed"] ) {
							value = "<div style='background-color:orange!important;font-weight:bold;width:100%'>" + value + "</div>";
					}
					else {
							value = "<div style='background-color:red!important;font-weight:bold;width:100%'>" + value + "</div>";
					}
				}
				else {
					value = "<div style='background-color:green!important;font-weight:bold;width:100%'>" + value + "</div>";
				}
			}
		}
	return value;
	}
};
