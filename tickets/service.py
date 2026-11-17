"""Business logic: all rules and permission checks live here (QR3).

The UI (app.py) only calls these functions, so every rule can be tested
directly with pytest without starting Streamlit.
"""
from copy import deepcopy
from typing import Iterable, List

from .models import CATEGORIES, Ticket
from .storage import InMemoryStore

ROLES = ("employee", "it")
# BR1: the ONLY allowed transitions. No skipping, no going back.
NEXT_STATUS = {"New": "In Progress", "In Progress": "Resolved"}

TITLE_MIN = 5
TITLE_MAX = 100
DESCRIPTION_MAX = 1000


class TicketError(Exception):
    """Expected business error. The UI shows it as a message (QR1)."""


def _require_role(role: str, allowed: Iterable[str]) -> None:
    # Whitelist check: unknown roles are rejected too (QR3).
    if role not in allowed:
        raise TicketError(f"Permission denied for role '{role}'.")


def _require_user(user) -> str:
    if not isinstance(user, str) or not user.strip():
        raise TicketError("Username is required.")
    return user.strip()


def create_ticket(store: InMemoryStore, user: str, role: str, title: str,
                  description: str, category: str) -> Ticket:
    """FR1: an employee submits a ticket."""
    _require_role(role, {"employee"})
    user = _require_user(user)

    if not isinstance(title, str):
        raise TicketError("Title is required.")
    title = title.strip()
    if not TITLE_MIN <= len(title) <= TITLE_MAX:  # BR4
        raise TicketError(
            f"Title must be {TITLE_MIN}-{TITLE_MAX} characters (after trimming spaces).")

    description = (description or "").strip()
    if len(description) > DESCRIPTION_MAX:  # BR4
        raise TicketError(f"Description must be at most {DESCRIPTION_MAX} characters.")

    if category not in CATEGORIES:  # caller-controlled input
        raise TicketError(f"Category must be one of: {', '.join(CATEGORIES)}.")

    ticket = Ticket(id=0, title=title, description=description,
                    category=category, created_by=user)
    return store.add(ticket)


def list_tickets(store: InMemoryStore, user: str, role: str) -> List[Ticket]:
    """FR2 / FR3: employees see only their own tickets (BR3); IT sees all."""
    _require_role(role, ROLES)
    if role == "it":
        return store.all()
    user = _require_user(user)
    return [t for t in store.all() if t.created_by == user]


def advance_status(store: InMemoryStore, role: str, ticket_id: int,
                   resolution: str = "") -> Ticket:
    """FR3 / FR4: IT moves a ticket to its next status only (BR1, BR2)."""
    _require_role(role, {"it"})  # BR2

    ticket = store.get(ticket_id)
    if ticket is None:
        raise TicketError(f"Ticket #{ticket_id} not found.")

    if ticket.status not in NEXT_STATUS:  # BR1: Resolved is final
        raise TicketError(f"Ticket #{ticket_id} is already {ticket.status}.")

    new_status = NEXT_STATUS[ticket.status]
    resolution = (resolution or "").strip()
    if new_status == "Resolved" and not resolution:  # FR4
        raise TicketError("A resolution note is required to resolve a ticket.")

    ticket.status = new_status
    if new_status == "Resolved":
        ticket.resolution = resolution
    return ticket


def get_ticket_details(store: InMemoryStore, user: str, role: str,
                       ticket_id) -> Ticket:
    """FR5 (V1.1): view the full details of one ticket.

    BR5: employees may only open their own tickets; IT may open any ticket.
    A ticket owned by someone else gives the SAME error as a missing ticket,
    so employees cannot discover which ticket IDs exist (no data leakage).

    Returns a COPY, not the stored object, so callers cannot change a ticket
    without going through create_ticket/advance_status (review finding RF-1).
    """
    _require_role(role, ROLES)
    # ticket_id is caller-controlled input: accept positive whole numbers only.
    if isinstance(ticket_id, bool) or not isinstance(ticket_id, int) or ticket_id < 1:
        raise TicketError("Ticket ID must be a positive whole number.")

    ticket = store.get(ticket_id)
    if ticket is None:
        raise TicketError(f"Ticket #{ticket_id} not found.")
    if role == "employee" and ticket.created_by != _require_user(user):
        raise TicketError(f"Ticket #{ticket_id} not found.")  # BR5
    return deepcopy(ticket)  # RF-1: read-only view of stored data
