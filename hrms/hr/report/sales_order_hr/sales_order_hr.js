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
 	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
		value = default_formatter(row, cell, value, columnDef, dataContext);
	if (columnDef.id == "Quantity Needed" && dataContext["Quantity Needed"] > 0) {
			value = "<span style='color:blue!important;font-weight:bold'>" + value + "</span>";
	}
	if (columnDef.id == "Shift Requests" && dataContext["Quantity Needed"] > 0 && dataContext["Shift Requests"] < dataContext["Quantity Needed"] ) {
	if (columnDef.id == "Customer" && columnDef.id != "Payment Date" && dataContext["Rental Payment"] > 100) {
			value = "<span style='color:green!important;font-weight:bold'>" + value + "</span>";
	}
	return value;
 }
};
