# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from erpnext.projects.doctype.timesheet.timesheet import Timesheet


class EmployeeTimesheet(Timesheet):
	def set_status(self):
		if self.docstatus > 0:
			self.status = {"1": "Submitted", "2": "Cancelled"}[str(self.docstatus)]
		elif self.status == "Sent":
			self.status = "Sent"
		else:
			self.status = "Draft"

		if self.per_billed == 100:
			self.status = "Billed"

		if self.status == "Sent":
			self.status = "Sent"

		if self.sales_invoice:
			self.status = "Completed"
