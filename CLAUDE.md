# claude-code-quality-framework Project Rules

## プロジェクト概要
Claude Code 向け ISO 9001:2015 準拠の品質管理フレームワーク配布リポジトリ。
ユーザーが `setup-prompt.md` の内容を Claude Code に貼り付けるだけで全ファイルが自動生成される。

## 設計原則
1. **プロンプトのみ導入**: setup-prompt.md 内の `<content>` タグにファイル内容をインライン展開する。`cp` コマンドや git clone を前提としない
2. **ECC競合ゼロ**: `~/.claude/CLAUDE.md` + `knowledge/` を使用（ECCの `~/.claude/rules/` と別空間）
3. **オンデマンド読込**: CLAUDE.md は判定・トリガーのみ（~160行）。実装ルールは `knowledge/practices/` にオンデマンド参照

## ファイル編集ルール

### setup-prompt.md（最重要ファイル）
- 全ファイルの内容は `<content>` タグ内にインライン展開すること
- `global/` や `knowledge/` へのファイルパス参照（`cp` コマンド等）は**禁止**
- セクション番号を変更した場合、後続セクションの番号も連動更新する
- §6 検証セクションの確認項目も実態と一致させる

### global/CLAUDE.md
- setup-prompt.md §1 の `<content>` と内容を同期させる
- ユーザー固有パス（スクリーンショットフォルダ等）は含めない

### knowledge/ 配下
- 新ファイル追加時は対応する `index.md` にも登録する
- setup-prompt.md の該当セクションにもインライン追加する

### hooks/ 配下
- Hook は**ブロックしない**（常に exit 0）。stderr にリマインダーを出力するのみ
- setup-prompt.md にもインライン追加する

### commands/ 配下
- コマンドファイルはClaude Code の `~/.claude/commands/` に配置される前提
- setup-prompt.md にもインライン追加する

## リポジトリ構成
```
├── CLAUDE.md               ← このファイル（プロジェクトルール）
├── README.md               ← ユーザー向け説明
├── setup-prompt.md         ← 配布用プロンプト本体（最重要）
├── recommended-tools.md    ← 推奨MCP/ツール一覧
├── global/                 ← 参照用マスターファイル
│   ├── CLAUDE.md
│   └── quality/
├── knowledge/              ← 知識ベース
│   ├── practices/          ← 開発プラクティス（6ファイル）
│   └── ...                 ← IPA/stats/ds 等
├── hooks/                  ← Hook スクリプト
├── commands/               ← スラッシュコマンド
└── examples/               ← テンプレート
```

## 変更時のチェックリスト
- [ ] `setup-prompt.md` の該当 `<content>` を更新したか
- [ ] `global/` のマスターファイルと同期しているか
- [ ] README.md のファイルツリーやテーブルに反映したか
- [ ] セクション番号がずれていないか
