// Copyright (c) 2024, LynX and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Transaction", {
  validate(frm) {
    check_article(frm);
  },
});

const check_membership = (frm) => {
  memberDoc = frappe.db.get_doc("Library Member", frm.doc.library_member).then((doc) => {
    let member = false;
    member = doc.memberships
      .reverse()
      .some(
        (membership) => membership.from_date <= frm.doc.date && membership.to_date >= frm.doc.date
      );
    console.log(member);
    if (!member) {
      frappe.msgprint(__("Member has no active membership"));
      frappe.validated = member;
    }
  });
};

const check_article = (frm) => {
  articleDoc = frappe.db.get_doc("Article", frm.doc.article).then((doc) => {
    if (frm.doc.type == "Issue" && check_membership(frm) && doc.status == "Issued") {
      frappe.msgprint(__("Article already issued"));
      frappe.validated = false;
    } else if (frm.doc.type == "Return" && doc.status == "Available") {
      frappe.msgprint(__("Article hasnt been issued"));
      frappe.validated = false;
    }
  });
};
