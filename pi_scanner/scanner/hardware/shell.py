"""
Safe wrapper for running terminal commands from the app (e.g. libcamera-still,
a calibration CLI, a shell script you already trust).

Always call with a list of args, never a single string with shell=True -
that's what keeps this safe even if a value happens to come from a config
file or settings screen later.

    run_command(["libcamera-still", "-o", "/tmp/frame.jpg", "-t", "1000"])
"""

import logging
import subprocess

logger = logging.getLogger(__name__)


class ShellError(RuntimeError):
    pass


def run_command(args, timeout=30, check=True):
    """
    Run a command and return its stdout (stripped).

    args:    list of strings, e.g. ["libcamera-still", "-o", "out.jpg"]
    timeout: seconds before the command is killed
    check:   raise ShellError on non-zero exit if True
    """
    if isinstance(args, str):
        raise TypeError("Pass a list of args, not a raw string (avoids shell=True).")

    logger.info("Running command: %s", " ".join(args))
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=check,
        )
        if result.stderr:
            logger.debug("stderr from %s: %s", args[0], result.stderr.strip())
        return result.stdout.strip()
    except subprocess.CalledProcessError as exc:
        logger.error("Command failed (%s): %s", args[0], exc.stderr)
        raise ShellError(exc.stderr.strip() or str(exc)) from exc
    except subprocess.TimeoutExpired as exc:
        logger.error("Command timed out: %s", args[0])
        raise ShellError(f"'{args[0]}' timed out after {timeout}s") from exc
    except FileNotFoundError as exc:
        raise ShellError(f"Command not found: {args[0]}") from exc
