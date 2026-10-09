#!/usr/bin/env python3
"""PreToolUse guard for the work loop (docs/ai-workflow.md §1 + §6).

Wired from `.claude/settings.json`. Reads the hook JSON on stdin and prints a `permissionDecision`
(deny / ask) when a rule fires; prints nothing (= allow) otherwise.

Rules:
  - `git push` to master, or any forced push   -> DENY  (§6: never push master; branch + PR)
  - `git commit`                               -> ASK   (§6: commit only when the maintainer asked)
  - Edit/Write of any file under vendor/       -> DENY  (§1.1: never edit vendor/)
Hook contract: https://code.claude.com/docs/en/hooks (PreToolUse, permissionDecision).
"""
import json
import re
import sys


def decide(decision: str, reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def main() -> None:
    try:
        hook = json.load(sys.stdin)
    except Exception:
        return  # malformed input: allow, never wedge the session
    tool = hook.get("tool_name", "") or ""
    tool_input = hook.get("tool_input", {}) or {}

    if tool in ("Bash", "PowerShell"):
        cmd = tool_input.get("command", "") or ""
        if re.search(r"\bgit\s+push\b", cmd):
            if re.search(r"(\s|:)master(\s|$)", cmd) or re.search(r"\s(--force\S*|-f)\b", cmd):
                decide("deny", "never push master or force-push (ai-workflow §6): branch + PR, the maintainer merges")
        if re.search(r"\bgit\s+commit\b", cmd):
            decide("ask", "commit only when the maintainer asked (ai-workflow §6) — did they ask for THIS commit?")
        return

    if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        path = str(tool_input.get("file_path", "") or tool_input.get("notebook_path", "") or "").replace("\\", "/")
        if re.search(r"(^|/)vendor/", path):
            decide("deny", "never edit vendor/ (ai-workflow §1.1, dev-boundaries.md): extend from our app instead")


if __name__ == "__main__":
    main()
