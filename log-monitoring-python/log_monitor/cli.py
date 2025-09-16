from pathlib import Path
from .parser import parse_lines
from .monitor import build_report

def main():
    # Determine root directory and input/output file paths
    root_dir = Path(__file__).resolve().parents[2]
    input_path = root_dir / "logs.log"
    output_path = root_dir / "output.log"

    with open(input_path) as f:
        entries = parse_lines(f)

    report = build_report(entries)

    # Filter only background job results
    background_results = [r for r in report.results if "job" in r.description]

    # Separate warnings and errors based on job duration
    warnings = [r for r in background_results if r.level() == "WARNING"]
    errors = [r for r in background_results if r.level() == "ERROR"]

    lines = []
    lines.append("---- Warnings ----")
    
    # Add warning jobs to output
    for r in warnings:
        secs = int(r.duration.total_seconds())
        lines.append(f"WARNING: {secs} (PID: {r.pid}) took {secs} seconds.")

    lines.append("\n---- Errors ----")
    
    # Add error jobs to output
    for r in errors:
        secs = int(r.duration.total_seconds())
        lines.append(f"ERROR: {secs} (PID: {r.pid}) took {secs} seconds.")

    output_text = "\n".join(lines)

    output_path.write_text(output_text, encoding="utf-8")

if __name__ == "__main__":
    main()
