# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate
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
				'docstatus': ['!=', 2],
			}):
			frappe.throw(_('Shift Avaibility already exists for this To Date'))
		if frappe.db.exists('Shift Avaibility', {
				'name': ['!=', self.name],
				'employee': self.employee,
				'to_date': ['between', [self.from_date, self.to_date]],
				'docstatus': ['!=', 2],
			}):
			frappe.throw(_('Shift Avaibility already exists for this From Date'))
		if frappe.db.exists('Shift Avaibility', {
				'name': ['!=', self.name],
				'employee': self.employee,
				'from_date': ['<=', self.from_date],
				'to_date': ['=>', self.to_date],
				'docstatus': ['!=', 2],
			}):
			frappe.throw(_('Shift Avaibility already exists in this period'))

	def delete_shifts_on_unchecked_days(self):
		if not self.monday:
			self.monday_avaibility = []
			frappe.db.commit
		if not self.tuesday:
			self.tuesday_avaibility = []
			frappe.db.commit
		if not self.wednesday:
			self.wednesday_avaibility = []
			frappe.db.commit
		if not self.thursday:
			self.thursday_avaibility = []
			frappe.db.commit
		if not self.friday:
			self.friday_avaibility = []
			frappe.db.commit
		if not self.saturday:
			self.saturday_avaibility = []
			frappe.db.commit
		if not self.sunday:
			self.sunday_avaibility = []
			frappe.db.commit

def check_avaibility(shift, from_date, to_date):
	av_shift = frappe.get_all('Shift Avaibility',
			{
				'employee': shift.employee,
				'from_date': ['<=', from_date],
				'to_date': ['>=', to_date],
			},
			[
				'name', 
				'monday', 
				'tuesday', 
				'wednesday', 
				'thursday', 
				'friday', 
				'saturday', 
				'sunday',
			],
		)
	if av_shift:
		av_shift = av_shift[0]
		td = getdate(to_date) - getdate(from_date) + datetime.timedelta(days=1)
		d = td.days
		dates = []
		date = getdate(from_date)
		for i in range(0,d):
			dates.append(date)
			date += datetime.timedelta(days=1)
			d+=1
		for date in dates:
			if date.isoweekday() == 1 and av_shift['monday']:
				avaibility_list = frappe.get_all('Avaibility Shift Type', {'parent': av_shift['name'], 'parentfield': 'monday_avaibility'}, ['shift_type'])
				avaibility = []
				for av in avaibility_list:
					avaibility.append(av['shift_type'])
				if shift.shift_type in avaibility:
					continue
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Monday'))
			elif date.isoweekday() == 1:
				frappe.throw(_('Employee not avaible on Monday'))

			elif date.isoweekday() == 2 and av_shift['tuesday']:
				avaibility_list = frappe.get_all('Avaibility Shift Type', {'parent': av_shift['name'], 'parentfield': 'tuesday_avaibility'}, ['shift_type'])
				avaibility = []
				for av in avaibility_list:
					avaibility.append(av['shift_type'])
				if shift.shift_type in avaibility:
					continue
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Tuesday'))
			elif date.isoweekday() == 2:
				frappe.throw(_('Employee not avaible on Tuesday'))

			elif date.isoweekday() == 3 and av_shift['wednesday']:
				avaibility_list = frappe.get_all('Avaibility Shift Type', {'parent': av_shift['name'], 'parentfield': 'wednesday_avaibility'}, ['shift_type'])
				avaibility = []
				for av in avaibility_list:
					avaibility.append(av['shift_type'])
				if shift.shift_type in avaibility:
					continue
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Wednesday'))
			elif date.isoweekday() == 3:
				frappe.throw(_('Employee not avaible on Wednesday'))

			elif date.isoweekday() == 4 and av_shift['thursday']:
				avaibility_list = frappe.get_all('Avaibility Shift Type', {'parent': av_shift['name'], 'parentfield': 'thursday_avaibility'}, ['shift_type'])
				avaibility = []
				for av in avaibility_list:
					avaibility.append(av['shift_type'])
				if shift.shift_type in avaibility:
					continue
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Thursday'))
			elif date.isoweekday() == 4:
				frappe.throw(_('Employee not avaible on Thursday'))

			elif date.isoweekday() == 5 and av_shift['friday']:
				avaibility_list = frappe.get_all('Avaibility Shift Type', {'parent': av_shift['name'], 'parentfield': 'friday_avaibility'}, ['shift_type'])
				avaibility = []
				for av in avaibility_list:
					avaibility.append(av['shift_type'])
				if shift.shift_type in avaibility:
					continue
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Friday'))
			elif date.isoweekday() == 5:
				frappe.throw(_('Employee not avaible on Friday'))

			elif date.isoweekday() == 6 and av_shift['saturday']:
				avaibility_list = frappe.get_all('Avaibility Shift Type', {'parent': av_shift['name'], 'parentfield': 'saturday_avaibility'}, ['shift_type'])
				avaibility = []
				for av in avaibility_list:
					avaibility.append(av['shift_type'])
				if shift.shift_type in avaibility:
					continue
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Saturday'))
			elif date.isoweekday() == 6:
				frappe.throw(_('Employee not avaible on Saturday'))

			elif date.isoweekday() == 7 and av_shift['sunday']:
				avaibility_list = frappe.get_all('Avaibility Shift Type', {'parent': av_shift['name'], 'parentfield': 'sunday_avaibility'}, ['shift_type'])
				avaibility = []
				for av in avaibility_list:
					avaibility.append(av['shift_type'])
				if shift.shift_type in avaibility:
					continue
				else:
					frappe.throw(_('Employee Not avaible on this Shift Type on Sunday'))
			elif date.isoweekday() == 7:
				frappe.throw(_('Employee not avaible on Sunday'))
	else:
		frappe.throw(_('Employee not avaible for this dates'))
