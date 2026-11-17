"""Streamlit UI. Only displays data and collects input.
All rules and permission checks are in tickets/service.py."""
import streamlit as st

from tickets.models import CATEGORIES
from tickets.service import (NEXT_STATUS, TicketError, advance_status,
                             create_ticket, list_tickets)
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
    return [{"ID": t.id, "Title": t.title, "Category": t.category,
             "Status": t.status, "Created by": t.created_by,
             "Resolution": t.resolution} for t in tickets]


store = get_store()

# ---- Sidebar: simulated login (out of scope: real authentication, risk R3) ----
st.sidebar.header("Simulated login")
role_label = st.sidebar.radio("Role", ["Employee", "IT Support"])
role = "employee" if role_label == "Employee" else "it"
user = st.sidebar.text_input("Username", value="alice")
st.sidebar.caption("Prototype only: no real authentication.")

st.title("🛠️ IT Service Request System")

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
            st.session_state["flash"] = f"Ticket #{t.id} submitted."
            st.rerun()
        except TicketError as e:
            st.error(str(e))

    st.subheader("My tickets")
    try:
        rows = to_rows(list_tickets(store, user, role))
        if rows:
            st.dataframe(rows, hide_index=True)
        else:
            st.info("You have no tickets yet.")
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
            "Ticket", open_tickets,
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
