// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shift Request", {
	setup: function (frm) {
		frm.set_query("approver", function () {
			return {
				query: "hrms.hr.doctype.department_approver.department_approver.get_approvers",
				filters: {
					employee: frm.doc.employee,
					doctype: frm.doc.doctype,
				},
			};
		});
		frm.set_query("employee", erpnext.queries.employee);
		frm.set_query("sales_order", function() {
			return {
				filters: {
					"docstatus": ['<', '2'],
					"delivery_date": ['between', [frm.doc.from_date, frm.doc.to_date]]

				}
			};
		});
	},
});
