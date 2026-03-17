# Claude Code 品質フレームワーク セットアップ

以下の指示に従って、品質管理フレームワークの全ファイルを作成してください。
各ファイルの内容は `<content>` タグ内にそのまま記載されています。
全て完了したら検証を実施してください。

---

## 1. グローバルルール

`~/.claude/CLAUDE.md` に以下を書き込んでください:

<content>
この内容は `global/CLAUDE.md` と同一です。
セットアップ時は `global/CLAUDE.md` をそのまま `~/.claude/CLAUDE.md` にコピーしてください。

```bash
cp global/CLAUDE.md ~/.claude/CLAUDE.md
```
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
| デプロイ手順 | `memory/deploy-protocol.md` | git版管理（プロジェクト毎に作成） |
| テスト手順 | `memory/test-debug-loop-protocol.md` | git版管理（プロジェクト毎に作成） |

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

## 3. 開発プラクティス・コマンド・Hook

### 3-1. 開発プラクティス（6ファイル）

CLAUDE.mdから分離した実装ルール群。コードを書く・変えるタスクで横断チェック「📏 コード品質」が発火すると参照される。

```bash
mkdir -p ~/.claude/knowledge/practices
cp knowledge/practices/*.md ~/.claude/knowledge/practices/
```

配置後の構成:
```
~/.claude/knowledge/practices/
├── index.md            ← 索引 + 課題→ファイルマッピング
├── coding-style.md     ← 命名・関数設計・エラー処理
├── security.md         ← 入力検証・認証認可・秘密管理
├── testing.md          ← TDD手順 + 予測モデル検証（非TDD）+ カバレッジ
├── git-workflow.md     ← ブランチ戦略・コミット規約・PR
└── dev-workflow.md     ← 調査→計画→実装→レビュー（PDCA対応）
```

### 3-2. スラッシュコマンド（4ファイル）

```bash
mkdir -p ~/.claude/commands
cp commands/*.md ~/.claude/commands/
```

| コマンド | 用途 |
|---|---|
| `/5s` | 作業開始前の5Sチェック（git status + リソース確認） |
| `/knowledge` | 課題分析→知識ファイル一括参照→要約 |
| `/quality-review` | PDCA完了状況チェック |
| `/risk` | git diff分析→リスクレベル自動判定 |

### 3-3. Hook（コミット前リスク判定リマインダー）

```bash
mkdir -p ~/.claude/hooks
cp hooks/process-gate.py ~/.claude/hooks/
```

`~/.claude/settings.json` に以下を追加（既存設定とマージ）:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python ~/.claude/hooks/process-gate.py"
          }
        ]
      }
    ]
  }
}
```

> Windows の場合: `command` のパスを `python C:/Users/<username>/.claude/hooks/process-gate.py` に変更

---

## 4. 知識ベース

7分野の専門知識リファレンスを導入します。
GitHubからリポジトリをクローンし、知識ファイルをコピーしてください。

```bash
# 1. リポジトリをクローン（一時ディレクトリ）
git clone https://github.com/akaganenakajima-jpg/claude-code-quality-framework.git /tmp/ccqf

# 2. 知識ベースをコピー
for dir in ipa stats ds-advanced ds-expert math-strategist e-cert python3; do
  mkdir -p ~/.claude/knowledge/$dir
  cp /tmp/ccqf/knowledge/$dir/*.md ~/.claude/knowledge/$dir/
done

# 3. 一時ディレクトリを削除
rm -rf /tmp/ccqf
```

Windows (Git Bash) の場合:
```bash
git clone https://github.com/akaganenakajima-jpg/claude-code-quality-framework.git "$TEMP/ccqf"
for dir in ipa stats ds-advanced ds-expert math-strategist e-cert python3; do
  mkdir -p ~/.claude/knowledge/$dir
  cp "$TEMP/ccqf/knowledge/$dir/"*.md ~/.claude/knowledge/$dir/
done
rm -rf "$TEMP/ccqf"
```

コピー後、以下の構成になっていることを確認してください:

```
~/.claude/knowledge/
├── ipa/                    ← システム開発（10分野・11ファイル）
│   ├── index.md            ← 分野横断マップ・実務活用索引
│   ├── fe.md               ← 基礎理論・CS（アルゴリズム・データ構造・離散数学・OS）
│   ├── ap.md               ← 応用技術（待ち行列理論・パイプライン・SQL応用・EVM）
│   ├── db.md               ← データベース（正規化・SQL高度技法・MVCC・分散DB）
│   ├── nw.md               ← ネットワーク（OSPF/BGP・VPN/IPsec・SD-WAN・TLS）
│   ├── es.md               ← 組込み・IoT（RTOS・安全設計・CAN/BLE/LoRa・TinyML）
│   ├── pm.md               ← プロジェクト管理（PMBOK・EVM・CPM/PERT・アジャイル）
│   ├── sm.md               ← ITサービス運用（ITIL4・SLA・MTBF/MTTR・BCP/DR）
│   ├── st.md               ← IT戦略・経営（DX戦略・NPV/IRR・BSC・ビジネスモデル）
│   ├── sa.md               ← アーキテクチャ（マイクロサービス・CQRS・DDD・性能設計）
│   └── au.md               ← 監査・内部統制（COSO・J-SOX・CAAT・COBIT・3線モデル）
├── stats/                  ← 統計検定1級（9分野・10ファイル）
│   ├── index.md            ← 分野横断マップ
│   ├── prob.md             ← 確率論・確率分布
│   ├── inference.md        ← 統計的推測
│   ├── multivariate.md     ← 多変量解析
│   ├── ts.md               ← 時系列解析
│   ├── bayes.md            ← ベイズ統計
│   ├── regression.md       ← 回帰分析・GLM
│   ├── doe.md              ← 実験計画法・ノンパラメトリック
│   ├── stochastic.md       ← 確率過程・決定理論
│   └── ml.md               ← 統計的機械学習
├── ds-advanced/            ← DS発展（4分野・5ファイル）
│   ├── index.md            ← 分野横断マップ
│   ├── data-engineering.md ← データエンジニアリング・前処理
│   ├── analytics.md        ← 分析・可視化・A/Bテスト
│   ├── modeling.md         ← 予測モデル構築・MLOps
│   └── ethics.md           ← データ倫理・法規
├── ds-expert/              ← DSエキスパート（4分野・5ファイル）
│   ├── index.md            ← 分野横断マップ
│   ├── advanced-modeling.md ← 高度モデリング・因果推論
│   ├── deep-analytics.md   ← 空間統計・NLP・推薦
│   ├── system-design.md    ← MLシステム設計
│   └── business.md         ← ビジネス応用・KPI
├── math-strategist/        ← DS数学ストラテジスト上級（4分野・5ファイル）
│   ├── index.md            ← 分野横断マップ
│   ├── linear-algebra.md   ← 線形代数・行列理論
│   ├── calculus-optimization.md ← 微積分・最適化
│   ├── probability-stats.md ← 確率・情報理論
│   └── applied-math.md     ← 応用数学
├── e-cert/                 ← E資格（4分野・5ファイル）
│   ├── index.md            ← 分野横断マップ
│   ├── dl-fundamentals.md  ← 深層学習基礎
│   ├── dl-architectures.md ← アーキテクチャ（CNN/RNN/Transformer）
│   ├── dl-training.md      ← 学習・最適化技法
│   └── dl-applications.md  ← 応用（検出・NLP・音声・強化学習）
└── python3/                ← Python3基礎（4分野・5ファイル）
    ├── index.md            ← 分野横断マップ
    ├── core-syntax.md      ← 構文・データ型・関数
    ├── stdlib.md           ← 標準ライブラリ
    ├── oop.md              ← オブジェクト指向
    └── best-practices.md   ← PEP8・テスト・パフォーマンス
```

### 活用マッピング

| 業務シーン | 参照ファイル |
|---|---|
| コードレビュー・アルゴリズム最適化 | `ipa/fe.md`, `ipa/ap.md` |
| DB設計・SQL最適化・トランザクション設計 | `ipa/db.md` |
| インフラ・NW設計・障害対応 | `ipa/nw.md` |
| セキュリティ設計・脅威分析 | `ipa/nw.md`, `ipa/au.md` |
| プロジェクト管理・見積り・進捗評価 | `ipa/pm.md` |
| 運用設計・SLA策定・障害管理 | `ipa/sm.md` |
| IT投資判断・DX戦略・ビジネス分析 | `ipa/st.md` |
| アーキテクチャ設計・技術選定 | `ipa/sa.md` |
| 組込み・IoTシステム設計 | `ipa/es.md` |
| 内部統制・コンプライアンス・監査対応 | `ipa/au.md` |
| 統計分析・仮説検定・回帰分析 | `stats/inference.md`, `stats/regression.md` |
| 時系列予測・異常検知 | `stats/ts.md`, `stats/stochastic.md` |
| ベイズ推定・不確実性定量化 | `stats/bayes.md` |
| 機械学習モデル構築・評価 | `stats/ml.md`, `ds-advanced/modeling.md` |
| データ前処理・ETL・特徴量エンジニアリング | `ds-advanced/data-engineering.md` |
| EDA・可視化・ダッシュボード設計 | `ds-advanced/analytics.md` |
| データ倫理・プライバシー保護・GDPR | `ds-advanced/ethics.md` |
| 高度モデリング・因果推論・強化学習 | `ds-expert/advanced-modeling.md` |
| MLシステム設計・Feature Store・サービング | `ds-expert/system-design.md` |
| 線形代数・最適化・数値計算 | `math-strategist/linear-algebra.md`, `math-strategist/calculus-optimization.md` |
| 深層学習・CNN/RNN/Transformer | `e-cert/dl-architectures.md`, `e-cert/dl-training.md` |
| Python開発・テスト・パッケージ管理 | `python3/core-syntax.md`, `python3/best-practices.md` |

関連業務が発生した際に該当ファイルを参照することで、専門知識に基づいた設計判断・レビュー・助言が可能になります。

---

## 5. 前提プログラムのインストール & 推奨ツール案内

### 5-1. 前提プログラムの最新バージョンをリサーチ & インストール

MCPサーバーやビルドツールに必要な前提プログラムを確認・インストールします。
**バージョン要件は変わるため、WebSearchで最新の推奨バージョンを都度確認すること。**

#### 手順:

1. 現在の環境を確認:
```bash
node --version 2>/dev/null || echo "Node.js: 未インストール"
npx --version 2>/dev/null || echo "npx: 未インストール"
python3 --version 2>/dev/null || python --version 2>/dev/null || echo "Python: 未インストール"
uvx --version 2>/dev/null || echo "uvx: 未インストール"
```

2. **WebSearch** で以下の最新バージョンを取得（変数として保持）:
   - 「Node.js LTS latest version」 → `$NODE_LATEST`
   - 「Python latest stable version」 → `$PYTHON_LATEST`
   - 「uv (astral) latest version」 → `$UV_LATEST`
   - 「Windows MCP (darbotlabs) Python minimum version requirement」 → `$PYTHON_MIN_FOR_MCP`

   ※ Pythonは最新安定版と MCP動作要件（Windows MCP等）の両方を満たすバージョンを選定すること。
   　 `$PYTHON_LATEST` が `$PYTHON_MIN_FOR_MCP` 未満の場合は要件を満たすバージョンを優先する。

3. 環境チェック結果と最新バージョンを比較してユーザーに報告:
   - インストール済み → 最新かどうかをバージョン比較して ✅ or ⚠️（古い）
   - 未インストール → ⚠️ と最新バージョンを明示
   - Pythonは MCP動作要件も併記（例: 「最新安定版: X.Y.Z / Windows MCP要件: ≥X.Y」）

4. **不足・古いものがあれば AskUserQuestion** で選択肢を提示:

**質問**: 「前提プログラムの更新が必要です。自動インストールしますか？」

| 選択肢 | 動作 |
|--------|------|
| **🚀 全て自動インストール** | 不足・古いものを全て最新版でインストール |
| **📋 不足一覧だけ表示** | インストール手順を表示し、ユーザーに任せる |
| **⏭️ スキップ** | 検証（セクション5）に進む |

「全て自動インストール」が選択された場合、**WebSearchで取得した最新バージョンを指定して**インストール:

**Linux / macOS:**
```bash
# Node.js — fnm経由で最新LTSを指定インストール
if ! command -v node &>/dev/null || [[ "$(node --version)" != "v$NODE_LATEST"* ]]; then
  curl -fsSL https://fnm.vercel.app/install | bash
  source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null
  fnm install "$NODE_LATEST" && fnm use "$NODE_LATEST"
fi
# Python — pyenv経由で最新安定版を指定インストール
if ! command -v python3 &>/dev/null || [[ "$(python3 --version)" != *"$PYTHON_LATEST"* ]]; then
  if ! command -v pyenv &>/dev/null; then
    curl https://pyenv.run | bash
    export PATH="$HOME/.pyenv/bin:$PATH" && eval "$(pyenv init -)"
  fi
  pyenv install "$PYTHON_LATEST" && pyenv global "$PYTHON_LATEST"
fi
# uv/uvx — 公式インストーラ（常に最新を取得）
if ! command -v uvx &>/dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  source $HOME/.local/bin/env 2>/dev/null
fi
```

**Windows (Git Bash):**
```bash
# Node.js — wingetで最新LTSを指定インストール
if ! command -v node &>/dev/null || [[ "$(node --version)" != "v$NODE_LATEST"* ]]; then
  winget install OpenJS.NodeJS.LTS --version "$NODE_LATEST" --accept-source-agreements --accept-package-agreements
  echo "⚠️ Node.jsインストール完了。ターミナルを再起動してPATHを反映してください。"
fi
# Python — wingetで最新版を指定インストール
if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null || [[ "$(python3 --version 2>/dev/null || python --version)" != *"$PYTHON_LATEST"* ]]; then
  winget install Python.Python.3 --version "$PYTHON_LATEST" --accept-source-agreements --accept-package-agreements
  echo "⚠️ Pythonインストール完了。ターミナルを再起動してPATHを反映してください。"
fi
# uv/uvx — 公式インストーラ（常に最新を取得）
if ! command -v uvx &>/dev/null; then
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  echo "⚠️ uvインストール完了。ターミナルを再起動してPATHを反映してください。"
fi
```

5. インストール後に `--version` で**WebSearchで取得した最新バージョンと一致するか**確認すること。

### 5-2. 推奨ツール（参考情報）

MCPサーバーを追加すると、Claude Codeの機能を拡張できます。
推奨ツールの一覧は `recommended-tools.md` を参照してください。

⚠️ MCPの追加はこのセットアップの範囲外です。ユーザー自身で必要に応じて追加してください。

---

## 6. 検証

全ファイルが正しく配置されたか確認してください:

1. `~/.claude/CLAUDE.md` が存在し、「品質管理 (ISO9001:2015準拠)」セクションが含まれている
2. `~/.claude/quality/` フォルダに以下の8ファイルが存在する:
   - `policy.md`, `process.md`, `gates.md`, `risks.md`
   - `nonconformity.md`, `metrics.md`, `review.md`, `docs.md`
3. 各ファイルの先頭行がISO9001の条項番号を含んでいる
4. 開発プラクティスフォルダに以下の6ファイルが存在する:
   - `~/.claude/knowledge/practices/` — `index.md`, `coding-style.md`, `security.md`, `testing.md`, `git-workflow.md`, `dev-workflow.md`
5. コマンドフォルダに以下の4ファイルが存在する:
   - `~/.claude/commands/` — `5s.md`, `knowledge.md`, `quality-review.md`, `risk.md`
6. Hookファイルが存在する:
   - `~/.claude/hooks/process-gate.py`
7. 知識ベースフォルダに以下のファイルが存在する:
   - `~/.claude/knowledge/ipa/` — 11ファイル（`index.md`, `fe.md`, `ap.md`, `db.md`, `nw.md`, `es.md`, `pm.md`, `sm.md`, `st.md`, `sa.md`, `au.md`）
   - `~/.claude/knowledge/stats/` — 10ファイル（`index.md`, `prob.md`, `inference.md`, `multivariate.md`, `ts.md`, `bayes.md`, `regression.md`, `doe.md`, `stochastic.md`, `ml.md`）
   - `~/.claude/knowledge/ds-advanced/` — 5ファイル（`index.md`, `data-engineering.md`, `analytics.md`, `modeling.md`, `ethics.md`）
   - `~/.claude/knowledge/ds-expert/` — 5ファイル（`index.md`, `advanced-modeling.md`, `deep-analytics.md`, `system-design.md`, `business.md`）
   - `~/.claude/knowledge/math-strategist/` — 5ファイル（`index.md`, `linear-algebra.md`, `calculus-optimization.md`, `probability-stats.md`, `applied-math.md`）
   - `~/.claude/knowledge/e-cert/` — 5ファイル（`index.md`, `dl-fundamentals.md`, `dl-architectures.md`, `dl-training.md`, `dl-applications.md`）
   - `~/.claude/knowledge/python3/` — 5ファイル（`index.md`, `core-syntax.md`, `stdlib.md`, `oop.md`, `best-practices.md`）

全て確認できたら、以下の形式でセットアップ結果をユーザーに表示してください:

```
## ✅ セットアップ完了

| コンポーネント | 状態 |
|--------------|------|
| CLAUDE.md（グローバルルール） | ✅ |
| 品質管理ファイル（8個） | ✅ |
| 開発プラクティス（6ファイル） | ✅ |
| スラッシュコマンド（4ファイル） | ✅ |
| Hook（process-gate.py） | ✅ |
| 知識ベース — IPA（11ファイル） | ✅ |
| 知識ベース — 統計検定1級（10ファイル） | ✅ |
| 知識ベース — DS発展（5ファイル） | ✅ |
| 知識ベース — DSエキスパート（5ファイル） | ✅ |
| 知識ベース — DS数学ストラテジスト上級（5ファイル） | ✅ |
| 知識ベース — E資格（5ファイル） | ✅ |
| 知識ベース — Python3基礎（5ファイル） | ✅ |
| 前提プログラム（Node.js/Python/uvx） | ✅ 確認済 / ⏭️ スキップ |

💡 MCPサーバーの追加は recommended-tools.md を参照してください。
```
