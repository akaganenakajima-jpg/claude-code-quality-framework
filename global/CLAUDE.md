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

## 知識ベース自動参照（`~/.claude/knowledge/`）
以下の業務・キーワードを検知したら、該当する知識ファイルを **Read して参照してから** 作業する。

### システム開発（`~/.claude/knowledge/ipa/`）
| トリガー（業務・キーワード） | 参照ファイル |
|---|---|
| DB設計・テーブル変更・インデックス・SQL最適化・正規化 | `ipa/db.md` |
| アーキテクチャ設計・マイクロサービス・可用性・キャッシュ・移行 | `ipa/sa.md` |
| NW設計・VPN・DNS・TLS・帯域・CDN・障害切り分け | `ipa/nw.md` |
| 運用設計・SLA・インシデント管理・BCP/DR・ITIL | `ipa/sm.md` |
| 監査・内部統制・ログ証跡・コンプライアンス・J-SOX | `ipa/au.md` |
| プロジェクト管理・見積り・EVM・スケジュール・リスク分析 | `ipa/pm.md` |
| IT投資判断・ROI/NPV・DX戦略・ビジネス分析・BSC | `ipa/st.md` |
| アルゴリズム最適化・計算量・データ構造・ソート | `ipa/fe.md` |
| 待ち行列・パイプライン・セキュリティ設計・暗号 | `ipa/ap.md` |
| 組込み・IoT・RTOS・安全設計・センサー | `ipa/es.md` |
| コードレビュー・設計レビュー（横断的） | `ipa/index.md` → 該当分野を特定 |

### 統計検定1級（`~/.claude/knowledge/stats/`）
| トリガー（業務・キーワード） | 参照ファイル |
|---|---|
| 確率分布・確率論・極限定理・不等式 | `stats/prob.md` |
| 統計的推測・検定・信頼区間・MLE・UMVUE | `stats/inference.md` |
| 多変量解析・PCA・因子分析・判別分析・SEM | `stats/multivariate.md` |
| 時系列解析・ARIMA・スペクトル・カルマンフィルター | `stats/ts.md` |
| ベイズ統計・MCMC・階層ベイズ・変分推論 | `stats/bayes.md` |
| 回帰分析・GLM・ロジスティック・生存時間解析 | `stats/regression.md` |
| 実験計画法・ANOVA・ノンパラメトリック・ブートストラップ | `stats/doe.md` |
| 確率過程・マルコフ連鎖・待ち行列・因果推論 | `stats/stochastic.md` |
| 機械学習理論・SVM・アンサンブル・EM・カーネル法 | `stats/ml.md` |

### DS発展・DSエキスパート（`~/.claude/knowledge/ds-advanced/`, `ds-expert/`）
| トリガー（業務・キーワード） | 参照ファイル |
|---|---|
| ETL・データクレンジング・前処理・特徴量エンジニアリング | `ds-advanced/data-engineering.md` |
| EDA・可視化・ダッシュボード・A/Bテスト設計 | `ds-advanced/analytics.md` |
| 予測モデル構築・CRISP-DM・MLOps・SHAP/LIME | `ds-advanced/modeling.md` |
| データ倫理・個人情報保護・GDPR・公平性 | `ds-advanced/ethics.md` |
| 高度モデリング・因果推論実践・強化学習・深層学習 | `ds-expert/advanced-modeling.md` |
| 空間統計・ネットワーク分析・NLP高度・推薦システム | `ds-expert/deep-analytics.md` |
| MLシステム設計・Feature Store・モデルサービング | `ds-expert/system-design.md` |
| ビジネスKPI・ROI計算・実験設計 | `ds-expert/business.md` |

### DS数学ストラテジスト上級（`~/.claude/knowledge/math-strategist/`）
| トリガー（業務・キーワード） | 参照ファイル |
|---|---|
| 線形代数・固有値・SVD・行列微分・テンソル | `math-strategist/linear-algebra.md` |
| 微積分・最適化・勾配降下法・KKT条件・凸最適化 | `math-strategist/calculus-optimization.md` |
| 確率不等式・情報理論・エントロピー・KLダイバージェンス | `math-strategist/probability-stats.md` |
| グラフ理論・数値計算・フーリエ解析・モンテカルロ | `math-strategist/applied-math.md` |

### E資格（`~/.claude/knowledge/e-cert/`）
| トリガー（業務・キーワード） | 参照ファイル |
|---|---|
| NN基礎・誤差逆伝播・活性化関数・正則化・初期化 | `e-cert/dl-fundamentals.md` |
| CNN・RNN・Transformer・生成モデル・GNN | `e-cert/dl-architectures.md` |
| 最適化アルゴリズム・分散学習・転移学習・LoRA・量子化 | `e-cert/dl-training.md` |
| 物体検出・セグメンテーション・NLP応用・音声・強化学習 | `e-cert/dl-applications.md` |

### Python3エンジニア認定基礎（`~/.claude/knowledge/python3/`）
| トリガー（業務・キーワード） | 参照ファイル |
|---|---|
| Python構文・データ型・リスト/辞書/集合・関数・ジェネレータ | `python3/core-syntax.md` |
| 標準ライブラリ・itertools/functools・asyncio・pathlib | `python3/stdlib.md` |
| クラス設計・継承・ダンダーメソッド・例外処理・メタクラス | `python3/oop.md` |
| PEP8・Pythonic・pytest・パッケージ管理・パフォーマンス | `python3/best-practices.md` |

- 複数分野にまたがる場合は各 `index.md` の横断マップで参照先を決定
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
