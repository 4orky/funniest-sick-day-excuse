"""Choose the strongest sick-day excuse and write it out.

Six one-line excuses were drafted for the brief and graded on five
craft marks: how believable the reason sounds, how fresh the idea
is, how late the twist lands, how much it sounds like a real text
to a manager, and how little it wastes. The highest total wins and
a tie goes to the shorter line, so the outcome never depends on
ordering or chance. The winner goes to /output/entry.txt and to
standard output, byte for byte the same on every run.
"""

from hashlib import sha256
from pathlib import Path

CEILING = 199
OUT_DIR = "/output"
ENTRY_NAME = "entry.txt"
EXPECTED_HEX = "f5460444d13186f3ce83cd18bd6dd0f1d0e7cce674cac19068206f0f11748b7f"

ENTRIES = [
    {
        # A pulled tooth is a real same-day reason; the hamster image
        # is new, and the ID-photo closer lands a second laugh last.
        "text": "My dentist pulled a tooth yesterday and now my cheek looks like a hamster storing nuts for winter, so I'm staying home until my face matches my ID photo again.",
        "marks": {"believable": 5, "fresh": 5, "twist": 5, "voice": 5, "tight": 4},
    },
    {
        # A throbbing wisdom tooth is believable, but the closer is a
        # shrug rather than a second laugh, so it grades lower.
        "text": "My wisdom tooth started throbbing at 3 a.m. and now I can only chew on one side, so I'm taking today to ice it before it starts making decisions for me.",
        "marks": {"believable": 5, "fresh": 4, "twist": 4, "voice": 5, "tight": 4},
    },
    {
        # Knock-out cough syrup is a solid reason, yet the spinning
        # room is a familiar image and the ending trails off.
        "text": "The pharmacist gave me cough syrup that knocks me out for twelve hours, so I'm calling in today and will answer emails once the room stops spinning.",
        "marks": {"believable": 5, "fresh": 4, "twist": 3, "voice": 5, "tight": 4},
    },
    {
        # A neck that only turns left is a fresh picture, but the joke
        # spends its twist early and then explains itself.
        "text": "I woke up with a stiff neck that only turns left, so I'm staying home today — I can't nod yes to anything until it turns right again.",
        "marks": {"believable": 4, "fresh": 5, "twist": 4, "voice": 4, "tight": 4},
    },
    {
        # A torn contact lens is believable and visual, though the
        # spare-pair ending is flat and the voice stays formal.
        "text": "My contact lens tore this morning and now I'm reading the world through one blurry eye, so I'm taking the day until the spare pair arrives.",
        "marks": {"believable": 5, "fresh": 4, "twist": 3, "voice": 4, "tight": 4},
    },
    {
        # A stomach complaint at a night market is vivid, but the
        # peace-treaty closer tries too hard to be clever.
        "text": "I ate something suspicious at the night market and my stomach has filed a formal complaint, so I need today to negotiate a peace treaty with it.",
        "marks": {"believable": 4, "fresh": 4, "twist": 4, "voice": 4, "tight": 3},
    },
]


def total_marks(entry):
    """Add up one entry's five craft marks."""
    return sum(entry["marks"].values())


def choose(entries):
    """Return the text of the highest-graded entry.

    The ranking key puts the mark total first and the length second,
    so a shorter line only wins when the totals are tied.
    """
    best_text = None
    best_rank = None
    for entry in entries:
        rank = (total_marks(entry), -len(entry["text"]))
        if best_rank is None or rank > best_rank:
            best_rank = rank
            best_text = entry["text"]
    if best_text is None:
        raise ValueError("no entries to choose from")
    return best_text


def gate_ok(text):
    """Refuse any line the brief would not accept.

    The gate takes one line of non-blank text between 1 and CEILING
    characters; anything else is a bug, not an excuse.
    """
    if not text.strip():
        raise ValueError("chosen line is blank")
    if "\n" in text or "\r" in text:
        raise ValueError("chosen line spans more than one line")
    if len(text) < 1 or len(text) > CEILING:
        raise ValueError(f"chosen line is {len(text)} chars, gate is 1..{CEILING}")
    return True


def fingerprint(text):
    """Return the SHA-256 hex digest of one line."""
    return sha256(text.encode("utf-8")).hexdigest()


def publish(text):
    """Write the line to the entry file and prove it landed.

    The file is written, made world-readable, read back, and hashed
    again, so the bytes the gate reads are the bytes chosen here.
    """
    target = Path(OUT_DIR) / ENTRY_NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    target.chmod(0o644)
    back = target.read_text(encoding="utf-8")
    if back != text:
        raise ValueError("entry file differs from the chosen line")
    if fingerprint(back) != EXPECTED_HEX:
        raise ValueError("entry file hash differs from the recorded value")
    return target


def run():
    """Pick, check, publish and print the winning excuse."""
    chosen = choose(ENTRIES)
    gate_ok(chosen)
    if fingerprint(chosen) != EXPECTED_HEX:
        raise ValueError("chosen line hash differs from the recorded value")
    publish(chosen)
    print(chosen)
    return 0


# Running this file is the only entry point; importing it stays quiet.
if __name__ == "__main__": raise SystemExit(run())
