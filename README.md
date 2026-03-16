# Claude Code 品質フレームワーク

ISO 9001:2015 に基づいた品質管理システムを Claude Code に導入するためのフレームワークです。
デスクトップアプリ（GUI版）向けです。

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
| グローバルルール | `~/.claude/CLAUDE.md` — 開発ルール・品質方針・5S・TDD等 |
| 品質管理（8ファイル） | `~/.claude/quality/` — ISO9001準拠のPDCA・リスク管理・品質ゲート等 |
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
│       ├── policy.md               ← 品質方針・品質目標
│       ├── process.md              ← PDCAプロセス定義
│       ├── gates.md                ← 品質ゲート（G1-G5）
│       ├── risks.md                ← リスク登録簿
│       ├── nonconformity.md        ← 不適合・是正処置
│       ├── metrics.md              ← 品質KPI
│       ├── review.md               ← 3層検証基準
│       └── docs.md                 ← 文書管理ルール
├── knowledge/
│   ├── ipa/                        ← システム開発（10分野・11ファイル）
│   │   ├── index.md, fe.md, ap.md, db.md, nw.md
│   │   ├── es.md, pm.md, sm.md, st.md, sa.md, au.md
│   ├── stats/                      ← 統計検定1級（9分野・10ファイル）
│   │   ├── index.md, prob.md, inference.md, multivariate.md, ts.md
│   │   ├── bayes.md, regression.md, doe.md, stochastic.md, ml.md
│   ├── ds-advanced/                ← DS発展（4分野・5ファイル）
│   │   ├── index.md, data-engineering.md, analytics.md, modeling.md, ethics.md
│   ├── ds-expert/                  ← DSエキスパート（4分野・5ファイル）
│   │   ├── index.md, advanced-modeling.md, deep-analytics.md, system-design.md, business.md
│   ├── math-strategist/            ← DS数学ストラテジスト上級（4分野・5ファイル）
│   │   ├── index.md, linear-algebra.md, calculus-optimization.md, probability-stats.md, applied-math.md
│   ├── e-cert/                     ← E資格（4分野・5ファイル）
│   │   ├── index.md, dl-fundamentals.md, dl-architectures.md, dl-training.md, dl-applications.md
│   └── python3/                    ← Python3基礎（4分野・5ファイル）
│       ├── index.md, core-syntax.md, stdlib.md, oop.md, best-practices.md
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
| Notion MCP | ⭐ おすすめ | ドキュメントをNotionに自動記録 |
| Context7 MCP | ⭐ おすすめ | ライブラリドキュメントを自動参照 |
| Claude Preview | ⭐ おすすめ | Webページの見た目を確認（標準搭載） |
| Windows MCP | 任意 | Windows操作の自動化 |
| Desktop Commander MCP | 任意 | ファイル操作・コマンド実行・プロセス管理 |
| PDF MCP | 任意 | PDF読み取り・作成・結合・分割 |
| GitHub MCP | 任意 | Issue・PR・コード検索・Actions連携 |
| Figma MCP | 任意 | Figmaデザイン参照 |

## 知識ベース（7分野・46ファイル）

`~/.claude/knowledge/` に7分野の専門知識リファレンスを導入します。

Claude Codeが業務で以下のような専門的助言を提供できるようになります:

| 分野 | 活用例 |
|---|---|
| **IPA（システム開発）** | DB正規化・SQL最適化、NW設計、セキュリティ、PM、運用、監査 |
| **統計検定1級** | 仮説検定、ベイズ推定、時系列予測、多変量解析、機械学習理論 |
| **DS発展** | データ前処理・ETL、EDA・可視化、予測モデル構築、データ倫理・GDPR |
| **DSエキスパート** | 因果推論、空間統計、NLP、MLシステム設計、ビジネスKPI |
| **DS数学ストラテジスト上級** | 線形代数、凸最適化、情報理論、数値計算、フーリエ解析 |
| **E資格** | CNN/RNN/Transformer、分散学習、転移学習、物体検出、強化学習 |
| **Python3基礎** | 構文・データ型、標準ライブラリ、OOP設計、pytest、パフォーマンス |

---

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
