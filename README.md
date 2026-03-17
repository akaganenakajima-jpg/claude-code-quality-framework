# Claude Code 品質フレームワーク

ISO 9001:2015 に基づいた品質管理システムを Claude Code に導入するためのフレームワークです。
[everything-claude-code](https://github.com/anthropics/courses/tree/master/prompt_engineering_interactive_tutorial) (ECC) との**競合ゼロ設計**で併用可能です。

## 設計思想（C案アーキテクチャ）

- **CLAUDE.md**: 判定・トリガーのみ（軽量約150行）。毎セッション読み込まれるコンテキスト消費を最小化
- **knowledge/practices/**: 実装ルール（コーディング・テスト・セキュリティ等）は横断チェック発火時にオンデマンドで Read
- **hooks/**: プロセス品質の自動チェック（コミット前リスク判定リマインダー）
- **commands/**: スラッシュコマンドで品質プロセスを手動起動（`/5s`, `/knowledge`, `/risk`, `/quality-review`）
- **ECC との棲み分け**: 当フレームワーク = プロセス品質（PDCA/リスク/5S）。ECC = コード品質（フォーマット/型/テスト実行）

## セットアップ（3ステップ）

### Step 1: プロンプトをコピー
`setup-prompt.md` を開き、**内容を全てコピー**してください。

### Step 2: Claude Code に貼り付け
Claude Code を起動し、コピーした内容をチャット欄に貼り付けて送信してください。

### Step 3: 指示に従って進める
Claude Code が自動的に全ファイルを作成します。
ファイル作成の確認が出たら許可してください。
前提プログラム（Node.js/Python/uvx）のインストール案内が表示されます。

**以上で完了です。**

---

## 導入されるもの

| カテゴリ | 内容 |
|---|---|
| グローバルルール | `~/.claude/CLAUDE.md` — 判定・トリガー・品質方針・5S |
| 品質管理（8ファイル） | `~/.claude/quality/` — ISO9001準拠のPDCA・リスク管理・品質ゲート等 |
| 開発プラクティス（6ファイル） | `~/.claude/knowledge/practices/` — TDD・セキュリティ・Git・コーディングスタイル |
| スラッシュコマンド（4ファイル） | `~/.claude/commands/` — `/5s`, `/knowledge`, `/quality-review`, `/risk` |
| Hook（1ファイル） | `~/.claude/hooks/process-gate.py` — コミット前リスク判定リマインダー |
| 知識ベース — IPA（11ファイル） | `~/.claude/knowledge/ipa/` — システム開発10分野の専門知識 |
| 知識ベース — 統計検定1級（10ファイル） | `~/.claude/knowledge/stats/` — 確率論・推測・多変量・時系列・ベイズ等 |
| 知識ベース — DS発展（5ファイル） | `~/.claude/knowledge/ds-advanced/` — データエンジニアリング・分析・倫理 |
| 知識ベース — DSエキスパート（5ファイル） | `~/.claude/knowledge/ds-expert/` — 高度モデリング・MLシステム設計 |
| 知識ベース — DS数学ストラテジスト上級（5ファイル） | `~/.claude/knowledge/math-strategist/` — 線形代数・最適化・情報理論 |
| 知識ベース — E資格（5ファイル） | `~/.claude/knowledge/e-cert/` — 深層学習基礎・アーキテクチャ・応用 |
| 知識ベース — Python3基礎（5ファイル） | `~/.claude/knowledge/python3/` — 構文・標準ライブラリ・OOP・ベストプラクティス |

## フレームワーク構成

```
claude-code-quality-framework/
├── README.md                       ← このファイル
├── setup-prompt.md                 ← セットアッププロンプト本体
├── recommended-tools.md            ← 推奨MCP/ツール一覧
├── global/
│   ├── CLAUDE.md                   ← グローバルルール（参照用）
│   └── quality/                    ← ISO9001 品質管理ファイル（参照用）
│       ├── policy.md, process.md, gates.md, risks.md
│       ├── nonconformity.md, metrics.md, review.md, docs.md
├── knowledge/
│   ├── practices/                  ← 開発プラクティス（6ファイル）★NEW
│   │   ├── index.md, coding-style.md, security.md
│   │   ├── testing.md, git-workflow.md, dev-workflow.md
│   ├── ipa/                        ← システム開発（10分野・11ファイル）
│   ├── stats/                      ← 統計検定1級（9分野・10ファイル）
│   ├── ds-advanced/                ← DS発展（4分野・5ファイル）
│   ├── ds-expert/                  ← DSエキスパート（4分野・5ファイル）
│   ├── math-strategist/            ← DS数学ストラテジスト上級（4分野・5ファイル）
│   ├── e-cert/                     ← E資格（4分野・5ファイル）
│   └── python3/                    ← Python3基礎（4分野・5ファイル）
├── hooks/                          ← Hook ★NEW
│   └── process-gate.py             ← コミット前リスク判定リマインダー
├── commands/                       ← スラッシュコマンド ★NEW
│   ├── 5s.md, knowledge.md, quality-review.md, risk.md
└── examples/
    └── project-claude-md.example   ← プロジェクトCLAUDE.md テンプレート
```

## ECC との併用

[everything-claude-code](https://github.com/affaan-m/everything-claude-code) と完全に共存できます。

| 領域 | 当フレームワーク | ECC |
|---|---|---|
| ルール格納先 | `~/.claude/CLAUDE.md` | `~/.claude/rules/` |
| 読込タイミング | CLAUDE.md = 毎ターン / knowledge = オンデマンド | rules = 毎ターン |
| Hook目的 | プロセス品質（リスク判定リマインダー） | コード品質（lint/type check/test） |
| コマンド | `/5s`, `/knowledge`, `/risk`, `/quality-review` | ECC固有の57コマンド |
| 対象レイヤー | **プロセス**（PDCA/リスク/5S/知識参照） | **コード**（フォーマット/型/テスト実行） |

**競合ポイント: ゼロ**（異なるファイル、異なるメカニズム）

## 推奨ツール

詳細は `recommended-tools.md` を参照してください。

| ツール | おすすめ度 | 説明 |
|---|---|---|
| Notion MCP | ⭐ おすすめ | ドキュメントをNotionに自動記録 |
| Context7 MCP | ⭐ おすすめ | ライブラリドキュメントを自動参照 |
| Claude Preview | ⭐ おすすめ | Webページの見た目を確認（標準搭載） |
| Windows MCP | 任意 | Windows操作の自動化 |
| Desktop Commander MCP | 任意 | ファイル操作・コマンド実行・プロセス管理 |

## カスタマイズ

### プロジェクト固有ルールの追加
各プロジェクトのリポジトリに `CLAUDE.md` を作成し、プロジェクト固有のルールを記載してください。
テンプレートは `examples/project-claude-md.example` を参照してください。

### Hookのカスタマイズ
`hooks/process-gate.py` をベースに、プロジェクト固有のリスク判定ロジックを追加できます。
`~/.claude/settings.json` の `hooks` セクションで設定します。

## ライセンス

組織内利用を想定しています。
