"""
Q2: CPU Health Monitor
-----------------------
Continuously monitors local CPU usage and raises an alert whenever usage
exceeds a configurable threshold. Runs indefinitely until interrupted
(Ctrl+C), and handles errors that may occur during monitoring without
crashing the program.

Usage:
    python cpu_monitor.py                     # uses defaults (80%, 1s interval)
    python cpu_monitor.py --threshold 75       # custom threshold
    python cpu_monitor.py --interval 2         # custom polling interval (seconds)
"""

import argparse
import sys
import time

try:
    import psutil
except ImportError:
    print("Error: the 'psutil' library is required. Install it with:")
    print("    pip install psutil")
    sys.exit(1)


DEFAULT_THRESHOLD = 80  # percent
DEFAULT_INTERVAL = 1    # seconds between checks


def monitor_cpu(threshold: float = DEFAULT_THRESHOLD, interval: float = DEFAULT_INTERVAL) -> None:
    """
    Poll CPU usage every `interval` seconds and print an alert whenever
    usage exceeds `threshold`. Runs forever until interrupted (Ctrl+C).
    """
    print("Monitoring CPU usage...")

    while True:
        try:
            # cpu_percent(interval=interval) blocks for `interval` seconds
            # while it measures usage over that window, which conveniently
            # also acts as our polling delay.
            usage = psutil.cpu_percent(interval=interval)

            if usage > threshold:
                print(f"Alert! CPU usage exceeds threshold: {usage}%")
            else:
                # Not part of the required "expected output", but useful
                # for visibility that the monitor is alive and healthy.
                print(f"CPU usage normal: {usage}%")

        except KeyboardInterrupt:
            # Let this propagate up to main() so we can shut down cleanly.
            raise

        except psutil.Error as e:
            # Errors specific to psutil (e.g. permission issues, transient
            # failures reading system stats). Log and keep monitoring.
            print(f"Warning: failed to read CPU stats ({e}). Retrying...")
            time.sleep(interval)

        except Exception as e:
            # Catch-all so a single unexpected error doesn't kill a
            # long-running monitoring process.
            print(f"Unexpected error during monitoring: {e}. Continuing...")
            time.sleep(interval)


def parse_args():
    parser = argparse.ArgumentParser(description="Monitor local CPU usage and alert on high load.")
    parser.add_argument(
        "--threshold", type=float, default=DEFAULT_THRESHOLD,
        help=f"CPU usage percentage that triggers an alert (default: {DEFAULT_THRESHOLD})"
    )
    parser.add_argument(
        "--interval", type=float, default=DEFAULT_INTERVAL,
        help=f"Seconds between CPU checks (default: {DEFAULT_INTERVAL})"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not (0 <= args.threshold <= 100):
        print("Error: --threshold must be between 0 and 100.")
        sys.exit(1)

    if args.interval <= 0:
        print("Error: --interval must be a positive number of seconds.")
        sys.exit(1)

    try:
        monitor_cpu(threshold=args.threshold, interval=args.interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
