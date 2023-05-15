// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shift Assignment', {
	setup: function(frm) {
		frm.set_query("sales_order", function() {
			return {
				filters: {
					"docstatus": ['<', '2'],
					"delivery_date": ['between', [frm.doc.start_date, frm.doc.end_date]]

				}
			};
		});
	},
	refresh: function(frm) {

	}
});
