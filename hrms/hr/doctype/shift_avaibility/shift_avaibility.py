# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ShiftAvaibility(Document):
	def validate(self):
		self.validate_dates()
		self.delete_shifts_on_unchecked_days()
	
	def validate_dates(self):
		av_dates = frappe.get_all(
			'Shift Avaibility', 
			filters={
				'employee': self.employee
				},
			fields=[
				'from_date',
				'to_date',
				],
			)
		for av_date in av_dates:
			if self.from_date in range(av_date['from_date'], av_date['to_date']):
				frappe.throw(__('From Date conflicts with an existing avaibility shift type'))
			if self.to_date in range(av_date['from_date'], av_date['to_date']):
				frappe.throw(__('To Date conflicts with an existing avaibility shift type'))

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
