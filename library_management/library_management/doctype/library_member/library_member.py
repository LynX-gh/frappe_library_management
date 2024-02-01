# Copyright (c) 2024, LynX and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import add_to_date, getdate
from frappe.model.document import Document
from email_validator import validate_email, EmailNotValidError


def update_member_name(doc):
    doc.full_name = f'{doc.first_name} {doc.last_name}'


def update_to_date(doc):
    for lms in doc.memberships:
        if not lms.to_date:
            lms.to_date = add_to_date(lms.from_date, seconds=lms.duration)


class LibraryMember(Document):

    def before_save(self):
        update_member_name(self)
        update_to_date(self)
        frappe.msgprint('After Save')

    def validate(self):

        # Get the previous membership end date
        end = frappe.get_last_doc('Library Membership', filters={'parent': self.name}, order_by='to_date')
        curr_end_date = end if end else getdate()

        # Validate new entries in the membership table
        for lms in self.memberships:
            if (not lms.to_date) and (getdate(lms.from_date) < curr_end_date):
                frappe.msgprint(f'From Date should be greater than {curr_end_date}', title='Invalid Membership', raise_exception=True)

        # Validate email address
        try:
            validate_email(self.email_address)
        except EmailNotValidError as e:
            frappe.msgprint(str(e), title='Invalid Details', raise_exception=True)
