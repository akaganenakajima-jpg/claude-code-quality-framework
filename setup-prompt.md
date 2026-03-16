# Claude Code 品質フレームワーク セットアップ

以下の指示に従って、品質管理フレームワークの全ファイルを作成してください。
各ファイルの内容は `<content>` タグ内にそのまま記載されています。
全て完了したら検証を実施してください。

---

## 1. グローバルルール

`~/.claude/CLAUDE.md` に以下を書き込んでください:

<content>
# CLAUDE.md — グローバル設定（全プロジェクト共通）

> プロジェクト固有ルールは各リポジトリの `CLAUDE.md` を参照

## Conversation Guidelines
- 常に日本語で会話する

## Code Style Guidelines
- 自明なコードコメントは書かないでください
- 不要な空白は削除してください
- 新規ファイルを作成する際は必ず末尾に改行を足すこと

## GitHub Operations
- GitHubのリソース（リポジトリ、Issue、PR、コード等）を操作する際は、`gh` コマンド（GitHub CLI）を使用する
- WebFetchやWebSearchではなく、`gh` コマンドを優先する

## 品質管理 (ISO9001:2015準拠)
品質方針: 「証拠に基づき、正しく・安全に・持続的に動くシステムを提供する」
詳細・品質目標 → `~/.claude/quality/policy.md`

### PDCAゲート（全タスクに適用。省略禁止）
1. **Plan**: 受入基準+リスク判定+影響範囲を明文化してから着手 → `quality/process.md`
2. **Do**: TDD + 品質ゲート通過 → `quality/gates.md`
3. **Check**: 3層検証（unit→E2E→本番）→ `quality/review.md`
4. **Act**: 不適合→根本原因→是正→水平展開 → `quality/nonconformity.md`

### リスク判定（変更前に必ず実施）→ `quality/risks.md`
- 🟢 通常: テスト追加・コメント修正・新規ファイル
- 🟡 標準: 既存コード修正・設定変更（revert可能）→ commit後に着手
- 🟠 強化: 複数機能に影響・API変更 → 影響分析必須
- 🔴 最高: DB変更・cron変更・デプロイ → Worktree必須

### 品質記録
- 不適合発生時 → `tasks/` にタスク化（根本原因・是正・水平展開を記載）
- セッション終了時 → 品質KPI更新 → `quality/metrics.md`
- 文書管理ルール → `quality/docs.md`

## 5S — 新タスク開始前の必須プロトコル
新しいタスクに取り掛かる前に、必ず以下の5Sを実施する。省略禁止。

### 1. 整理（Seiri）— 不要プロセスの排除
- タスクマネージャー等で実行中プロセスを確認
- ゾンビプロセス・不要なバックグラウンドジョブがあれば kill
- 前タスクのログファイル・一時ファイルが不要なら削除

### 2. 整頓（Seiton）— 作業環境の確認
- 現在の git ブランチ・uncommitted changes を確認（`git status`）
- 作業ディレクトリが正しいか確認
- 必要なファイル・データが揃っているか確認

### 3. 清掃（Seiso）— リソースの健全性確認
- CPU / メモリ / ディスクの使用率を確認
- 異常値（CPU>50%持続、メモリ>80%、ディスク>90%）があれば先に解決
- **異常は運用（手動kill等）ではなく仕組み（limiter/watchdog等）で解決**する

### 4. 清潔（Seiketsu）— ルール・設定の最新化
- プロジェクトの CLAUDE.md / memory が最新か確認
- 前タスクで得た知見がメモリに記録されているか確認

### 5. 躾（Shitsuke）— 手順の遵守
- タスク管理（TodoWrite）を開始
- 必要ならタスクファイル（`tasks/`）を作成

## 知識ベース自動参照（`~/.claude/knowledge/ipa/`）
以下の業務・キーワードを検知したら、該当する知識ファイルを **Read して参照してから** 作業する。

| トリガー（業務・キーワード） | 参照ファイル |
|---|---|
| DB設計・テーブル変更・インデックス・SQL最適化・正規化 | `db.md` |
| アーキテクチャ設計・マイクロサービス・可用性・キャッシュ・移行 | `sa.md` |
| NW設計・VPN・DNS・TLS・帯域・CDN・障害切り分け | `nw.md` |
| 運用設計・SLA・インシデント管理・BCP/DR・ITIL | `sm.md` |
| 監査・内部統制・ログ証跡・コンプライアンス・J-SOX | `au.md` |
| プロジェクト管理・見積り・EVM・スケジュール・リスク分析 | `pm.md` |
| IT投資判断・ROI/NPV・DX戦略・ビジネス分析・BSC | `st.md` |
| アルゴリズム最適化・計算量・データ構造・ソート | `fe.md` |
| 待ち行列・パイプライン・セキュリティ設計・暗号 | `ap.md` |
| 組込み・IoT・RTOS・安全設計・センサー | `es.md` |
| コードレビュー・設計レビュー（横断的） | `index.md` → 該当分野を特定して参照 |

- 複数分野にまたがる場合は `index.md` の横断マップで参照先を決定
- 知識ファイルの具体的なセクション番号（§）を引用して根拠を示す

## Development Philosophy
### Before Implementation
- 新しい機能を実装する前に、以下を必ず確認する：
1. 既存のコードベース内に同様の実装やユーティリティがないか検索する
2. 使用しているライブラリ/フレームワークに該当する API や機能がないか確認する
3. Context7 MCP（`mcp__context7__`）を使ってライブラリのドキュメントを参照する
- 「自分で実装する」より「既存の解決策を使う」を優先する

## Task Management
- タスクはプロジェクトルートの `tasks/` フォルダで管理する
- タスクファイルの命名規則: `YYYYMMDD_TXXX_タスク名.md`（例: `20260303_T001_承認待ち状態API調査.md`）
- `YYYYMMDD`: タスク作成日
- `TXXX`: 3桁連番（プロジェクト内でユニーク）
- タスクファイルには以下を記載する:
  - 背景・目的
  - 調査・作業結果（随時更新）
  - 次のアクション
- タスク完了後は `tasks/done/` フォルダにアーカイブする

### Test-Driven Development (TDD)
- 原則としてテスト駆動開発（TDD）で進める
- 期待される入出力に基づき、まずテストを作成する
- 実装コードは書かず、テストのみを用意する
- テストを実行し、失敗を確認する
- テストが正しいことを確認できた段階でコミットする
- その後、テストをパスさせる実装を進める
- 実装中はテストを変更せず、コードを修正し続ける
- すべてのテストが通過するまで繰り返す

## 開発フロー（GitHub Flow）
- 変更は feature ブランチで行い PR を経由して main にマージする
- コミット粒度は「1機能/1バグ修正」を1コミットに。巨大コミット禁止
- デプロイ前に E2E テストを実行する
- デプロイ前にロールバック手順を確認する

## セキュリティ原則（IPA セキュアコーディング準拠）
- **入力値検証**: APIエンドポイントは必ずパラメータをバリデーションする（型・範囲・形式）
- **エラー情報**: エラーレスポンスにスタックトレース・内部パス・DB構造を含めない
- **依存パッケージ**: 定期的に `npm audit` を実行し高リスク脆弱性は即対応
- **シークレット**: APIキー・認証情報をコードにハードコードしない
- **ログ管理**: 個人情報・認証情報をログに出力しない

## 行き詰まり・エラー対処プロトコル
- **Bash が 3分無応答**: 強制中断し、原因（無限ループ/権限エラー/ネットワーク等）を特定して報告する
- **同じエラーが 5回**: 同じアプローチを繰り返さず、別の解決策を検討する。「試したこと / 失敗理由 / 次の案」を報告する
- **作業前の保存**: 大きな変更を始める前に `git add -p && git commit` で現状を保存する（特にリファクタリング前）
- **変更後の確認**: 修正後は `git diff HEAD` で変更箇所を自分でも確認し、ユーザーに要点を報告する

## Subagent 活用方針
以下の条件を満たす場合は Task ツール（Explore/Bash/general-purpose）でサブエージェントに委譲する:
- 独立した調査ステップが 3つ以上並列実行できる
- 重い検索・探索でメインコンテキストを消費したくない
- 長時間実行のバックグラウンド処理（`run_in_background: true`）が適切な場合

委譲しない場合:
- ファイルが特定されており、Glob/Grep で即座に見つかる単純検索
- 2〜3ファイルの読み書きで完結するタスク

## Claude Code ツール使用上の注意
- `preview_eval` で `return` 文を使う場合は即時関数 `(function(){ ... return ...; })()` に包む
- モバイルデザイン確認は `preview_resize preset:mobile` を使う

## Claude Code 高度機能の活用

### Worktrees（リスクの高い変更時に積極的に提案する）
- 「大幅なUI変更」「破壊的リファクタリング」「実験的機能を試したい」場合は `EnterWorktree` を提案する
- main は常にデプロイ可能な状態に保つ。失敗してもworktreeを削除するだけで戻せる
- 提案タイミング: 「試しに〜したい」「〜を大幅に変えたい」「壊れても構わない」と言われた時

### Headless mode（自動化・cron・スクリプト化の相談時に提案する）
- 非インタラクティブ実行: `env -u CLAUDECODE claude -p "プロンプト"` または標準入力でデータを渡す
- `CLAUDECODE` 環境変数が設定されていると起動できないため `env -u CLAUDECODE` が必須
- 提案タイミング: 「毎日自動で〜したい」「cronで〜を実行したい」「APIの結果をClaudeに分析させたい」と言われた時

### Hooks（デプロイ安全性強化・新プロジェクトのガード設定時に提案する）
- `.claude/settings.json` の `hooks` セクションで設定（プロジェクト単位）
- PreToolUse: exit 1 でツールをブロック / exit 0 で許可。stdin に JSON でツール情報が来る
- PostToolUse: 常に exit 0（リマインダー・追加コンテキスト表示）
- 典型パターン:
  - デプロイ前 E2E 強制: Bash hook で `.e2e_passed` タイムスタンプを確認
  - 禁止ファイルガード: Edit/Write hook でファイルパスをチェック
</content>

---

## 2. 品質管理ファイル（8個）

### `~/.claude/quality/policy.md`:
<content>
# 品質方針 (ISO9001 §5.2) + 品質目標 (§6.2)

## 方針
「証拠に基づき、正しく・安全に・持続的に動くシステムを提供する」
1. **Evidence-First**: 推測でなくテスト結果・メトリクスで判断
2. **Fail-Safe**: 影響を理解してから実施。失敗してもロールバック可能な状態を保つ
3. **Continuous Learning**: 不適合を記録・分析し同じ問題を二度起こさない

## 品質目標（測定可能）
| KPI | 目標 | 測定 |
|---|---|---|
| テスト通過率 | 100% | vitest + E2E |
| デプロイ後障害 | ≤1回/月 | ロールバック記録 |
| 不適合再発 | 0件 | tasks/done分析 |
| 手戻り回数 | ≤2回/セッション | Phase1再開数 |
| 是正完了率 | ≥90% | タスク完了率 |
| E2E所要時間 | ≤3分 | e2e_test.sh |
</content>

### `~/.claude/quality/process.md`:
<content>
# PDCAプロセス定義 (ISO9001 §4.4)

全タスクに以下のサイクルを適用する。段階の省略禁止。

## Plan（計画）
- 前提: 5Sプロトコル完了済み
- 受入基準を明文化（「何が達成されたら完了か」）
- リスク判定実施 → `risks.md`
- 影響範囲を特定（変更するファイル・API・DB）

## Do（実行）
- TDDでテスト先行
- 品質ゲート順守 → `gates.md`
- 1機能/1バグ = 1コミット

## Check（検証）
- 3層検証 → `review.md`
- 6Phaseデバッグループ（該当時）
- deploy-protocol準拠（デプロイ時）

## Act（改善）
- 不適合 → 根本原因分析 → 是正 → `nonconformity.md`
- 品質KPI更新 → `metrics.md`
- 再発防止策の水平展開
</content>

### `~/.claude/quality/gates.md`:
<content>
# 品質ゲート定義 (ISO9001 §8.3/§8.5/§8.6)

タスク進行は以下5ゲートを順に通過すること。未通過での次段階進行は禁止。

## G1: 受入基準（Plan完了）
- 完了条件が明文化されている
- リスク判定済み（🟢🟡🟠🔴）
- 影響範囲が特定されている

## G2: テスト先行（TDD）
- テストが先に書かれている
- テスト失敗を確認済み
- テストをコミット済み

## G3: 実装完了
- 全テストがPASS（vitest）
- コード変更が`git diff`で確認済み
- 1コミット = 1機能/1修正

## G4: E2E検証
- `e2e_test.sh` 全件PASS
- 6Phaseループ該当箇所PASS（UI変更時）

## G5: 本番検証（デプロイ時のみ）
- `deploy-protocol.md` 全チェック完了
- ロールバック手順確認済み
- 本番API疎通確認済み
</content>

### `~/.claude/quality/risks.md`:
<content>
# リスク登録簿 (ISO9001 §6.1)

変更前に必ずリスク判定を実施し、対策レベルに従う。

## リスクマトリクス（影響×発生→対策）
|  | 影響:小（局所） | 影響:中（機能） | 影響:大（全体） |
|---|---|---|---|
| 高頻度 | 🟡標準 | 🟠強化 | 🔴最高 |
| 中頻度 | 🟢通常 | 🟡標準 | 🟠強化 |
| 低頻度 | 🟢通常 | 🟢通常 | 🟡標準 |

## 対策レベル
- 🟢 **通常**: 標準フローで実施
- 🟡 **標準**: git commit で保存後に着手
- 🟠 **強化**: 影響分析必須 + テスト強化
- 🔴 **最高**: Worktree必須 + ロールバック手順事前確認

## リスク登録簿
| リスク | 影響 | 対策 |
|---|---|---|
| AIハルシネーション | 中 | バリデーション+強制上書き |
| DB(D1)スキーマ変更 | 大 | 🔴 Worktree+バックアップ |
| cron変更（5本上限） | 大 | 🔴 影響分析+ロールバック |
| KVキー競合 | 中 | Grep確認ルール |
| 外部API障害 | 中 | フォールバック確認 |
| デプロイ障害 | 大 | 🔴 E2E Gate+即時ロールバック |
</content>

### `~/.claude/quality/nonconformity.md`:
<content>
# 不適合・是正処置 (ISO9001 §10.2)

バグ・障害・仕様逸脱が発生した場合、以下6ステップを実行する。

## 是正プロセス
1. **発見・修正**: 応急処置で影響を止める
2. **記録**: `tasks/` にタスク化（現象・影響範囲・発生条件を記載）
3. **根本原因分析**: 5Why（なぜ5回）で真因を特定
4. **是正実装**: 真因に対する恒久対策を実装（対症療法は不可）
5. **水平展開**: 同様の問題が他にないかGrepで横断チェック
6. **検証**: テスト追加 + E2E で再発しないことを確認

## エスカレーション
- 対症療法しかできない場合 → 不適合として再記録し、ユーザーに報告
- 同一root causeが3回発生 → 設計レビュー強制（アーキテクチャ見直し）
- 同じエラーが5回 → 別アプローチ検討（既存エラー対処プロトコル連携）
</content>

### `~/.claude/quality/metrics.md`:
<content>
# 品質KPI (ISO9001 §9.1/§10.3)

セッション終了時に測定・記録する。悪化傾向で改善アクションを実施。

## KPI定義
| # | KPI | 目標 | 測定方法 | 悪化時アクション |
|---|---|---|---|---|
| 1 | テスト通過率 | 100% | vitest + E2E結果 | 失敗テスト即修正 |
| 2 | デプロイ後障害 | ≤1回/月 | ロールバック実績 | deploy-protocol強化 |
| 3 | 不適合再発 | 0件 | tasks/done同一root cause | 設計レビュー実施 |
| 4 | 手戻り回数 | ≤2回/S | Phase1再スタート数 | Plan段階の精度向上 |
| 5 | 是正完了率 | ≥90% | 完了タスク/発生タスク | 未完了原因を分析 |
| 6 | E2E所要時間 | ≤3分 | e2e_test.sh実行時間 | テスト最適化 |

## 記録タイミング
- **セッション終了時**: 該当KPIをmemoryに記録
- **月次**: KPIトレンド分析 → 改善計画策定
</content>

### `~/.claude/quality/review.md`:
<content>
# 検証基準 — 3層検証 (ISO9001 §8.6/§9.1)

成果物は以下3層の検証を順に通過すること。層の飛ばし禁止。

## Layer 1: ユニットテスト
- `vitest` 全件PASS（既存テスト含む）
- 新機能にはテスト追加必須（TDD — G2準拠）
- 失敗時 → 修正してLayer 1を再実行

## Layer 2: E2Eテスト
- `bash e2e_test.sh` 全件PASS
- UI変更時は6Phaseデバッグループも実施
- 失敗時 → 修正してLayer 1から再実行

## Layer 3: 本番検証（デプロイ時のみ）
- `deploy-protocol.md` 全チェック実施
  - API疎通（/api/health）
  - 残高異常値チェック
  - 外部監視UP確認
- 失敗時 → ロールバック → 修正 → Layer 1から再実行

## 6Phaseループとの関係
Layer 2の拡張手順として、UI/機能変更時に `test-debug-loop-protocol.md` を適用する。
</content>

### `~/.claude/quality/docs.md`:
<content>
# 文書管理ルール (ISO9001 §7.5)

## 文書分類
- **維持する文書**（ルール・手順）: 常に最新状態を保つ
- **保持する記録**（実施の証拠）: 一定期間保存し追跡可能にする

## 維持する文書
| 文書 | 格納場所 | 管理方法 |
|---|---|---|
| 品質方針・目標 | `quality/policy.md` | git版管理 |
| CLAUDE.md群 | リポジトリ + ~/.claude/ | git版管理 |
| デプロイ手順 | `memory/deploy-protocol.md` | git版管理 |
| テスト手順 | `memory/test-debug-loop-protocol.md` | git版管理 |

## 保持する記録
| 記録 | 格納場所 | 保持期間 |
|---|---|---|
| テスト結果 | git log + CI | 永続 |
| デプロイ記録 | Notion + git tag | 12ヶ月 |
| 不適合・是正 | tasks/ → tasks/done/ | 12ヶ月 |
| 品質KPI | memory/ | セッション毎更新 |
| インシデント | /api/monitor + Notion | 12ヶ月 |

## 変更管理
- 文書変更はgitコミットで版管理（変更日・内容がgit logで追跡可能）
- 重要文書の変更はコミットメッセージに「docs:」プレフィックス
</content>

---

## 3. システム開発 知識ベース

システム開発に必要な10分野の専門知識リファレンスを導入します。
GitHubからリポジトリをクローンし、知識ファイルをコピーしてください。

```bash
# 1. リポジトリをクローン（一時ディレクトリ）
git clone https://github.com/akaganenakajima-jpg/claude-code-quality-framework.git /tmp/ccqf

# 2. 知識ベースをコピー
mkdir -p ~/.claude/knowledge/ipa
cp /tmp/ccqf/knowledge/ipa/*.md ~/.claude/knowledge/ipa/

# 3. 一時ディレクトリを削除
rm -rf /tmp/ccqf
```

Windows (Git Bash) の場合:
```bash
git clone https://github.com/akaganenakajima-jpg/claude-code-quality-framework.git "$TEMP/ccqf"
mkdir -p ~/.claude/knowledge/ipa
cp "$TEMP/ccqf/knowledge/ipa/"*.md ~/.claude/knowledge/ipa/
rm -rf "$TEMP/ccqf"
```

コピー後、以下の構成になっていることを確認してください:

```
~/.claude/knowledge/ipa/
├── index.md   ← 分野横断マップ・実務活用索引
├── fe.md      ← 基礎理論・CS（アルゴリズム・データ構造・離散数学・OS）
├── ap.md      ← 応用技術（待ち行列理論・パイプライン・SQL応用・EVM）
├── db.md      ← データベース（正規化・SQL高度技法・MVCC・分散DB）
├── nw.md      ← ネットワーク（OSPF/BGP・VPN/IPsec・SD-WAN・TLS）
├── es.md      ← 組込み・IoT（RTOS・安全設計・CAN/BLE/LoRa・TinyML）
├── pm.md      ← プロジェクト管理（PMBOK・EVM・CPM/PERT・アジャイル）
├── sm.md      ← ITサービス運用（ITIL4・SLA・MTBF/MTTR・BCP/DR）
├── st.md      ← IT戦略・経営（DX戦略・NPV/IRR・BSC・ビジネスモデル）
├── sa.md      ← アーキテクチャ（マイクロサービス・CQRS・DDD・性能設計）
└── au.md      ← 監査・内部統制（COSO・J-SOX・CAAT・COBIT・3線モデル）
```

### 活用マッピング

| 業務シーン | 参照ファイル |
|---|---|
| コードレビュー・アルゴリズム最適化 | `fe.md`, `ap.md` |
| DB設計・SQL最適化・トランザクション設計 | `db.md` |
| インフラ・NW設計・障害対応 | `nw.md` |
| セキュリティ設計・脅威分析 | `nw.md`, `au.md` |
| プロジェクト管理・見積り・進捗評価 | `pm.md` |
| 運用設計・SLA策定・障害管理 | `sm.md` |
| IT投資判断・DX戦略・ビジネス分析 | `st.md` |
| アーキテクチャ設計・技術選定 | `sa.md` |
| 組込み・IoTシステム設計 | `es.md` |
| 内部統制・コンプライアンス・監査対応 | `au.md` |

関連業務が発生した際に該当ファイルを参照することで、専門知識に基づいた設計判断・レビュー・助言が可能になります。

---

## 4. 推奨ツール設定（任意）

以下のMCPサーバーの導入を推奨として**ユーザーに提示**してください。
追加はユーザーの判断に委ねますが、**必ず一覧を表示して案内すること**。

### 4-1. 前提条件チェック（MCP導入前に必ず実行）

MCPサーバーは `npx` または `uvx` で起動するものが大半です。
**ユーザーに案内する前に、以下のコマンドで前提プログラムの有無を確認してください:**

```bash
# Node.js / npx（ほとんどのMCPで必要）
node --version && npx --version

# Python / uvx（一部のMCPで必要）
python3 --version 2>/dev/null || python --version 2>/dev/null
uvx --version 2>/dev/null || echo "uvx未インストール"
```

チェック結果をユーザーに報告した後、**不足があれば以下の選択肢を提示してください**（AskUserQuestion ツールを使用）:

**質問**: 「MCP実行に必要な前提プログラムが不足しています。自動インストールしますか？」

| 選択肢 | 動作 |
|--------|------|
| **🚀 全て自動インストール** | 不足分を全てインストールしてからMCP案内に進む |
| **📋 不足一覧だけ表示** | インストール手順を表示し、ユーザーに任せる |
| **⏭️ スキップ** | MCP設定をスキップして検証（セクション5）に進む |

「全て自動インストール」が選択された場合、OSを判定して以下を実行してください:

**Linux / macOS:**
```bash
# Node.js (未インストール時のみ)
if ! command -v node &>/dev/null; then
  curl -fsSL https://fnm.vercel.app/install | bash
  source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null
  fnm install --lts && fnm use lts-latest
fi

# uv + uvx (未インストール時のみ)
if ! command -v uvx &>/dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  source $HOME/.local/bin/env 2>/dev/null
fi
```

**Windows (Git Bash):**
```bash
# Node.js (未インストール時のみ — wingetが使える場合)
if ! command -v node &>/dev/null; then
  winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
  echo "⚠️ Node.jsをインストールしました。ターミナルを再起動してPATHを反映してください。"
fi

# uv + uvx (未インストール時のみ)
if ! command -v uvx &>/dev/null; then
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  echo "⚠️ uvをインストールしました。ターミナルを再起動してPATHを反映してください。"
fi
```

**⚠️ 重要**: インストール後に `node --version` / `uvx --version` で成功を確認してから次に進むこと。
PATHが反映されない場合は「ターミナルを再起動してください」とユーザーに案内すること。

全て成功した場合、またはチェック時点で不足がない場合は、そのまま 4-2 に進む。

### 4-2. MCPサーバー選択

まず以下の一覧をユーザーに表示してください:

| # | MCP | 概要 | 品質管理での活用 | 前提 |
|---|-----|------|----------------|------|
| 1 | **Notion** ⭐ | ドキュメント自動記録・検索 | レポート・インシデント記録の自動保存 | npx |
| 2 | **Context7** ⭐ | ライブラリドキュメント自動参照 | 「既存の解決策を使う」原則の実践支援 | npx |
| 3 | **Claude Preview** ⭐ | Webページのスクリーンショット確認 | UI検証の3層検証Layer2 | 不要（標準搭載） |
| 4 | **Windows MCP** | Windows操作の自動化（ウィンドウ/プロセス/レジストリ） | 開発環境の自動構築・検証 | npx |
| 5 | **Desktop Commander** | ファイル操作・ターミナル・プロセス管理 | 運用自動化・バッチ処理 | npx |
| 6 | **PDF** | PDF読み取り・作成・結合・分割 | 設計書・仕様書の自動処理 | npx |
| 7 | **GitHub** | Issue・PR・コード検索・Actions連携 | GitHub Flow・CI/CD管理 | npx + GitHub Token |
| 8 | **Figma** | デザインファイル参照 | 設計・開発管理 | npx + Figma APIキー |

（⭐ = 推奨）

次に、**AskUserQuestion ツール**で以下の選択肢を提示してください:

**質問**: 「導入するMCPサーバーを選んでください（⭐は推奨）」

| 選択肢 |
|--------|
| ⭐ 推奨3つを導入（Notion + Context7 + Claude Preview） |
| 🔧 全8つを導入 |
| 📝 個別に選ぶ |
| ⏭️ スキップ（MCPは後で設定する） |

**「個別に選ぶ」が選択された場合**、8つのMCPそれぞれについて順番にAskUserQuestionで「導入する / スキップ」を聞いてください。

### 4-3. 前提条件セットアップ & GUI導入案内

MCPサーバーはClaude CodeのGUI（設定画面）から追加するのが最も確実です。
ここでは**選択されたMCPの前提条件を整え**、**GUI操作手順を案内**してください。

#### Step 1: 選択されたMCPの前提条件を確認・インストール

選択されたMCPに応じて、必要な前提条件を自動セットアップしてください:

| MCP | 前提条件 | セットアップ |
|-----|---------|-------------|
| Notion | npx (Node.js) | 4-1で確認済み。不足なら `fnm install --lts` |
| Context7 | npx (Node.js) | 同上 |
| Claude Preview | なし | セットアップ不要（標準搭載） |
| Windows MCP | npx (Node.js) | 同上 |
| Desktop Commander | npx (Node.js) | 同上 |
| PDF | npx (Node.js) | 同上 |
| GitHub | npx (Node.js) + **GitHub Token** | Token取得手順を案内（下記参照） |
| Figma | npx (Node.js) + **Figma APIキー** | APIキー取得手順を案内（下記参照） |

**APIキー/トークンが必要なMCPが選択された場合**、以下の手順をユーザーに案内してください:

- **GitHub Token**: `https://github.com/settings/tokens` → Generate new token (classic) → `repo` スコープを付与
- **Figma APIキー**: `https://www.figma.com/developers/api#access-tokens` → Personal Access Token を生成
- **Notion Token**: `https://www.notion.so/my-integrations` → New integration → Internal Integration Token をコピー

前提条件が全て整ったことを確認したら、npxパッケージの事前ダウンロードを実行してください:

```bash
# 選択されたMCPのパッケージを事前ダウンロード（初回起動を高速化）
npx -y @notionhq/notion-mcp-server --help 2>/dev/null
npx -y @upstash/context7-mcp --help 2>/dev/null
# ↑ 選択されたMCPのみ実行すること
```

#### Step 2: GUI操作手順を案内

前提条件のセットアップ完了後、以下の手順をユーザーに表示してください:

```
📋 MCPサーバーのGUI追加手順:

1. Claude Code の設定を開く（左下の歯車アイコン or Ctrl+Shift+,）
2. 「MCP Servers」セクションを選択
3. 以下のMCPを名前で検索して「追加」:

   ✅ Notion        → 検索: "Notion"
   ✅ Context7       → 検索: "Context7"
   ✅ Claude Preview → 追加不要（標準搭載）
   ✅ Windows MCP    → 検索: "Windows"
   ✅ Desktop Commander → 検索: "Desktop Commander"
   ✅ PDF            → 検索: "PDF"
   ✅ GitHub         → 検索: "GitHub"（Token入力を求められます）
   ✅ Figma          → 検索: "Figma"（APIキー入力を求められます）

4. 追加後、各MCPの「接続」ボタンでステータスが ✅ になることを確認
```

（⚠️ 上記は選択されたMCPのみ表示すること。スキップしたものは含めない）

#### Step 3: 導入結果の確認

ユーザーがGUIからMCPを追加したら、結果を確認して報告してください:
```
✅ Notion — 接続OK
✅ Context7 — 接続OK
✅ Claude Preview — 標準搭載
✅ Windows MCP — 接続OK
✅ Desktop Commander — 接続OK
✅ PDF — 接続OK
⏭️ GitHub — スキップ
⏭️ Figma — スキップ
```

**MCPがGUIに見つからない場合**の代替手段として、`~/.claude/settings.json` に手動追加する方法を案内してください:
```json
// ~/.claude/settings.json の "mcpServers" に追記
"context7": {
  "command": "npx",
  "args": ["-y", "@upstash/context7-mcp"]
}
```
（追加後は Claude Code の再起動が必要: Ctrl+C → 再度起動）

### 4-4. MCP導入時のトラブルシューティング

MCPサーバー追加後にエラーが出た場合、以下を順にチェックしてユーザーに案内してください:

| エラーパターン | 原因 | 対処 |
|--------------|------|------|
| `npx: command not found` | Node.js未インストール | 4-1に戻って自動インストールを実行 |
| `uvx: command not found` | uv未インストール | 4-1に戻って自動インストールを実行 |
| `EACCES: permission denied` | グローバルnpmの権限不足 | `npm config set prefix ~/.npm-global` + PATH追加 |
| `Error: Cannot find module` | npxキャッシュ破損 | `npx --yes clear-npx-cache` → 再試行 |
| `ETIMEOUT` / `ECONNREFUSED` | ネットワーク/プロキシ | `npm config set proxy` でプロキシ設定 |
| `401 Unauthorized` | APIキー未設定/期限切れ | 該当サービスでキーを再発行 |
| `spawn UNKNOWN` (Windows) | パスにスペース含む | パスをダブルクォートで囲む |
| MCP起動後すぐ切断 | ポート競合 or メモリ不足 | `lsof -i :PORT` で競合確認、不要プロセスをkill |

**エラーが解決できない場合**はAskUserQuestionで「リトライ / このMCPをスキップ / MCP設定を全てスキップ」の3択を提示してください。

全MCPの導入が完了（またはスキップ）したら、次のセクション（検証）に進んでください。

---

## 5. 検証

全ファイルが正しく配置されたか確認してください:

1. `~/.claude/CLAUDE.md` が存在し、「品質管理 (ISO9001:2015準拠)」セクションが含まれている
2. `~/.claude/quality/` フォルダに以下の8ファイルが存在する:
   - `policy.md`, `process.md`, `gates.md`, `risks.md`
   - `nonconformity.md`, `metrics.md`, `review.md`, `docs.md`
3. 各ファイルの先頭行がISO9001の条項番号を含んでいる
4. `~/.claude/knowledge/ipa/` フォルダに11ファイルが存在する:
   - `index.md`, `fe.md`, `ap.md`, `db.md`, `nw.md`
   - `es.md`, `pm.md`, `sm.md`, `st.md`, `sa.md`, `au.md`
5. セクション4で選択したMCPの前提条件が整っている（スキップした場合は省略）

全て確認できたら、以下の形式でセットアップ結果をユーザーに表示してください:

```
## ✅ セットアップ完了

| コンポーネント | 状態 |
|--------------|------|
| CLAUDE.md（グローバルルール） | ✅ |
| 品質管理ファイル（8個） | ✅ |
| 知識ベース（11ファイル） | ✅ |
| MCP前提条件（Node.js/npx） | ✅ / ⏭️ |
| MCP: Notion | ✅ 前提OK・GUI案内済 / ⏭️ |
| MCP: Context7 | ✅ 前提OK・GUI案内済 / ⏭️ |
| MCP: Claude Preview | ✅（標準搭載） |
| MCP: Windows MCP | ✅ 前提OK・GUI案内済 / ⏭️ |
| MCP: Desktop Commander | ✅ 前提OK・GUI案内済 / ⏭️ |
| MCP: PDF | ✅ 前提OK・GUI案内済 / ⏭️ |
| MCP: GitHub | ✅ 前提OK・GUI案内済 / ⏭️ |
| MCP: Figma | ✅ 前提OK・GUI案内済 / ⏭️ |

💡 MCPサーバー本体は上記のGUI手順で追加してください。
   追加後に Claude Code を再起動すると利用可能になります。
```
