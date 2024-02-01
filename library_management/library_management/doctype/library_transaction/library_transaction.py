# Copyright (c) 2024, LynX and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryTransaction(Document):
    def on_submit(self):
        articleDoc = frappe.get_doc('Article', self.article)
        if self.type == 'Issue':
            articleDoc.status = 'Issued'
            articleDoc.save()
        elif self.type == 'Return':
            articleDoc.status = 'Available'
            articleDoc.save()

        max_articles = frappe.db.get_single_value('Library Settings', 'max_articles')
        count = frappe.db.count('Library Transaction', filters={'library_member': self.library_member, 'type': 'Issue', 'docstatus': 1})
        if count > max_articles:
            frappe.throw(f'You have already issued {max_articles} articles')
