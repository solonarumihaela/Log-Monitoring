from datetime import datetime, date, timedelta
from typing import Iterable, List
from .models import LogEntry

def _parse_timestamp(ts: str, base: date | None = None, last: datetime | None = None) -> datetime:
    base = base or date.today()
    h, m, s = map(int, ts.split(":"))
    candidate = datetime(base.year, base.month, base.day, h, m, s)
    if last and candidate < last:
        candidate += timedelta(days=1)
    return candidate

def parse_lines(lines: Iterable[str]) -> List[LogEntry]:
    entries = []
    last_dt = None
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        ts, desc, state, pid = [p.strip() for p in raw.split(",")]
        dt = _parse_timestamp(ts, last=last_dt)
        last_dt = dt
        entries.append(LogEntry(timestamp=dt, description=desc, state=state, pid=pid))
    return entries
