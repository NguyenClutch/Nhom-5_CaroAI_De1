from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Button:
    label: str
    action: str
    rect: Any | None = None
