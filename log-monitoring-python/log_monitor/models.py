from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Tuple

@dataclass(frozen=True)
class LogEntry:
    timestamp: datetime
    description: str
    state: str
    pid: str

    @property
    def key(self) -> Tuple[str, str]:
        return (self.pid, self.description)

@dataclass
class JobResult:
    pid: str
    description: str
    start: datetime
    end: datetime
    duration: timedelta

    def level(self, warn_seconds: int = 300, error_seconds: int = 600) -> Optional[str]:
        secs = self.duration.total_seconds()
        if secs > error_seconds:
            return "ERROR"
        if secs > warn_seconds:
            return "WARNING"
        return None
