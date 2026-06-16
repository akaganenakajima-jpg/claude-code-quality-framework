# claude-code-quality-framework Project Rules

## プロジェクト概要
Claude Code 向け ISO 9001:2015 準拠の品質管理フレームワーク配布リポジトリ。
ユーザーが `setup-prompt.md` の内容を Claude Code に貼り付けるだけで全ファイルが自動生成される。

## 設計原則
1. **貼り付けで導入**: process系（CLAUDE.md・quality・practices・commands・hooks）は setup-prompt.md 内の `<content>` タグにインライン展開し、貼り付けだけで導入できる。knowledge/ と skills/ は容量が大きいため §4 で git clone + cp により導入する
2. **ECC競合ゼロ**: `~/.claude/CLAUDE.md` + `knowledge/` を使用（ECCの `~/.claude/rules/` と別空間）
3. **オンデマンド読込**: CLAUDE.md は判定・トリガーのみ（~160行）。実装ルールは `knowledge/practices/` にオンデマンド参照

## ファイル編集ルール

### setup-prompt.md（最重要ファイル）
- process系（§1 CLAUDE.md / §2 quality / §3 practices・commands・hooks）の内容は `<content>` タグ内にインライン展開すること
- knowledge/ と skills/ は §4 の git clone + cp で導入する（`<content>` インラインしない）
- 新しい知識ドメインを追加したら §4 の cp ループ・§0-2 の diff ループ・§6 検証にドメイン名を追加する
- セクション番号を変更した場合、後続セクションの番号も連動更新する
- §6 検証セクションの確認項目も実態と一致させる

### global/CLAUDE.md
- setup-prompt.md §1 の `<content>` と内容を同期させる
- ユーザー固有パス（スクリーンショットフォルダ等）は含めない

### knowledge/ 配下
- 新ファイル追加時は対応する `index.md` にも登録する
- §4 の clone+cp で配布される。新ドメイン追加時は §4 cp ループ・§0-2 diff ループ・§6 検証にドメイン名を追加する（`<content>` インラインは不要）

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
- [ ] `setup-prompt.md` の該当 `<content>` を更新したか（process系の場合）
- [ ] 知識ドメイン追加時は §4 cp ループ・§0-2 diff ループ・§6 検証にドメイン名を追加したか
- [ ] `global/` のマスターファイルと同期しているか
- [ ] README.md のファイルツリーやテーブルに反映したか
- [ ] セクション番号がずれていないか
