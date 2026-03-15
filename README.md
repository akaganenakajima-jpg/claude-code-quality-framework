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
| IPA知識ベース（11ファイル） | `~/.claude/knowledge/ipa/` — 全10資格の満点合格者レベル専門知識 |

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
│   └── ipa/                        ← IPA情報処理技術者試験 知識ベース
│       ├── index.md                ← 分野横断マップ・実務活用索引
│       ├── fe.md                   ← 基本情報技術者
│       ├── ap.md                   ← 応用情報技術者
│       ├── db.md                   ← データベーススペシャリスト
│       ├── nw.md                   ← ネットワークスペシャリスト
│       ├── es.md                   ← エンベデッドシステムスペシャリスト
│       ├── pm.md                   ← プロジェクトマネージャ
│       ├── sm.md                   ← ITサービスマネージャ
│       ├── st.md                   ← ITストラテジスト
│       ├── sa.md                   ← システムアーキテクト
│       └── au.md                   ← システム監査技術者
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

## IPA知識ベース

IPA情報処理技術者試験 全10区分（FE/AP/DB/NW/ES/PM/SM/ST/SA/AU）の満点合格者レベルの知識を `~/.claude/knowledge/ipa/` に導入します。

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
