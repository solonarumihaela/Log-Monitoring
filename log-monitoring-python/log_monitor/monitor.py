from collections import defaultdict
from typing import List, Dict, Tuple
from .models import LogEntry, JobResult

class MonitoringReport:
    def __init__(self, results: List[JobResult], unmatched_starts: List[LogEntry], unmatched_ends: List[LogEntry]):
        self.results = results
        self.unmatched_starts = unmatched_starts
        self.unmatched_ends = unmatched_ends

    @property
    def summary(self) -> Dict[str, int]:
        levels = {"OK": 0, "WARNING": 0, "ERROR": 0}
        for r in self.results:
            lvl = r.level()
            levels[lvl or "OK"] += 1
        return levels

# Matches START/END log entries to build job results and track unmatched events
def build_report(entries: List[LogEntry]) -> MonitoringReport:
    stacks: Dict[Tuple[str,str], List[LogEntry]] = defaultdict(list)
    results: List[JobResult] = []
    unmatched_ends: List[LogEntry] = []

    for e in entries:
        key = e.key
        if e.state == "START":
            stacks[key].append(e)  # Push START event to stack
        else:
            if stacks[key]:
                s = stacks[key].pop()  # Pop matching START event
                results.append(JobResult(
                    pid=e.pid,
                    description=e.description,
                    start=s.timestamp,
                    end=e.timestamp,
                    duration=e.timestamp - s.timestamp
                ))
            else:
                unmatched_ends.append(e)  # No matching START for this END

    # Collect all unmatched START events left in stacks
    unmatched_starts = [x for stack in stacks.values() for x in stack]

    return MonitoringReport(results, unmatched_starts, unmatched_ends)
