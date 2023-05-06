frappe.views.calendar['Shift Avaibility'] = {
    field_map: {
        start: 'from_date',
        end: 'to_date',
        id: 'name',
        allDay: 'all_day',
        title: 'title',
        status: 'status',
        color: 'color'
    },
    style_map: {
        Public: 'success',
        Private: 'info'
    },
    order_by: 'from_date',
    get_events_method: 'hrms.hr.doctype.shift_avaibility.get_events'
}
