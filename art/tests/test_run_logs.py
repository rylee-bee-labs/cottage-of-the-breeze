#!/usr/bin/env python3
"""Tests for the committed run logs under art/source/.

A run log is a transcript of the agent's own session, kept beside the sheets it
drew because it records how a batch was asked for and what came back. It is
also the one kind of file here that can carry the author's private machine
details: the absolute path of their home directory, and the Codex session id.
The repo is private today and may be distributed one day, so those two are
redacted in the committed logs and these tests keep them out.

Redaction is a substitution, not a cut: the log still reads as a transcript
(the banner, the prompt, the outputs), so the last test says so.

Pure text checks: no network, no Pillow, no image files.
"""
import re
import unittest
from pathlib import Path

ART_DIR = Path(__file__).resolve().parents[1]          # the art/ folder
SOURCE_DIR = ART_DIR / "source"                        # art/source/

# What the other tests loop over: every committed run log, whichever round it
# came from. A log that arrives in a later round is covered on arrival.
LOGS = tuple(sorted(SOURCE_DIR.rglob("*.log")))

# An absolute path into somebody's home directory. The home directory is the
# author's private machine layout: their user name, their checkout, their agent
# skills. `$HOME` says the same thing without the disclosure.
HOME_DIR = re.compile(r"/(?:home|Users|root)/[A-Za-z0-9._-]+")

# A Codex session id (a UUID). It identifies one private session of one
# person; it is never needed to read the log.
SESSION_ID = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


def line_of(text, pattern):
    """The 1-based number of the first line `pattern` matches, for the message."""
    for number, line in enumerate(text.splitlines(), start=1):
        if pattern.search(line):
            return number
    return 0


class RunLogTests(unittest.TestCase):
    maxDiff = None

    def test_there_are_logs_to_check(self):
        # A quiet guard on the loops below: if the folder ever empties, the
        # tests after this one would pass without checking anything.
        self.assertTrue(LOGS, "no run logs found under art/source/")

    def test_no_log_carries_an_absolute_home_path(self):
        for path in LOGS:
            with self.subTest(log=path.name, round=path.parent.name):
                text = read(path)
                found = HOME_DIR.findall(text)
                self.assertEqual(
                    found, [],
                    "%s leaks a home directory path; write $HOME instead "
                    "(first on line %d)"
                    % (path, line_of(text, HOME_DIR)))

    def test_no_log_carries_a_session_id(self):
        for path in LOGS:
            with self.subTest(log=path.name, round=path.parent.name):
                text = read(path)
                self.assertEqual(
                    SESSION_ID.findall(text), [],
                    "%s carries a session id; write <redacted> instead "
                    "(first on line %d)"
                    % (path, line_of(text, SESSION_ID)))

    def test_each_log_still_reads_as_a_transcript(self):
        # Redaction replaced the two details, it did not cut the log down: the
        # banner that says where the run happened is still there, with the
        # home directory written as $HOME.
        for path in LOGS:
            with self.subTest(log=path.name, round=path.parent.name):
                text = read(path)
                self.assertIn("session id:", text,
                              "%s: the session banner is gone" % path)
                self.assertIn("workdir: $HOME", text,
                              "%s: no $HOME workdir line in the banner" % path)


if __name__ == "__main__":
    unittest.main()