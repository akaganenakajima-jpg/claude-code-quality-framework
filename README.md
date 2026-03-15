# Claude Code 品質フレームワーク

ISO 9001:2015 に基づいた品質管理システムを、Claude Code（GUI版）に導入するためのフレームワークです。

## セットアップ（3ステップ・クリックのみ）

### Step 1: プロンプトをコピー
`setup-prompt.md` を開き、**内容を全てコピー**してください。

### Step 2: Claude Code に貼り付け
Claude Code（GUI版）を起動し、コピーした内容をチャット欄に貼り付けて送信してください。

### Step 3: 指示に従ってクリック
Claude Code が自動的に全ファイルを作成します。
途中で「ファイルを作成してよいですか？」と聞かれたら「はい」をクリックしてください。
推奨ツールの追加も案内されるので、必要なものを選択してください。

**以上で完了です。**

---

## 導入されるもの

| カテゴリ | 内容 |
|---|---|
| グローバルルール | `~/.claude/CLAUDE.md` — 開発ルール・品質方針・5S・TDD等 |
| 品質管理（8ファイル） | `~/.claude/quality/` — ISO9001準拠のPDCA・リスク管理・品質ゲート等 |

## フレームワーク構成

```
claude-code-quality-framework/
├── README.md                       ← このファイル
├── setup-prompt.md                 ← セットアッププロンプト本体
├── recommended-tools.md            ← 推奨MCP/ツール一覧
├── global/
│   ├── CLAUDE.md                   ← グローバルルール（参照用）
│   └── quality/                    ← ISO9001 品質管理ファイル（参照用）
│       ├── policy.md               ← 品質方針・品質目標
│       ├── process.md              ← PDCAプロセス定義
│       ├── gates.md                ← 品質ゲート（G1-G5）
│       ├── risks.md                ← リスク登録簿
│       ├── nonconformity.md        ← 不適合・是正処置
│       ├── metrics.md              ← 品質KPI
│       ├── review.md               ← 3層検証基準
│       └── docs.md                 ← 文書管理ルール
├── hooks/                          ← Hookテンプレート（参考用）
│   ├── pre-edit-guard.py.template
│   ├── pre-deploy-guard.py.template
│   └── post-deploy-remind.py.template
└── examples/
    ├── project-claude-md.example   ← プロジェクトCLAUDE.md テンプレート
    └── commands/
        ├── deploy.md.example       ← デプロイスキル例
        └── quick-status.md.example ← ステータス確認スキル例
```

## 推奨ツール

詳細は `recommended-tools.md` を参照してください。

| ツール | おすすめ度 | 説明 |
|---|---|---|
| Notion MCP | おすすめ | ドキュメントをNotionに自動記録 |
| Context7 MCP | おすすめ | ライブラリドキュメントを自動参照 |
| Claude Preview | おすすめ | Webページの見た目を確認（標準搭載） |
| Figma MCP | 任意 | Figmaデザイン参照 |
| Google Drive MCP | 任意 | Google Driveファイル読み取り |
| Box MCP | 任意 | Boxファイル管理 |

## カスタマイズ

### プロジェクト固有ルールの追加
各プロジェクトのリポジトリに `CLAUDE.md` を作成し、プロジェクト固有のルールを記載してください。
テンプレートは `examples/project-claude-md.example` を参照してください。

### Hookの導入
`hooks/` フォルダのテンプレートを参考に、プロジェクトの `.claude/settings.json` に設定できます。
- **pre-edit-guard**: 特定ファイルの編集を防止
- **pre-deploy-guard**: E2Eテスト未実施のデプロイをブロック
- **post-deploy-remind**: デプロイ後のチェックリストを表示

## ライセンス

組織内利用を想定しています。
