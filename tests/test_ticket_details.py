"""V1.1 tests for CR-1 (ticket detail view). Expected results come from
FR5 / BR5 in requirements.md. The V1.0 tests in test_service.py are kept
unchanged and re-run as the regression suite."""
import pytest

from tickets.service import (TicketError, advance_status, create_ticket,
                             get_ticket_details)


def make(store, user="alice", title="Laptop will not start"):
    return create_ticket(store, user, "employee", title, "Details here", "Hardware")


def test_employee_opens_own_ticket(store):  # FR5
    t = make(store)
    d = get_ticket_details(store, "alice", "employee", t.id)
    assert d.title == "Laptop will not start"
    assert d.description == "Details here"
    assert d.status == "New"


def test_employee_cannot_open_other_users_ticket(store):  # BR5 (security)
    t = make(store, user="alice")
    with pytest.raises(TicketError):
        get_ticket_details(store, "bob", "employee", t.id)


def test_other_users_ticket_and_missing_ticket_give_same_error(store):  # BR5 no leakage
    t = make(store, user="alice")
    with pytest.raises(TicketError) as other:
        get_ticket_details(store, "bob", "employee", t.id)
    with pytest.raises(TicketError) as missing:
        get_ticket_details(store, "bob", "employee", 999)
    assert "not found" in str(other.value)
    assert "not found" in str(missing.value)


def test_it_can_open_any_ticket(store):  # BR5
    t = make(store, user="alice")
    assert get_ticket_details(store, "itbob", "it", t.id).created_by == "alice"


def test_full_resolution_text_is_returned(store):  # FR5 - defect found in validation
    long_note = "Step " * 300  # 1500 characters, far longer than a table cell
    t = make(store)
    advance_status(store, "it", t.id)
    advance_status(store, "it", t.id, resolution=long_note)
    d = get_ticket_details(store, "alice", "employee", t.id)
    assert d.resolution == long_note.strip()


@pytest.mark.parametrize("bad_id", [0, -1, "1", 1.5, None, True])
def test_invalid_ticket_id_rejected(store, bad_id):  # caller-controlled input
    make(store)
    with pytest.raises(TicketError):
        get_ticket_details(store, "alice", "employee", bad_id)


@pytest.mark.parametrize("role", ["admin", "", None])
def test_unknown_role_cannot_open_ticket(store, role):  # QR3
    t = make(store)
    with pytest.raises(TicketError):
        get_ticket_details(store, "alice", role, t.id)


def test_viewing_does_not_change_ticket(store):  # read-only operation
    t = make(store)
    get_ticket_details(store, "alice", "employee", t.id)
    assert t.status == "New" and t.resolution == ""
