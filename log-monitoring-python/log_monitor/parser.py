from datetime import datetime, date, timedelta
from typing import Iterable, List
from .models import LogEntry

# Parse a timestamp string (HH:MM:SS) into a datetime object
# Handles day rollover if times go past midnight
def _parse_timestamp(ts: str, base: date | None = None, last: datetime | None = None) -> datetime:
    base = base or date.today()
    h, m, s = map(int, ts.split(":"))
    dt = datetime(base.year, base.month, base.day, h, m, s)
    if last and dt < last:
        dt += timedelta(days=1)  # If time goes backwards, assume next day
    return dt

# Parse lines from log file into a list of LogEntry objects
# Each line should be in the format: timestamp, description, state, pid
def parse_lines(lines: Iterable[str]) -> List[LogEntry]:
    entries, last_dt = [], None  # List to hold parsed entries, last_dt for day rollover
    for raw in lines:
        if not (raw := raw.strip()):
            continue
        ts, desc, state, pid = [p.strip() for p in raw.split(",")]
        dt = _parse_timestamp(ts, last=last_dt)
        last_dt = dt
        entries.append(LogEntry(timestamp=dt, description=desc, state=state, pid=pid))  # Create LogEntry object
    return entries
