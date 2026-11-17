"""Streamlit UI. Only displays data and collects input.
All rules and permission checks are in tickets/service.py.

V1.1 (CR-1): role switch moved from the sidebar to the top of the page
(mobile users missed it), and a ticket detail view shows the full text
(the resolution note was truncated in the table)."""
import streamlit as st

from tickets.models import CATEGORIES
from tickets.service import (NEXT_STATUS, TicketError, advance_status,
                             create_ticket, get_ticket_details, list_tickets)
from tickets.storage import InMemoryStore

st.set_page_config(page_title="IT Service Request System", page_icon="🛠️")


@st.cache_resource
def get_store() -> InMemoryStore:
    """One shared in-memory store, pre-loaded with demo data (risk R2)."""
    store = InMemoryStore()
    create_ticket(store, "alice", "employee", "Laptop will not start",
                  "Black screen after update.", "Hardware")
    create_ticket(store, "bob", "employee", "Cannot connect to VPN",
                  "Error 809 when working from home.", "Network")
    t = create_ticket(store, "alice", "employee", "Password reset needed",
                      "Locked out of email.", "Account")
    advance_status(store, "it", t.id)
    return store


def to_rows(tickets):
    # Short columns only; long text is shown in the detail view (CR-1).
    return [{"ID": t.id, "Title": t.title, "Category": t.category,
             "Status": t.status, "Created by": t.created_by} for t in tickets]


def show_details(store, user, role, tickets):
    """FR5: full details of one ticket, readable on a phone."""
    st.subheader("Ticket details")
    if not tickets:
        st.info("No tickets to show.")
        return
    chosen = st.selectbox("Open a ticket", tickets, key="detail_select",
                          format_func=lambda t: f"#{t.id} {t.title} ({t.status})")
    try:
        t = get_ticket_details(store, user, role, chosen.id)
    except TicketError as e:
        st.error(str(e))
        return
    with st.container(border=True):
        st.markdown(f"**#{t.id} – {t.title}**")
        st.markdown(f"**Status:** {t.status}  \n**Category:** {t.category}  \n"
                    f"**Created by:** {t.created_by}  \n"
                    f"**Submitted:** {t.created_at:%Y-%m-%d %H:%M}")
        st.markdown("**Description**")
        st.text(t.description or "(none)")
        st.markdown("**Resolution**")
        st.text(t.resolution or "Not resolved yet.")


store = get_store()

st.title("🛠️ IT Service Request System")

# ---- Simulated login at top of page (out of scope: real auth, risk R3) ----
with st.container(border=True):
    st.markdown("**Who are you?** (simulated login – switch role here)")
    role_label = st.radio("Role", ["Employee", "IT Support"], horizontal=True)
    user = st.text_input("Username", value="alice")
role = "employee" if role_label == "Employee" else "it"

if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))

# ---- Employee view ----
if role == "employee":
    st.subheader("Submit a new ticket")
    with st.form("new_ticket"):
        title = st.text_input("Title (5-100 characters)")
        description = st.text_area("Description (optional, max 1000 characters)")
        category = st.selectbox("Category", CATEGORIES)
        submitted = st.form_submit_button("Submit ticket")
    if submitted:
        try:
            t = create_ticket(store, user, role, title, description, category)
            st.session_state["flash"] = (
                f"Ticket #{t.id} submitted. Track it under 'Ticket details' below.")
            st.rerun()
        except TicketError as e:
            st.error(str(e))

    st.subheader("My tickets")
    try:
        mine = list_tickets(store, user, role)
        if mine:
            st.dataframe(to_rows(mine), hide_index=True)
        else:
            st.info("You have no tickets yet.")
        show_details(store, user, role, mine)
    except TicketError as e:
        st.error(str(e))

# ---- IT Support view ----
else:
    st.subheader("All tickets")
    tickets = list_tickets(store, user, role)
    st.dataframe(to_rows(tickets), hide_index=True)

    st.subheader("Update a ticket")
    open_tickets = [t for t in tickets if t.status in NEXT_STATUS]
    if not open_tickets:
        st.info("No open tickets.")
    else:
        chosen = st.selectbox(
            "Ticket", open_tickets, key="update_select",
            format_func=lambda t: f"#{t.id} {t.title} ({t.status})")
        next_status = NEXT_STATUS[chosen.status]
        resolution = ""
        if next_status == "Resolved":
            resolution = st.text_area("Resolution note (required)")
        if st.button(f"Move to '{next_status}'", type="primary"):
            try:
                advance_status(store, role, chosen.id, resolution)
                st.session_state["flash"] = f"Ticket #{chosen.id} moved to {next_status}."
                st.rerun()
            except TicketError as e:
                st.error(str(e))

    show_details(store, user, role, tickets)
