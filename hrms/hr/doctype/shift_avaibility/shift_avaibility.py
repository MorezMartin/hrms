# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
import datetime

class ShiftAvaibility(Document):
	def validate(self):
		self.validate_dates()
		self.delete_shifts_on_unchecked_days()

	def validate_dates(self):
		if frappe.db.exists('Shift Avaibility', {
	            'name': ['!=', self.name],
				'employee': self.employee,
	            'from_date': ['between', [self.from_date, self.to_date]],
			}):
			frappe.throw(_('Shift Avaibility already exists for this To Date'))
		if frappe.db.exists('Shift Avaibility', {
	            'name': ['!=', self.name],
				'employee': self.employee,
	            'to_date': ['between', [self.from_date, self.to_date]],
			}):
			frappe.throw(_('Shift Avaibility already exists for this From Date'))
		if frappe.db.exists('Shift Avaibility', {
	            'name': ['!=', self.name],
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

def check_avaibility(shift):
	av_shift = frappe.get_all('Shift Avaibility', {
	    'employee': shift.employee,
        'from_date': ['<=', shift.from_date],
        'to_date': ['>=', shift.to_date],
	    })
	if av_shift:
        av_shift = av_shift[0]
		td = shift[to_date] - [from_date]
		d = td.days
		dates = []
		date = shift.from_date
		for i in range(1,d):
			dates.append(date)
			date += datetime.timedelta(days=1)
			d+=1
		for date in dates:
			if date.isoweekday() == 1 and av_shift.monday:
				if shift.shift_type in av_shift.monday_avaibility:
					pass
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Monday'))
			elif date.isoweekday() == 1:
				frappe.throw(_('Employee not avaible on Monday'))

			elif date.isoweekday() == 2 and av_shift.tuesday:
				if shift.shift_type in av_shift.tuesday_avaibility:
					pass
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Tuesday'))
			elif date.isoweekday() == 2:
				frappe.throw(_('Employee not avaible on Tuesday'))

			elif date.isoweekday() == 3 and av_shift.wednesday:
				if shift.shift_type in av_shift.wednesday_avaibility:
					pass
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Wednesday'))
			elif date.isoweekday() == 3:
				frappe.throw(_('Employee not avaible on Wednesday'))

			elif date.isoweekday() == 4 and av_shift.thursday:
				if shift.shift_type in av_shift.thursday_avaibility:
					pass
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Thursday'))
			elif date.isoweekday() == 4:
				frappe.throw(_('Employee not avaible on Thursday'))

			elif date.isoweekday() == 5 and av_shift.friday:
				if shift.shift_type in av_shift.friday_avaibility:
					pass
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Friday'))
			elif date.isoweekday() == 5:
				frappe.throw(_('Employee not avaible on Friday'))

			elif date.isoweekday() == 6 and av_shift.saturday:
				if shift.shift_type in av_shift.saturday_avaibility:
					pass
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Saturday'))
			elif date.isoweekday() == 6:
				frappe.throw(_('Employee not avaible on Saturday'))

			elif date.isoweekday() == 7 and av_shift.sunday:
				if shift.shift_type in av_shift.sunday_avaibility:
					pass
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Sunday'))
			elif date.isoweekday() == 7:
				frappe.throw(_('Employee not avaible on Sunday'))
	else:
	    frappe.throw(_('Employee not avaible for this dates'))
