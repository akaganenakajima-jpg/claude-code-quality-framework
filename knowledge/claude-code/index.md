# claude-code/ — Claude Code 高度機能 索引

Claude Code 自体の機能を使って作業を「速く・安全に・自動で」回すための運用知識。
ドメイン専門知識（ipa/stats/ds 等）とは別軸で、**道具としての Claude Code を使いこなす**ためのリファレンス。

> **最終検証日: 2026-06-16** ／ 出典: 公式ドキュメント `https://code.claude.com/docs`
> Claude Code の機能は更新が速い。**機能名・コマンド名・挙動は使用前に必ず公式ドキュメントで再確認すること**（このファイルはスナップショット）。
> `/cc-features` コマンドは本ファイルを正本として参照する。

## ファイル一覧

| ファイル | 扱う領域 |
|---|---|
| `orchestration.md` | サブエージェント・並列実行・Workflow・Agent View・Worktrees |
| `automation.md` | `/loop`・Routines(`/schedule`)・Desktopタスク・headless・Hooks |
| `tooling.md` | Plugins/Marketplace・Skills・Memory・Checkpoints・Fast mode・出力スタイル・MCP・Sessions |

## 課題→機能 逆引き

| やりたいこと | 使う機能 | 参照 |
|---|---|---|
| 重い調査で会話を圧迫したくない | サブエージェント | `orchestration.md` §1 |
| 独立した調査を同時に進めたい | 並列エージェント | `orchestration.md` §2 |
| 数十〜数百ファイルを一括変換・監査したい | Workflow（大規模オーケストレーション） | `orchestration.md` §3 |
| 複数セッションを並行管理したい | Agent View / バックグラウンドエージェント | `orchestration.md` §4 |
| 壊しても安全な隔離環境で実験したい | Worktrees | `orchestration.md` §5 |
| 一定間隔で同じ作業を繰り返したい（セッション中） | `/loop` | `automation.md` §1 |
| 条件達成まで粘り強く継続させたい | `/goal` | `automation.md` §2 |
| マシンOFFでも定期実行したい（クラウド） | Routines / `/schedule` | `automation.md` §3 |
| ローカルで定期実行したい（短間隔） | Desktop スケジュールタスク | `automation.md` §4 |
| CI/CDやスクリプトから自動実行したい | headless mode (`claude -p`) | `automation.md` §5 |
| 特定イベントで自動チェック・整形したい | Hooks | `automation.md` §6 |
| 機能をパッケージ化・共有・導入したい | Plugins / Marketplace | `tooling.md` §1 |
| 再利用ワークフローを `/名前` で呼びたい | Skills | `tooling.md` §2 |
| プロジェクト固有ルールを永続化したい | Memory (CLAUDE.md / rules / auto memory) | `tooling.md` §3 |
| 編集を巻き戻したい・誤りから復旧したい | Checkpoints / `/rewind` | `tooling.md` §4 |
| 反復作業を高速に回したい | Fast mode (`/fast`) | `tooling.md` §5 |
| 外部ツール・DB・APIを接続したい | MCP | `tooling.md` §7 |

## 品質フレームワークとの接続

- 🔴 最高リスク作業（DB構造変更・定期実行変更・本番公開）→ **Worktrees** で隔離（`quality/risks.md` の対策レベルと連動）。
- 大改修の前に「戻れる状態」を確保 → **Checkpoints** + git コミット（`practices/git-workflow.md` §3）。
- 調べることが3つ以上で並行可能 → **並列サブエージェント**（CLAUDE.md「サブエージェントの使い分け」）。
- 定期的な品質チェック・監視の自動化 → **Hooks / Routines**（`quality/metrics.md` のKPI記録など）。

## 出典

- Overview: https://code.claude.com/docs
- Subagents: https://code.claude.com/docs/en/sub-agents
- Workflows: https://code.claude.com/docs/en/workflows
- Agent View: https://code.claude.com/docs/en/agent-view
- Worktrees: https://code.claude.com/docs/en/worktrees
- Scheduled tasks (`/loop`): https://code.claude.com/docs/en/scheduled-tasks
- Routines: https://code.claude.com/docs/en/routines
- Hooks: https://code.claude.com/docs/en/hooks-guide
- Plugins: https://code.claude.com/docs/en/plugins
- Skills: https://code.claude.com/docs/en/skills
- Memory: https://code.claude.com/docs/en/memory
- Checkpointing: https://code.claude.com/docs/en/checkpointing
- MCP: https://code.claude.com/docs/en/mcp
