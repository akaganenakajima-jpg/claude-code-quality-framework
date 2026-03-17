#!/usr/bin/env python3
"""
process-gate.py — コミット前リスク判定リマインダー
PreToolUse / Bash hook: git commit を検知してリスクレベルを推定表示する。
ブロックしない（常に exit 0）。リマインダーのみ。
"""
import sys
import io
import json
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")
    if "git commit" not in command:
        sys.exit(0)

    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--stat"],
            capture_output=True, text=True, timeout=5
        )
        stat = result.stdout.strip()
    except Exception:
        sys.exit(0)

    if not stat:
        sys.exit(0)

    lines = stat.split("\n")
    summary = lines[-1] if lines else ""

    files_changed = 0
    insertions = 0
    deletions = 0
    for part in summary.split(","):
        part = part.strip()
        if "file" in part:
            files_changed = int(part.split()[0])
        elif "insertion" in part:
            insertions = int(part.split()[0])
        elif "deletion" in part:
            deletions = int(part.split()[0])

    total_changes = insertions + deletions

    if total_changes <= 20 and files_changed <= 2:
        level = "🟢 低リスク"
    elif total_changes <= 100 and files_changed <= 5:
        level = "🟡 中リスク"
    elif total_changes <= 300 or files_changed <= 10:
        level = "🟠 高リスク"
    else:
        level = "🔴 最高リスク"

    print(
        f"\n⚙️ リスク判定リマインダー: {level}\n"
        f"   {files_changed}ファイル / +{insertions} -{deletions} 行\n"
        f"   → リスクに応じた品質ゲートを確認してください（quality/risks.md）\n",
        file=sys.stderr
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
