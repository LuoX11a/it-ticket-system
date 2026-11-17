"""Simple in-memory storage (prototype scope - see risk R2 in requirements.md)."""
from typing import Dict, List, Optional

from .models import Ticket


class InMemoryStore:
    def __init__(self) -> None:
        self._tickets: Dict[int, Ticket] = {}
        self._next_id = 1

    def add(self, ticket: Ticket) -> Ticket:
        ticket.id = self._next_id
        self._tickets[ticket.id] = ticket
        self._next_id += 1
        return ticket

    def get(self, ticket_id: int) -> Optional[Ticket]:
        return self._tickets.get(ticket_id)

    def all(self) -> List[Ticket]:
        return sorted(self._tickets.values(), key=lambda t: t.id)
