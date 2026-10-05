"""Make repositories' labels match labels/labels.json of Zhengjunliang/.github.

One line, the same in Git Bash and cmd.exe, from any directory, gh logged in:

  gh api -H "Accept: application/vnd.github.raw" repos/Zhengjunliang/.github/contents/labels/sync.py | python - OWNER/REPO [OWNER/REPO ...] [--dry-run]

Each repository gets the manifest's "default" labels plus its own list under
"repos". A missing label is created and a different one edited; a label named
in an entry's "aliases" is renamed to it, so whatever carries it keeps it.
Every other label is deleted. The labels are then read back and compared with
the manifest, and open issues without exactly one "type: " label are listed;
either difference exits non-zero. --dry-run prints the steps and changes
nothing. Keep this file ASCII: cmd.exe pipes it in the console's code page.
"""

from __future__ import annotations

import json
import subprocess
import sys

SOURCE = "repos/Zhengjunliang/.github/contents/labels/labels.json"
RAW = "Accept: application/vnd.github.raw"


def gh(*args: str) -> str:
    done = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    if done.returncode:
        sys.exit(f"gh {' '.join(args)} failed:\n{done.stderr.strip()}")
    return done.stdout


def present(repo: str) -> dict[str, dict]:
    rows = json.loads(gh("label", "list", "-R", repo, "-L", "1000", "--json", "name,color,description"))
    return {row["name"].lower(): row for row in rows}


def plan(labels: list[dict], have: dict[str, dict]) -> list[list[str]]:
    steps: list[list[str]] = []
    kept: set[str] = set()
    for label in labels:
        name, color, text = label["name"], label["color"].lower(), label["description"]
        aliases = [a.lower() for a in label.get("aliases", []) if a.lower() in have]
        if name.lower() in have and aliases:
            sys.exit(f'"{name}" and its alias "{aliases[0]}" both exist: move the alias\'s issues, then run again')
        key = name.lower() if name.lower() in have else (aliases[0] if aliases else None)
        if key is None:
            steps.append(["create", name, "--color", color, "--description", text])
            continue
        kept.add(key)
        row = have[key]
        if (row["name"], row["color"].lower(), row["description"]) != (name, color, text):
            steps.append(["edit", row["name"], "--name", name, "--color", color, "--description", text])
    steps += [["delete", row["name"], "--yes"] for key, row in have.items() if key not in kept]
    return steps


def untyped(repo: str) -> list[int]:
    rows = json.loads(gh("issue", "list", "-R", repo, "--state", "open", "-L", "1000", "--json", "number,labels"))
    return [
        row["number"]
        for row in rows
        if sum(label["name"].startswith("type: ") for label in row["labels"]) != 1
    ]


def main(argv: list[str]) -> None:
    dry = "--dry-run" in argv
    repos = [arg for arg in argv if arg != "--dry-run"]
    if not repos:
        sys.exit(__doc__)
    manifest = json.loads(gh("api", "-H", RAW, SOURCE))
    failed = False
    for repo in repos:
        labels = manifest["default"] + manifest["repos"].get(repo, [])
        for step in plan(labels, present(repo)):
            print(repo, "gh label", " ".join(f'"{s}"' if " " in s or not s else s for s in step))
            if not dry:
                gh("label", *step, "-R", repo)
        if not dry:
            want = {(label["name"], label["color"].lower(), label["description"]) for label in labels}
            have = {(row["name"], row["color"].lower(), row["description"]) for row in present(repo).values()}
            if have != want:
                failed = True
                print(repo, "differs from the manifest:", sorted(have ^ want))
        if bad := untyped(repo):
            failed = True
            print(repo, "open issues without exactly one type label:", " ".join(f"#{n}" for n in bad))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
