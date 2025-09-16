# log_monitor/cli.py
import argparse
from .parser import parse_lines
from .monitor import build_report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to logs.log")
    args = parser.parse_args()

    with open(args.path) as f:
        entries = parse_lines(f)

    report = build_report(entries)

    warnings = [r for r in report.results if r.level() == "WARNING"]
    errors = [r for r in report.results if r.level() == "ERROR"]

    warnings.sort(key=lambda r: r.start)
    errors.sort(key=lambda r: r.start)

    print("---- Warnings ----")
    for r in warnings:
        secs = int(r.duration.total_seconds())
        print(f"WARNING: {secs} (PID: {r.pid}) took {secs} seconds.")

    print("\n---- Errors ----")
    for r in errors:
        secs = int(r.duration.total_seconds())
        print(f"ERROR: {secs} (PID: {r.pid}) took {secs} seconds.")

if __name__ == "__main__":
    main()
