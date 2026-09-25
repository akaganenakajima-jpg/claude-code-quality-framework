# claude-code/ — Claude Code 高度機能・運用 索引

Claude Code 自体の機能を使って作業を「速く・安全に・自動で」回すための運用知識。
ドメイン専門知識（ipa/stats/ds 等）とは別軸で、**道具としての Claude Code を使いこなす**ためのリファレンス。

> **最終検証日: 2026-09-25**（`model-routing.md` / `agentic-operating.md`。`orchestration.md` / `automation.md` / `tooling.md` は 2026-06-16 検証）／ 出典: 公式ドキュメント `https://code.claude.com/docs`・Anthropic 公式移行ガイド
> Claude Code の機能もモデルも更新が速い。**機能名・コマンド名・挙動・モデル事実は使用前に必ず公式で再確認すること**（このファイル群はスナップショット）。新モデルが出たら `agentic-operating.md` §10 の再監査手順を実行する。
> `/cc-features` コマンドは本ファイルを正本として参照する。

## ファイル一覧

| ファイル | 扱う領域 |
|---|---|
| `agentic-operating.md` | **エージェント運用原則** — 自律の線引き・スコープ・証拠ベース報告・委譲・最小変更、世代で反転した指針の記録、モデルリリース時の再監査手順 |
| `model-routing.md` | **モデル選定と effort** — 現行モデル表・effort 運用・Claude Code エイリアスとリスク対応・フォールバック |
| `orchestration.md` | サブエージェント・並列実行・Workflow・Agent View・Worktrees |
| `automation.md` | `/loop`・Routines(`/schedule`)・Desktop タスク・headless・Hooks |
| `tooling.md` | Plugins/Marketplace・Skills・Memory・Checkpoints・Fast mode・出力スタイル・MCP・Sessions |

## 課題→機能 逆引き

| やりたいこと | 使う機能 | 参照 |
|---|---|---|
| 聞かずに進めてよい範囲を決めたい | 自律の線引き（リスク判定に接続） | `agentic-operating.md` §1 |
| 頼まれた範囲をやり切り、余計な変更をしない | スコープ厳守・最小変更 | `agentic-operating.md` §3, §7 |
| 進捗・完了報告を信頼できるものにしたい | 証拠ベース報告 | `agentic-operating.md` §4 |
| 長時間の自律タスクで途中停止させたくない | 自律稼働の指示文 | `agentic-operating.md` §1 |
| どのモデル・effort を使うか決めたい | モデル選定・effort 運用 | `model-routing.md` §2, §3 |
| 上位モデルが使えない・落ちる | フォールバック運用 | `model-routing.md` §4 |
| 新モデルが出たので設定を見直したい | 再監査手順 | `agentic-operating.md` §10 |
| 重い調査で会話を圧迫したくない | サブエージェント | `orchestration.md` §1 |
| 独立した調査を同時に進めたい | 並列エージェント（非同期で自分の作業を続ける） | `orchestration.md` §2, `agentic-operating.md` §6 |
| 数十〜数百ファイルを一括変換・監査したい | Workflow（大規模オーケストレーション） | `orchestration.md` §3 |
| 複数セッションを並行管理したい | Agent View / バックグラウンドエージェント | `orchestration.md` §4 |
| 壊しても安全な隔離環境で実験したい | Worktrees | `orchestration.md` §5 |
| 一定間隔で同じ作業を繰り返したい（セッション中） | `/loop` | `automation.md` §1 |
| 条件達成まで粘り強く継続させたい | `/goal` | `automation.md` §2 |
| マシン OFF でも定期実行したい（クラウド） | Routines / `/schedule` | `automation.md` §3 |
| ローカルで定期実行したい（短間隔） | Desktop スケジュールタスク | `automation.md` §4 |
| CI/CD やスクリプトから自動実行したい | headless mode (`claude -p`) | `automation.md` §5 |
| 特定イベントで自動チェック・整形したい | Hooks | `automation.md` §6 |
| 機能をパッケージ化・共有・導入したい | Plugins / Marketplace | `tooling.md` §1 |
| 再利用ワークフローを `/名前` で呼びたい | Skills | `tooling.md` §2 |
| プロジェクト固有ルールを永続化したい | Memory (CLAUDE.md / rules / auto memory) | `tooling.md` §3 |
| 編集を巻き戻したい・誤りから復旧したい | Checkpoints / `/rewind` | `tooling.md` §4 |
| 反復作業を高速に回したい | Fast mode (`/fast`) | `tooling.md` §5, `model-routing.md` §3 |
| 外部ツール・DB・API を接続したい | MCP | `tooling.md` §7 |

## 品質フレームワークとの接続

- **自律の線引き = リスク判定**: 🟢🟡 は聞かずに進め、🟠🔴・破壊的操作・スコープ変更は確認（`quality/risks.md` と `agentic-operating.md` §1）。
- **自律化 ≠ 検証削減**: PDCA・3 層検証・TDD は維持。ゲート外の冗長な再確認だけ足さない（`agentic-operating.md` §0, §5）。
- **申し送り**: 作業中に見つけた担当タスク外の既存バグ・改善案は直さず `tasks/` に記録して申し送る（`quality/nonconformity.md` 手順2「記録」。担当タスク内で発生した不適合は同ファイルの是正プロセスに従う）。
- 🔴 最高リスク作業（DB 構造変更・定期実行変更・本番公開）→ **Worktrees** で隔離、モデルは `best`（`model-routing.md` §3）。
- 大改修の前に「戻れる状態」を確保 → **Checkpoints** + git コミット（`practices/git-workflow.md` §3）。
- 調べることが 3 つ以上で並行可能 → **並列サブエージェント**、待たずに自分の作業を続ける。
- 定期的な品質チェック・監視の自動化 → **Hooks / Routines**（`quality/metrics.md` の KPI 記録など）。

## 出典

- Overview: https://code.claude.com/docs
- Model config: https://code.claude.com/docs/en/model-config
- Anthropic 公式移行ガイド: https://platform.claude.com/docs/en/about-claude/models/migration-guide
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
