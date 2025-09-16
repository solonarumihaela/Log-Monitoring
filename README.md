# Log Monitoring Application

A Python application that processes a log file, calculates job durations, and generates a report highlighting jobs that exceed defined time thresholds.

---

## Functionality

- Parses `logs.log`, a CSV-like log file containing `START` and `END` events
- Considers only entries containing `"job"` in the description (scheduled tasks are ignored)
- Matches `START` and `END` pairs by `(description, PID)`
- Calculates job durations based on timestamps (HH:MM:SS)
- Classification rules:
  - **OK** — duration ≤ 5 minutes (≤ 300s)
  - **WARNING** — 5 < duration ≤ 10 minutes (300–600s)
  - **ERROR** — duration > 10 minutes (> 600s)
- Outputs a report to both console and `output.log`

---

## Architecture

```
log-monitoring-python/
│
├── log_monitor/
│   ├── cli.py            # CLI entry point
│   ├── parser.py         # Line parsing logic
│   ├── monitor.py        # Job tracking and report generation
│   └── models.py         # LogEntry, JobResult, MonitoringReport
│
├── tests/
│   └── test_monitor.py   # Unit tests for core functionality
│
├── run_tests.py          # Custom test runner
│
logs.log                  # Sample log input (outside log-monitoring-python)
output.log                # Generated report (outside log-monitoring-python)
README.md                 # Project documentation (outside log-monitoring-python)
```

---

## Testing

- Implemented with `unittest`
- **10 unit tests** validating:
  - Threshold-based classification (OK / WARNING / ERROR)
  - Multiple jobs with different PIDs
  - Handling of missing START or END entries
  - Ignoring non-job (scheduled task) entries
  - Multiple START/END pairs for the same PID
- Custom runner (`run_tests.py`) produces a clear `[OK] / [NOT OK]` summary saved to `test_results.log`

Example test output:
```
[OK]       Duration exactly 5 minutes
[OK]       Duration exactly 10 minutes
[OK]       Duration over 10 minutes
...
```

---

## Usage

**Run the application:**
```bash
cd log-monitoring-python
python3 -m log_monitor.cli
```

**Run the tests:**
```bash
cd log-monitoring-python
python3 run_tests.py
```

---

## Performance

- Each line is processed once → **O(n)**  
- Job lookup by PID/description → **O(1)** (dictionary)
- Overall complexity → **O(n)**

---

## Future Enhancements

- Integration tests for end-to-end CLI execution
- Configurable input/output paths via CLI arguments
