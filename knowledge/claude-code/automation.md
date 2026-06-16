# 自動化・定期実行 — 繰り返しと無人実行

> 最終検証日: 2026-06-16 ／ 出典 `https://code.claude.com/docs`。挙動は使用前に公式ドキュメントで再確認。

スケジューリングは「どこで・いつ・何にアクセスして」動かすかで使い分ける。早見表:

| | `/loop` | Desktop タスク | Routines（クラウド） |
|---|---|---|---|
| 実行場所 | ローカル | ローカル | Anthropic クラウド |
| マシンOFFでも実行 | ✗ | ✗ | ✓ |
| セッション起動が必要 | ✓ | ✗ | ✗ |
| ローカルファイルアクセス | ✓ | ✓ | ✗（クラウドで都度clone） |
| 最小間隔 | 数十秒〜 | 1分 | 1時間 |
| GitHub/API トリガー | ✗ | ✗ | ✓ |

## 1. `/loop` — セッション中の繰り返し

開いているセッション内で、プロンプトを一定間隔または動的間隔で繰り返す。

- **構文**: `/loop 5m <プロンプト>`（固定間隔）／ `/loop <プロンプト>`（Claudeが間隔を自己判断）／ `/loop`（組み込みメンテナンスプロンプト）。単位は `s`/`m`/`h`/`d`。
- **いつ使うか**: 「5分ごとにデプロイ状況を確認」「PRを見張り続ける」などのポーリング。
- **注意**: **セッションを開いている間だけ**動く。一定期間（約7日）で自動失効。`Esc` で停止。`.claude/loop.md` / `~/.claude/loop.md` でデフォルトプロンプトをカスタム可能。
- 出典: https://code.claude.com/docs/en/scheduled-tasks

## 2. `/goal` — 条件達成まで継続

完了条件を指定し、達成するまでターンを継いで自律的に進める（ポーリングではなく粘り強い継続）。

- **いつ使うか**: 「テストが全部通るまで」「ビルドが緑になるまで」のように、明確なゴール条件がある反復作業。
- 出典: https://code.claude.com/docs/en/goal

## 3. Routines — クラウドで無人定期実行

Anthropic のクラウドで、マシンが OFF でも保存済み設定（プロンプト・対象リポジトリ・MCPコネクタ）を自動実行する。結果は新規セッションとして記録される。

- **トリガー3種**: ①スケジュール（cron 5フィールド／hourly・daily・weekly等、最小1時間）②GitHubイベント（pull_request / release、author・branch・label 等でフィルタ）③API（POST `/fire`、bearer token、任意の `text` でコンテキスト付与）。
- **作成**: CLI `/schedule`、またはWeb（claude.ai/code）。MCPコネクタ（Slack/Linear/Gmail等）を指定可能。
- **いつ使うか**: 「毎朝レポート生成」「PRが来たら自動レビュー」「アラート受信で自動調査」。
- **注意**: 権限プロンプトなしの自律実行。実行時刻は±数分のずれ（同一ルーティンでは一定）。
- 出典: https://code.claude.com/docs/en/routines

## 4. Desktop スケジュールタスク — ローカル定期実行

デスクトップアプリでローカル実行する定期/単発タスク。セッションを開いておく必要がなく、ローカルファイルに直接アクセスできる。最小間隔1分。`/schedule` で「ローカル」を選ぶか Routines UI から作成。

- 出典: https://code.claude.com/docs/en/desktop-scheduled-tasks

## 5. Headless mode — スクリプト/CI から呼び出す

TTY なしの単発実行。`claude -p "プロンプト"` でプロンプトを渡す。settings・hooks・permissions を継承。

- **いつ使うか**: GitHub Actions・pre-commit・シェルスクリプトからの自動実行、API結果の自動分析。
- **注意（本フレームワーク固有）**: `CLAUDECODE` 環境変数が設定済みの環境では `env -u CLAUDECODE claude -p "..."` のように除外して呼ぶ。
- 出典: https://code.claude.com/docs/en/github-actions

## 6. Hooks — イベント駆動の決定論的フック

特定イベントでシェルコマンドを自動実行する。LLMの判断に依存しない**決定論的**な制御（自動整形・検証・ルール強制）に使う。

- **イベント種別**: PreToolUse / PostToolUse / Stop / SubagentStop / SessionStart / SessionEnd / UserPromptSubmit / PreCompact / Notification。
- **設定**: `~/.claude/settings.json`（ユーザー）／ `.claude/settings.json`（プロジェクト）。`matcher` で対象ツールを正規表現指定し、`command` を実行。入力は stdin に JSON で渡る。
- **本フレームワークの方針**: 品質ゲートのフックは**ブロックしない**（常に exit 0）。stderr にリマインダーを出すのみ（`hooks/process-gate.py` 参照）。
- **いつ使うか**: 編集後の自動 lint/format、コミット前チェック、セッション開始時の環境確認。
- 出典: https://code.claude.com/docs/en/hooks-guide
