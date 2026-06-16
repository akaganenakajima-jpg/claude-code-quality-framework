# /cc-features — Claude Code 高度機能の案内

Claude Code 自体の機能（オーケストレーション・自動化・周辺ツール）を、いま手元の課題に合わせて提案する。

## 手順

1. `~/.claude/knowledge/claude-code/index.md` を Read し、逆引き表から課題に合う機能を特定する。
2. 必要に応じて該当トピック（`orchestration.md` / `automation.md` / `tooling.md`）を Read して詳細を確認する。
3. **記憶に頼らず**、機能名・コマンド名・挙動を公式ドキュメント（`https://code.claude.com/docs`）または `claude-code-guide` エージェントで裏取りしてから案内する。
4. 「どの機能を・なぜ・どう呼び出すか」を、現在の作業文脈に紐づけて具体的に提示する。

## 原則

- このコマンドは機能一覧を持たない。**正本は `knowledge/claude-code/index.md`**（単一の情報源）。
- index.md 冒頭の「最終検証日」が古い場合は、公式ドキュメントとの差分があり得る旨を添える。
- 🔴 最高リスク作業には Worktrees、大規模変換には Workflow、定期実行には Routines/`/loop` を優先的に検討する（`quality/risks.md` と連動）。

$ARGUMENTS に「やりたいこと」がある場合はそれを分析対象にする。
ない場合は現在のコンテキストから課題を推定する。
