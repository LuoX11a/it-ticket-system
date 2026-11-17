"""Data model for tickets."""
from dataclasses import dataclass, field
from datetime import datetime

STATUSES = ("New", "In Progress", "Resolved")
CATEGORIES = ("Hardware", "Software", "Network", "Account")


@dataclass
class Ticket:
    id: int
    title: str
    description: str
    category: str
    created_by: str
    status: str = "New"
    resolution: str = ""
    created_at: datetime = field(default_factory=datetime.now)
