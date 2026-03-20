# resume_parser.py  v4.2
# ─────────────────────────────────────────────────────────────────────────────
# Lightweight metadata extraction from plain-text resume and JD strings.
#
# v4.2 fixes:
#   [1] candidate_name() now handles ALL CAPS names ("ASHWATH RANJITH")
#       by title-casing the line before pattern matching, then returning
#       the title-cased version. The original all-caps form is not useful
#       for display.
#   [2] candidate_name() checks more lines (8 instead of 5) since some
#       resumes have a header line before the name.
#   [3] target_role() strips emoji and unicode characters from lines before
#       checking for role labels, so "🎯 Job Title: X" is parsed correctly.
# ─────────────────────────────────────────────────────────────────────────────

import re


def _log(level: str, fn: str, msg: str) -> None:
    print(f"[resume_parser:{fn}] {level:<5}  {msg}")

def _info(fn, msg):  _log("INFO",  fn, msg)
def _warn(fn, msg):  _log("WARN",  fn, msg)
def _debug(fn, msg): _log("DEBUG", fn, msg)


def _strip_non_ascii(s: str) -> str:
    """Remove emoji and non-ASCII characters that can break regex matching."""
    return re.sub(r"[^\x00-\x7F]+", "", s).strip()


def candidate_name(text: str) -> str:
    """
    Extract candidate name from the top of a resume.

    Handles:
      - Title case:  "Ashwath Ranjith"
      - ALL CAPS:    "ASHWATH RANJITH"  → returned as "Ashwath Ranjith"
      - Mixed:       "ASHWATH Ranjith"  → returned as "Ashwath Ranjith"

    Skips lines that look like email addresses, phone numbers, or URLs.
    Falls back to 'Candidate' if nothing found.
    """
    fn    = "candidate_name"
    lines = text.strip().split("\n")[:8]

    for line in lines:
        line = line.strip()
        _debug(fn, f"Checking: '{line[:60]}'")

        # Skip obvious non-name lines
        if not line:
            continue
        if any(c in line for c in ["@", "http", "github", "linkedin", "+91", "+1", "."]):
            _debug(fn, "  → skipped (looks like contact info)")
            continue
        if len(line) < 4 or len(line) > 50:
            continue

        # Normalise to title case for pattern matching
        normalised = line.title()

        # Must look like "Firstname Lastname":
        #   - 2-4 words (names are not sentences)
        #   - each word is 2+ chars (filters "No X Y" style matches)
        #   - no digits
        # Reject lines that are all-lowercase in the original —
        # a real name always has at least one capital letter.
        if not any(w[0].isupper() for w in line.split() if w):
            _debug(fn, "  → skipped (no uppercase in original)")
            continue
        words = normalised.split()
        if (2 <= len(words) <= 4
                and all(len(w) >= 2 for w in words)
                and re.match(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)+$", normalised)
                and not any(c.isdigit() for c in normalised)):
            _info(fn, f"Detected name: '{normalised}' (original: '{line}')")
            return normalised

    _warn(fn, f"No name found in first 8 lines — returning 'Candidate'")
    _warn(fn, f"Lines checked: {[l.strip()[:40] for l in lines]}")
    return "Candidate"


def target_role(jd: str) -> str:
    """
    Extract the target role from a JD.

    Handles:
      - Explicit labels:  "Job Title: UI/UX Designer"
      - With emoji:       "🎯 Job Title: UI/UX Designer"
      - First short capitalised line as fallback

    Falls back to 'Target Role' if nothing found.
    """
    fn    = "target_role"
    lines = jd.strip().split("\n")[:10]

    for line in lines:
        line    = line.strip()
        cleaned = _strip_non_ascii(line)  # remove emoji first
        _debug(fn, f"Checking: '{cleaned[:60]}'")

        if not cleaned:
            continue

        # Look for explicit label pattern — "Job Title: X", "Role: X", etc.
        if any(k in cleaned.lower() for k in ["job title:", "title:", "role:", "position:"]):
            parts = cleaned.split(":", 1)
            if len(parts) > 1 and parts[1].strip():
                role = parts[1].strip()
                _info(fn, f"Detected role via label: '{role}'")
                return role

        # Fallback: first short capitalised line (likely the role header)
        if 8 < len(cleaned) < 60 and re.match(r"^[A-Z]", cleaned):
            _info(fn, f"Detected role via first capitalised line: '{cleaned}'")
            return cleaned

    _warn(fn, "No role found — returning 'Target Role'")
    _warn(fn, f"Lines checked: {[l.strip()[:40] for l in lines]}")
    return "Target Role"