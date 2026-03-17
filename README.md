# Claude Code 品質フレームワーク

ISO 9001:2015 に基づいた品質管理システムと、8分野75ファイルの専門知識ベースを Claude Code に導入するフレームワークです。
[everything-claude-code](https://github.com/affaan-m/everything-claude-code) (ECC) との**競合ゼロ設計**で併用可能です。

## セットアップ（3ステップ）

### Step 1: プロンプトをコピー
`setup-prompt.md` を開き、**内容を全てコピー**してください。

### Step 2: Claude Code に貼り付け
Claude Code を起動し、コピーした内容をチャット欄に貼り付けて送信してください。

### Step 3: 指示に従って進める
Claude Code が自動的に全ファイルを作成します。
ファイル作成の確認が出たら許可してください。

**以上で完了です。**

---

## 設計思想

```
CLAUDE.md（~160行）          ← 毎セッション読み込み。判定・トリガーのみ
  ├─ 大分類 13項目           「何をする課題か？」→ 参照先を特定
  └─ 横断チェック 8項目      「安全？性能？テスト？UX？」→ 追加参照
       ↓
knowledge/*/index.md          ← オンデマンド読み込み。シナリオ逆引きでルーティング
       ↓
knowledge/*/detail.md          ← 必要な§セクションだけ読む（平均1-2ファイル）
```

- **コンテキスト消費を最小化**: CLAUDE.md はトリガー判定のみ。詳細知識はオンデマンド
- **プロセス品質**: PDCA ゲート・リスク判定・5S を全タスクに適用
- **ECC との棲み分け**: 当フレームワーク = プロセス品質。ECC = コード品質（フォーマット/型/テスト実行）

## 導入されるもの

### プロセス品質

| カテゴリ | ファイル数 | 内容 |
|---|---|---|
| グローバルルール | 1 | `~/.claude/CLAUDE.md` — 判定・トリガー・品質方針・5S |
| 品質管理 | 8 | `~/.claude/quality/` — ISO9001準拠のPDCA・リスク管理・品質ゲート |
| 開発プラクティス | 6 | `~/.claude/knowledge/practices/` — TDD・セキュリティ・Git・コーディングスタイル |
| スラッシュコマンド | 4 | `~/.claude/commands/` — `/5s`, `/knowledge`, `/quality-review`, `/risk` |
| Hook | 1 | `~/.claude/hooks/process-gate.py` — コミット前リスク判定リマインダー |

### 知識ベース（8分野・75ファイル）

タスクを受けると CLAUDE.md が課題を分析し、該当する知識ファイルを自動で Read してから作業します。

| 分野 | ファイル数 | パス | 内容 |
|---|---|---|---|
| IPA情報処理 | 11 | `knowledge/ipa/` | システム開発10分野（アーキテクチャ・DB・NW・PM等） |
| 統計検定1級 | 10 | `knowledge/stats/` | 確率論・推測・回帰・時系列・ベイズ・機械学習 |
| DS発展 | 5 | `knowledge/ds-advanced/` | データエンジニアリング・分析・モデリング・倫理 |
| DSエキスパート | 5 | `knowledge/ds-expert/` | 高度モデリング・因果推論・MLシステム設計 |
| DS数学ストラテジスト | 5 | `knowledge/math-strategist/` | 線形代数・最適化・確率・応用数学 |
| E資格 | 5 | `knowledge/e-cert/` | 深層学習基礎・アーキテクチャ・学習技法・応用 |
| Python3基礎 | 5 | `knowledge/python3/` | 構文・標準ライブラリ・OOP・ベストプラクティス |
| UX心理学 | 6 | `knowledge/ux-psychology/` | 43法則（情報設計・選択設計・動機設計・印象設計・認知の罠） |

## フレームワーク構成

```
claude-code-quality-framework/
├── README.md                       ← このファイル
├── setup-prompt.md                 ← セットアッププロンプト本体
├── recommended-tools.md            ← 推奨MCP/ツール一覧
├── global/
│   ├── CLAUDE.md                   ← グローバルルール（参照用マスター）
│   └── quality/                    ← ISO9001 品質管理（8ファイル）
├── knowledge/
│   ├── practices/                  ← 開発プラクティス（6ファイル）
│   ├── ipa/                        ← IPA情報処理（11ファイル）
│   ├── stats/                      ← 統計検定1級（10ファイル）
│   ├── ds-advanced/                ← DS発展（5ファイル）
│   ├── ds-expert/                  ← DSエキスパート（5ファイル）
│   ├── math-strategist/            ← DS数学ストラテジスト上級（5ファイル）
│   ├── e-cert/                     ← E資格（5ファイル）
│   ├── python3/                    ← Python3基礎（5ファイル）
│   └── ux-psychology/              ← UX心理学（6ファイル）
├── hooks/
│   └── process-gate.py             ← コミット前リスク判定リマインダー
├── commands/
│   └── 5s.md, knowledge.md, quality-review.md, risk.md
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
