import io
import unittest
from log_monitor.parser import parse_lines
from log_monitor.monitor import build_report

class TestLogMonitor(unittest.TestCase):
    def test_error_job(self):
        data = """11:00:00,background job abc, START,111
11:10:30,background job abc, END,111
"""
        entries = parse_lines(io.StringIO(data))
        report = build_report(entries)

        self.assertEqual(len(report.results), 1)
        job = report.results[0]
        self.assertEqual(int(job.duration.total_seconds()), 630)
        self.assertEqual(job.level(), "ERROR")

if __name__ == "__main__":
    unittest.main()
