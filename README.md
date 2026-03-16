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
| 開発知識ベース（11ファイル） | `~/.claude/knowledge/ipa/` — 10分野の専門知識リファレンス |

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
│   └── ipa/                        ← システム開発 知識ベース（10分野）
│       ├── index.md                ← 分野横断マップ・実務活用索引
│       ├── fe.md                   ← 基礎理論・CS
│       ├── ap.md                   ← 応用技術
│       ├── db.md                   ← データベース
│       ├── nw.md                   ← ネットワーク
│       ├── es.md                   ← 組込み・IoT
│       ├── pm.md                   ← プロジェクト管理
│       ├── sm.md                   ← ITサービス運用
│       ├── st.md                   ← IT戦略・経営
│       ├── sa.md                   ← アーキテクチャ
│       └── au.md                   ← 監査・内部統制
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
| Desktop Commander | 任意 | ファイル操作・コマンド実行・プロセス管理 |
| PDF | 任意 | PDF読み取り・作成・結合・分割 |
| GitHub | 任意 | Issue・PR・コード検索・Actions連携 |
| Figma MCP | 任意 | Figmaデザイン参照 |

## システム開発 知識ベース

10分野の専門知識リファレンスを `~/.claude/knowledge/ipa/` に導入します。

Claude Codeが開発業務で以下のような専門的助言を提供できるようになります:

| 業務 | 活用例 |
|---|---|
| DB設計 | 正規化理論(1NF-5NF)に基づくスキーマレビュー、SQL最適化 |
| NW設計 | OSPF/BGPルーティング設計、VPN選定、障害切り分け手順 |
| セキュリティ | ゼロトラスト設計、TLS1.3、脅威モデリング(STRIDE) |
| PM | EVM(SPI/CPI/EAC)による進捗評価、見積り技法(FP法) |
| 運用 | SLA策定(MTBF/MTTR/稼働率計算)、ITIL4ベースの運用設計 |
| 経営 | NPV/IRRによるIT投資判断、DX戦略立案 |
| 設計 | マイクロサービス/CQRS/DDDのトレードオフ分析 |
| 監査 | COSO/J-SOXベースの内部統制設計、コンプライアンス確認 |

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
