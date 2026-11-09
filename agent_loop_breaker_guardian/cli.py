"""CLI for agent-loop-breaker-guardian."""
import sys
import argparse
from .guardian import LoopBreakerGuardian


def main():
    parser = argparse.ArgumentParser(description="Agent Loop Breaker Guardian CLI")
    parser.add_argument("--demo", action="store_true", help="Run loop breaker simulation")
    args = parser.parse_args()

    if args.demo:
        guardian = LoopBreakerGuardian()
        # Simulate oscillating agent edit
        print("Simulating oscillating edits...")
        guardian.record_step("edit_file", "import typing as t")
        guardian.record_step("edit_file", "from typing import List")
        guardian.record_step("edit_file", "import typing as t")
        res = guardian.record_step("edit_file", "from typing import List")

        print(f"Guardian Evaluation: Loop Detected = {res.loop_detected}")
        if res.loop_detected:
            print(f"  Period: {res.period} | Reason: {res.message}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
