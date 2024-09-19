# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from frappe.utils.data import flt

from erpnext.projects.doctype.timesheet.timesheet import Timesheet


class EmployeeTimesheet(Timesheet):
	def set_status(self):
		if self.docstatus > 0:
			self.status = {"1": "Submitted", "2": "Cancelled"}[str(self.docstatus)]
		elif self.status not in ("Sent", "Declared"):
			self.status = "Draft"

		if flt(self.per_billed, self.precision("per_billed")) >= 100.0:
			self.status = "Billed"

		if 0.0 < flt(self.per_billed, self.precision("per_billed")) < 100.0:
			self.status = "Partially Billed"

		if self.salary_slip:
			self.status = "Payslip"

		if self.status == "Sent":
			self.status = "Sent"

		if self.status == "Declared":
			self.status = "Declared"

		if self.sales_invoice:
			self.status = "Completed"
