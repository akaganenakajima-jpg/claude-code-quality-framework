# 周辺ツール・機能 — 拡張・記憶・復旧・接続

> 最終検証日: 2026-06-16 ／ 出典 `https://code.claude.com/docs`。挙動は使用前に公式ドキュメントで再確認。

## 1. Plugins と Marketplace

Skills・agents・hooks・MCPサーバーなどを1つにまとめて配布・導入できるパッケージ。`.claude-plugin/plugin.json` をマニフェストに持つ。

- **導入**: `/plugin`（マーケットプレイスから検索・インストール）。`/plugin marketplace add <owner/repo>` でチーム/コミュニティのマーケットを登録。
- **いつ使うか**: 既存の解決策を取り込みたいとき（本フレームワークの「自分で作るより既にあるものを使う」原則）。チームで設定を共有したいとき。
- **命名**: スキル等はプラグイン名でネームスペースされる（例 `/plugin-name:skill-name`）。
- 出典: https://code.claude.com/docs/en/plugins ／ https://code.claude.com/docs/en/discover-plugins

## 2. Skills

`SKILL.md` に「いつ使うか（description）」と手順を書いた再利用可能な能力。Claudeが文脈に応じて自動起動するか、`/skill-name` で明示呼び出しできる。

- **配置**: `~/.claude/skills/<name>/SKILL.md`（単体）またはプラグイン内。`$ARGUMENTS` でユーザー入力を受け取る。
- **本フレームワークでの例**: `skills/apple-hig-designer/` がこの形。UI作成時に自動適用される。
- **注意**: `description` の質が自動起動の精度を左右する。タスクに該当しそうなら積極的に起動する。
- 出典: https://code.claude.com/docs/en/skills

## 3. Memory — 永続的な記憶

| 種類 | 場所 | 用途 |
|---|---|---|
| プロジェクト CLAUDE.md | `./CLAUDE.md` / `./.claude/CLAUDE.md` | リポジトリ共有のルール（コミット対象） |
| ユーザー CLAUDE.md | `~/.claude/CLAUDE.md` | 全プロジェクト共通の個人設定 |
| ローカル CLAUDE.md | `./CLAUDE.local.md` | 個人のプロジェクト固有（gitignore） |
| パススコープルール | `.claude/rules/*.md`（frontmatter で `paths:`） | 特定ディレクトリにだけ効くルール |
| Auto memory | `~/.claude/projects/<proj>/memory/MEMORY.md` | Claudeが学習を自動蓄積 |

- **import**: `@path/to/file` で他ファイルを取り込める。
- **推奨**: CLAUDE.md は軽量に（目安200行以下）。詳細はオンデマンド参照に逃がす（本フレームワークの設計思想と一致）。
- 出典: https://code.claude.com/docs/en/memory

## 4. Checkpoints / `/rewind` — 巻き戻し

ファイル編集を自動でチェックポイント記録し、過去のプロンプト時点へ戻せる。

- **操作**: `/rewind` または `Esc` 2回。コードのみ／会話のみ／両方の復元、指定区間の要約を選べる。
- **保持**: 約30日（設定可能）。
- **限界**: Bashコマンドによる変更や Claude 外部の編集は追跡されない。**バージョン管理の代替ではない** → 大改修前は git コミットも併用（`practices/git-workflow.md` §3）。
- 出典: https://code.claude.com/docs/en/checkpointing

## 5. Fast mode

同じ Opus モデルを**速度最適化した設定**で動かすモード（モデル自体は変わらない）。`/fast` でトグル。

- **いつ使うか**: 反復的なペアプロ・ライブデバッグなど、即応性を優先したいとき。
- **注意**: コンテキストやコストの扱いが変わるわけではなく、応答が速くなるAPI設定の違い。対応モデルは公式ドキュメントで確認。

## 6. 出力スタイル（Output styles）

Claudeの応答形式をカスタムする。代表例: explanatory（詳細解説）・learning（教育的に学習者へコード貢献を促す）。プラグイン等でトグルする。

## 7. MCP — 外部ツール接続

Model Context Protocol。外部ツール・DB・APIを標準化された方法で接続する。

- **追加方法**:
  - CLI: `claude mcp add <name> ...`（`--transport http` でリモート接続など）
  - 設定ファイル: `~/.claude/.mcp.json`（ユーザー）／ `./.claude/.mcp.json`（プロジェクト）
  - デスクトップアプリ: 設定 → MCP Servers から検索追加
  - クラウド連携: claude.ai アカウントでコネクタ接続（Routines から利用）
- **トランスポート**: stdio / HTTP / SSE。
- **本フレームワークでの位置づけ**: 既存解決策の活用（Context7でライブラリ参照、GitHub操作は`gh`優先 等）。推奨MCP一覧は `recommended-tools.md`。
- 出典: https://code.claude.com/docs/en/mcp

## 8. Sessions — 継続・分岐

- `--continue` / `--resume`: 前回セッションを再開。
- `--fork-session`: 元を残したまま分岐。
- **いつ使うか**: 長い作業の中断・再開、別案を試す分岐。コンテキスト限界が近い時は `session-handoff` 系の引き継ぎも検討。
- 出典: https://code.claude.com/docs/en/sessions
