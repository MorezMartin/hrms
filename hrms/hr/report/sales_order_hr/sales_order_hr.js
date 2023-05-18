// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Order HR"] = {
	"filters": [
		{
			fieldname: 'end',
			label: __('Start'),
			options: 'Company',
		},
		{
			fieldname: 'end',
			label: __('End'),
			options: 'Company',
		}
	]
};
