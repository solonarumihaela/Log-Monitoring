from pathlib import Path
from .parser import parse_lines
from .monitor import build_report

# Main function for CLI execution
# Reads log file, processes jobs, and writes warnings/errors to output

def main():
    root_dir = Path(__file__).resolve().parents[2] 
    input_path = root_dir / "logs.log" 
    output_path = root_dir / "output.log"

    entries = parse_lines(open(input_path))
    report = build_report(entries)

    # Filter only background jobs (ignore scheduled tasks)
    jobs = [r for r in report.results if "job" in r.description]
    
    # Split jobs into warnings and errors based on duration
    warnings = [r for r in jobs if r.level() == "WARNING"]
    errors = [r for r in jobs if r.level() == "ERROR"]

    lines = ["---- Warnings ----"] + [
        f"WARNING: {int(r.duration.total_seconds())} (PID: {r.pid}) took {int(r.duration.total_seconds())} seconds."
        for r in warnings
    ] + ["\n---- Errors ----"] + [
        f"ERROR: {int(r.duration.total_seconds())} (PID: {r.pid}) took {int(r.duration.total_seconds())} seconds."
        for r in errors
    ]

    output_path.write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    main()
