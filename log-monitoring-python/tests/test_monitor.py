import io
import unittest
from log_monitor.parser import parse_lines
from log_monitor.monitor import build_report

# Helper function to create a job report from log text
# Returns the first job result from the report
def make_job(log_text: str):
    entries = parse_lines(io.StringIO(log_text.strip()))
    report = build_report(entries)
    return report.results[0]

class TestJobs(unittest.TestCase):
    def test_duration_5_minutes(self):
        """Duration exactly 5 minutes"""
        job = make_job("11:00:00,background job a, START,1\n11:05:00,background job a, END,1")
        self.assertIsNone(job.level())

    def test_duration_10_minutes(self):
        """Duration exactly 10 minutes"""
        job = make_job("11:00:00,background job a, START,1\n11:10:00,background job a, END,1")
        self.assertEqual(job.level(), "WARNING")

    def test_duration_11_minutes(self):
        """Duration over 10 minutes"""
        job = make_job("11:00:00,background job a, START,1\n11:11:00,background job a, END,1")
        self.assertEqual(job.level(), "ERROR")

    def test_duration_7_minutes(self):
        """Duration between 5 and 10 minutes"""
        job = make_job("11:00:00,background job a, START,1\n11:07:00,background job a, END,1")
        self.assertEqual(job.level(), "WARNING")

    def test_duration_30_seconds(self):
        """Very short job (30 seconds)"""
        job = make_job("11:00:00,background job a, START,1\n11:00:30,background job a, END,1")
        self.assertIsNone(job.level())

    def test_two_jobs_different_pids(self):
        """Two different jobs"""
        entries = """11:00:00,background job a, START,1
11:01:00,background job a, END,1
11:02:00,background job b, START,2
11:03:00,background job b, END,2"""
        report = build_report(parse_lines(io.StringIO(entries)))
        self.assertEqual(len(report.results), 2)
        self.assertTrue(all(j.level() is None for j in report.results))

    def test_unmatched_start(self):
        """Job with START but no END"""
        entries = """11:00:00,background job a, START,1"""
        report = build_report(parse_lines(io.StringIO(entries)))
        self.assertEqual(len(report.results), 0)
        self.assertEqual(len(report.unmatched_starts), 1)

    def test_unmatched_end(self):
        """Job with END but no START"""
        entries = """11:00:00,background job a, END,1"""
        report = build_report(parse_lines(io.StringIO(entries)))
        self.assertEqual(len(report.results), 0)
        self.assertEqual(len(report.unmatched_ends), 1)

    def test_multiple_intervals_same_pid(self):
        """Same PID appearing twice with START/END pairs"""
        entries = """11:00:00,background job a, START,1
11:01:00,background job a, END,1
11:02:00,background job a, START,1
11:03:00,background job a, END,1"""
        report = build_report(parse_lines(io.StringIO(entries)))
        self.assertEqual(len(report.results), 2)
        self.assertTrue(all(j.level() is None for j in report.results))

    def test_ignore_scheduled_tasks(self):
        """Ignore scheduled tasks and count only jobs"""
        entries = """11:00:00,scheduled task x, START,10
11:02:00,scheduled task x, END,10
11:00:00,background job b, START,2
11:12:00,background job b, END,2"""
        report = build_report(parse_lines(io.StringIO(entries)))
        jobs = [j for j in report.results if "job" in j.description]
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].level(), "ERROR")
