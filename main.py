# The Funniest Sick-Day Excuse — make.fun bounty
# u-zeroxfive-the-funniest-sick-day-excuse-37423a36
#
# The program writes one sick-day excuse, a single line under 200
# characters and nothing else, to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a reason to call in sick that a boss might half believe and a
#      coworker would laugh at
#   2. turns on a fresh idea rather than a worn excuse about a fever,
#      a dog or a dead grandmother
#   3. lands on one read, with the twist or the funniest word arriving
#      near the end
#   4. sounds like a real person typing a message, not a joke built
#      for a contest
#   5. wastes no words: every part of the line is doing work
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: believable 10, fresh 10, twist 10, real voice 10,
    #   tight 9 = 49. Dental swelling is a real, half-believable
    #   reason to stay home; the hamster image is fresh, and the
    #   punch lands near the end on the ID photo.
    ("My dentist pulled a tooth yesterday and now my cheek looks like "
     "a hamster storing nuts for winter, so I'm staying home until my "
     "face matches my ID photo again.",
     49),
    # score: believable 10, fresh 9, twist 9, real voice 9,
    #   tight 9 = 46. Dilated pupils are a genuine same-day reason
    #   to miss work; the watercolour image is fresh and the twist
    #   arrives near the end.
    ("The eye doctor dilated my pupils and now the whole world looks "
     "like a watercolour left out in the rain, so I'm taking today off "
     "until my eyes agree to focus again.",
     46),
    # score: believable 9, fresh 9, twist 9, real voice 9,
    #   tight 9 = 45. A migraine is half-believable and the spotlight
    #   image is vivid; the interpretive-dance turn lands near the end.
    ("I have a migraine so bad the light from my phone feels like a "
     "spotlight, so I'm taking today off before I start answering "
     "emails in interpretive dance.",
     45),
    # score: believable 10, fresh 8, twist 9, real voice 9,
    #   tight 8 = 44. Throwing your back out is believable and the
    #   crawling-into-the-office image is funny, but back injuries
    #   are a well-worn excuse.
    ("I threw my back out reaching for the remote, which is "
     "embarrassing, but the doctor says lying flat today beats "
     "crawling into the office tomorrow.",
     44),
    # score: believable 9, fresh 8, twist 8, real voice 9,
    #   tight 9 = 43. Food poisoning is believable and the
    #   first-name-basis line is funny, but it is a familiar excuse.
    ("Last night's leftovers have me on a first-name basis with my "
     "bathroom, so I need today to recover and formally apologise to "
     "the fridge.",
     43),
    # score: believable 9, fresh 8, twist 8, real voice 8,
    #   tight 9 = 42. A twisted ankle is believable and the ice pack
    #   as boss is a nice turn, but the setup is ordinary.
    ("I slipped on the stairs this morning and twisted my ankle, "
     "which is fine, but the ice pack says I have to stay put, and "
     "honestly the ice pack is the boss now.",
     42),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text, and
# the brief asks for under 200 characters, so every candidate is kept
# below 200.
MAX_CHARS = 199


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import hashlib
    import os
    # SHA-256 self-check: the chosen line must hash to the value recorded
    # when the candidates were drafted, so a silent edit to the winning
    # text (or to the file on disk) is caught instead of shipped.
    expected_sha256 = (
        "f5460444d13186f3ce83cd18bd6dd0f1d0e7cce674cac19068206f0f11748b7f"
    )
    actual_sha256 = hashlib.sha256(line.encode("utf-8")).hexdigest()
    assert actual_sha256 == expected_sha256, \
        f"chosen line hash changed: {actual_sha256}"
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what was actually written: the gate reads this file, not stdout.
    # The scorer collects outputs as another user, so the file must be
    # readable by everyone (mode 0644), not just by the writer.
    os.chmod("/output/entry.txt", 0o644)
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt differs from the chosen line"
    assert 1 <= len(written.strip()) <= MAX_CHARS, \
        "entry.txt outside the gate"
    assert written.strip(), "entry.txt is blank"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    # Re-hash what is on disk: the file the gate reads must match the
    # chosen line byte for byte, not just in length.
    written_sha256 = hashlib.sha256(written.encode("utf-8")).hexdigest()
    assert written_sha256 == expected_sha256, \
        f"entry.txt hash changed on disk: {written_sha256}"
    print(line)


if __name__ == "__main__":
    main()
