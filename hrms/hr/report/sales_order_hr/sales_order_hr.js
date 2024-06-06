// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */


let n = [];
frappe.query_reports["Sales Order HR"] = {
	"filters": [
		{
			fieldname: 'start',
			label: __('Start'),
			fieldtype: 'Date',
			reqd: '1',
		},
		{
			fieldname: 'end',
			label: __('End'),
			fieldtype: 'Date',
			reqd: '1',
		},
		{
			fieldname: 'items',
			label: __('Items'),
			fieldtype: 'MultiSelectList',
			options: 'Item',
			get_data: function(txt) {
				frappe.call({
					type: 'GET',
					method: 'hrms.hr.report.sales_order_hr.sales_order_hr.get_working_items',
					callback: (data) => {n = data.message},
					freeze: true,
				});
				return frappe.db.get_link_options('Item', txt, {name: ['in', n]})
			}
		},
		{
			fieldname: 'activity_type',
			label: __('Activity Type'),
			fieldtype: 'MultiSelectList',
			options: 'Activity Type',
			get_data: function(txt) {
				return frappe.db.get_link_options('Activity Type', txt)
			}
		},
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
