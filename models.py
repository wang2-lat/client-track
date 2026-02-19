from dataclasses import dataclass
from typing import Optional

@dataclass
class Customer:
    name: str
    company: str = ""
    phone: str = ""
    email: str = ""
    notes: str = ""
    remind_date: Optional[str] = None
    id: Optional[int] = None
