#!/usr/bin/env python3
"""Pick the funniest one-line sick-day excuse for the make.fun bounty.

A shortlist of hand-written excuses is scored on five craft axes:
whether a manager could half believe it, whether the image feels
new, whether the joke lands late, whether it reads like a genuine
message to a boss, and whether every word earns its keep. The
top scorer is written to the entry file and printed; ties break
toward the shorter line, so the result is fully deterministic.
"""

import hashlib
import os
import sys

CHAR_LIMIT = 199
ENTRY_PATH = "/output/entry.txt"
EXIT_OK = 0
WINNER_DIGEST = "f5460444d13186f3ce83cd18bd6dd0f1d0e7cce674cac19068206f0f11748b7f"

# The winning line, split into fragments so the wording stays exact
# while the source layout is free to change.
WINNER_BITS = (
    "My dentist pulled a tooth yesterday ",
    "and now my cheek looks like a hamster storing nuts for winter, ",
    "so I'm staying home until my face matches my ID photo again.",
)
WINNER = "".join(WINNER_BITS)

# Each draft carries five scores in the order: believable, original,
# late punch, true voice, economical. The winner must outscore the rest.
DRAFTS = [
    {"line": WINNER, "scores": (5, 5, 5, 5, 4)},
    {
        "line": "I woke up with my jaw swollen shut after the dentist pulled a molar, so today I am on soup and ice packs until I can open my mouth properly again.",
        "scores": (5, 4, 3, 5, 4),
    },
    {
        "line": "The eye drops the doctor gave me blur everything past arm's length, so I'm staying home until the world comes back into focus.",
        "scores": (5, 4, 4, 4, 4),
    },
    {
        "line": "I sliced my thumb chopping onions and the bandage keeps slipping off, so I'm taking today to stop bleeding on the keyboard.",
        "scores": (4, 4, 4, 5, 4),
    },
    {
        "line": "My back locked up reaching for a cereal box and now I walk like a folding chair, so I'm staying flat until it unfolds.",
        "scores": (4, 5, 4, 4, 4),
    },
    {
        "line": "The allergy tablets knocked me out cold for fourteen hours and I woke up on the kitchen floor, so I'm calling in until I can stay upright.",
        "scores": (4, 4, 3, 4, 4),
    }, ]


def add_scores(draft):
    """Total the five craft scores of one draft."""
    marks = draft["scores"]
    if len(marks) != 5:
        raise ValueError("a draft must carry exactly five scores")
    return sum(marks)


def pick_best(drafts):
    """Return the line of the best-scoring draft.

    Ranking is by total first and by brevity second, so a shorter
    line only wins when the totals match exactly.
    """
    champion = None
    champion_key = None
    for draft in drafts:
        key = (add_scores(draft), -len(draft["line"]))
        if champion_key is None or key > champion_key:
            champion_key = key
            champion = draft["line"]
    if champion is None:
        raise ValueError("draft list came up empty")
    return champion


def digest_of(line):
    """SHA-256 hex digest of a single line, UTF-8 encoded."""
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


def check_line(line):
    """Reject any line the brief would not accept.

    One non-empty line, no line breaks, no longer than CHAR_LIMIT.
    Anything failing here is a bug in the shortlist, not an excuse.
    """
    stripped = line.strip()
    if not stripped:
        raise ValueError("winning line is empty")
    if line != stripped:
        raise ValueError("winning line has stray leading or trailing space")
    if any(ch in line for ch in ("\n", "\r", "\t")):
        raise ValueError("winning line contains a line break or a tab")
    if len(line) > CHAR_LIMIT:
        raise ValueError("winning line runs %d chars, limit is %d" % (len(line), CHAR_LIMIT))


def save_line(line):
    """Write the line to the entry file and verify what landed.

    The file is written, made world-readable, read back and hashed
    again, so the bytes on disk are proven to be the chosen bytes.
    """
    folder = os.path.dirname(ENTRY_PATH)
    os.makedirs(folder, exist_ok=True)
    with open(ENTRY_PATH, "w", encoding="utf-8") as handle:
        handle.write(line)
    os.chmod(ENTRY_PATH, 0o644)
    with open(ENTRY_PATH, "r", encoding="utf-8") as handle:
        stored = handle.read()
    if stored != line:
        raise ValueError("entry file content drifted from the chosen line")
    if digest_of(stored) != WINNER_DIGEST:
        raise ValueError("entry file digest drifted from the recorded value")
    return ENTRY_PATH


def entrypoint():
    """Score the drafts, verify the winner, publish it, print it."""
    winner = pick_best(DRAFTS)
    check_line(winner)
    if digest_of(winner) != WINNER_DIGEST:
        raise ValueError("chosen line digest drifted from the recorded value")
    save_line(winner)
    print(winner)
    return EXIT_OK


_LAUNCHED_AS_SCRIPT = __name__ == "__main__"
if _LAUNCHED_AS_SCRIPT:
    sys.exit(entrypoint())
