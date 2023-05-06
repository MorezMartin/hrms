# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class ShiftAvaibility(Document):
	def validate(self):
		self.validate_dates()
		self.delete_shifts_on_unchecked_days()

	def validate_dates(self):
		if frappe.db.exists('Shift Avaibility', {
				'employee': self.employee,
                'from_date': ['between', [self.from_date, self.to_date]],
			}):
			frappe.throw(_('Shift Avaibility already exists for this To Date'))
		if frappe.db.exists('Shift Avaibility', {
				'employee': self.employee,
                'to_date': ['between', [self.from_date, self.to_date]],
			}):
			frappe.throw(_('Shift Avaibility already exists for this From Date'))
		if frappe.db.exists('Shift Avaibility', {
				'employee': self.employee,
                'from_date': ['<=', self.from_date],
                'to_date': ['=>', self.to_date],
			}):
			frappe.throw(_('Shift Avaibility already exists in this period'))

	def delete_shifts_on_unchecked_days(self):
		if not self.monday:
			self.monday_avaibility = []
			frappe.db.commit
		if not self.tuesday:
			self.tuesday_avaibility = []
			frappe.db.commit
		if not self.monday:
			self.wednesday_avaibility = []
			frappe.db.commit
		if not self.monday:
			self.thursday_avaibility = []
			frappe.db.commit
		if not self.monday:
			self.friday_avaibility = []
			frappe.db.commit
		if not self.monday:
			self.saturday_avaibility = []
			frappe.db.commit
		if not self.monday:
			self.sunday_avaibility = []
			frappe.db.commit
