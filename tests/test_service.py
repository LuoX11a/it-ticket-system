"""V1.0 tests. Expected results come from requirements.md, not from the code.
Keep ALL of these when adding new features - they are the regression suite."""
import pytest

from tickets.service import (TicketError, advance_status, create_ticket,
                             list_tickets)


def make(store, user="alice", title="Laptop will not start", category="Hardware"):
    return create_ticket(store, user, "employee", title, "Details here", category)


# ---------- FR1 / BR4: creating tickets ----------

def test_employee_creates_ticket(store):  # FR1
    t = make(store)
    assert t.id == 1
    assert t.status == "New"
    assert t.created_by == "alice"
    assert t.category == "Hardware"


@pytest.mark.parametrize("length, ok", [(4, False), (5, True), (100, True), (101, False)])
def test_title_length_boundaries(store, length, ok):  # BR4 boundary values
    title = "x" * length
    if ok:
        assert make(store, title=title).title == title
    else:
        with pytest.raises(TicketError):
            make(store, title=title)


def test_whitespace_only_title_rejected(store):  # BR4
    with pytest.raises(TicketError):
        make(store, title="        ")


def test_title_is_trimmed_before_length_check(store):  # BR4: "  abc  " is only 3 chars
    with pytest.raises(TicketError):
        make(store, title="   abc   ")


def test_description_too_long_rejected(store):  # BR4
    with pytest.raises(TicketError):
        create_ticket(store, "alice", "employee", "Valid title", "d" * 1001, "Software")


def test_invalid_category_rejected(store):  # FR1, caller-controlled input
    with pytest.raises(TicketError):
        make(store, category="Printer")


def test_empty_username_rejected(store):  # QR1
    with pytest.raises(TicketError):
        make(store, user="   ")


def test_it_cannot_create_ticket(store):  # role check
    with pytest.raises(TicketError):
        create_ticket(store, "itbob", "it", "Valid title", "", "Network")


# ---------- FR2 / FR3 / BR3: viewing tickets ----------

def test_employee_sees_only_own_tickets(store):  # BR3, FR2
    make(store, user="alice")
    make(store, user="bob", title="VPN not connecting", category="Network")
    alice_view = list_tickets(store, "alice", "employee")
    assert [t.created_by for t in alice_view] == ["alice"]


def test_it_sees_all_tickets(store):  # FR3
    make(store, user="alice")
    make(store, user="bob", title="VPN not connecting", category="Network")
    assert len(list_tickets(store, "anyone", "it")) == 2


# ---------- BR1 / BR2 / FR4: changing status ----------

def test_new_to_in_progress(store):  # BR1
    t = make(store)
    assert advance_status(store, "it", t.id).status == "In Progress"


def test_in_progress_to_resolved_with_note(store):  # BR1, FR4
    t = make(store)
    advance_status(store, "it", t.id)
    t = advance_status(store, "it", t.id, resolution="Replaced battery")
    assert t.status == "Resolved"
    assert t.resolution == "Replaced battery"


def test_resolve_without_note_rejected(store):  # FR4 expected failure
    t = make(store)
    advance_status(store, "it", t.id)
    with pytest.raises(TicketError):
        advance_status(store, "it", t.id, resolution="   ")
    assert store.get(t.id).status == "In Progress"  # state unchanged


def test_resolved_ticket_cannot_advance(store):  # BR1: no further/backward moves
    t = make(store)
    advance_status(store, "it", t.id)
    advance_status(store, "it", t.id, resolution="Fixed")
    with pytest.raises(TicketError):
        advance_status(store, "it", t.id, resolution="Again")
    assert store.get(t.id).status == "Resolved"


def test_employee_cannot_change_status(store):  # BR2, QR3 (risk R1)
    t = make(store)
    with pytest.raises(TicketError):
        advance_status(store, "employee", t.id)
    assert store.get(t.id).status == "New"  # failure must not change state


@pytest.mark.parametrize("role", ["admin", "IT", "", None])
def test_unknown_role_rejected(store, role):  # QR3 whitelist
    t = make(store)
    with pytest.raises(TicketError):
        advance_status(store, role, t.id)
    with pytest.raises(TicketError):
        list_tickets(store, "alice", role)


def test_ticket_not_found(store):  # QR1: error, not crash
    with pytest.raises(TicketError):
        advance_status(store, "it", 999)
