# Claude Code 品質フレームワーク セットアップ

以下の指示に従って、品質管理フレームワークの全ファイルをセットアップしてください。
各ファイルの内容は `<content>` タグ内にそのまま記載されています。
全て完了したら検証を実施してください。

---

## 0. インストールモード判定

まず、既存インストールの有無を確認してください。

### 判定方法

`~/.claude/CLAUDE.md` が存在するか確認する:
```bash
ls -la ~/.claude/CLAUDE.md 2>/dev/null && echo "EXISTING" || echo "NEW"
```

### 🆕 新規インストール（`~/.claude/CLAUDE.md` が存在しない）

→ **セクション1〜6を順番に実行**してください。

### 🔄 アップデート（`~/.claude/CLAUDE.md` が既に存在する）

既存インストールとの差分を確認し、変更があるファイルだけを更新します。

#### Step 0-1: content ファイルの差分チェック

以下の各ファイルについて、**既存ファイルを Read し、このプロンプト内の `<content>` ブロックと比較**してください:

| # | ファイルパス | セクション |
|---|---|---|
| 1 | `~/.claude/CLAUDE.md` | §1 |
| 2 | `~/.claude/quality/policy.md` | §2 |
| 3 | `~/.claude/quality/process.md` | §2 |
| 4 | `~/.claude/quality/gates.md` | §2 |
| 5 | `~/.claude/quality/risks.md` | §2 |
| 6 | `~/.claude/quality/nonconformity.md` | §2 |
| 7 | `~/.claude/quality/metrics.md` | §2 |
| 8 | `~/.claude/quality/review.md` | §2 |
| 9 | `~/.claude/quality/docs.md` | §2 |
| 10 | `~/.claude/knowledge/practices/index.md` | §3 |
| 11 | `~/.claude/knowledge/practices/coding-style.md` | §3 |
| 12 | `~/.claude/knowledge/practices/security.md` | §3 |
| 13 | `~/.claude/knowledge/practices/testing.md` | §3 |
| 14 | `~/.claude/knowledge/practices/git-workflow.md` | §3 |
| 15 | `~/.claude/knowledge/practices/dev-workflow.md` | §3 |
| 16 | `~/.claude/commands/5s.md` | §3 |
| 17 | `~/.claude/commands/knowledge.md` | §3 |
| 18 | `~/.claude/commands/quality-review.md` | §3 |
| 19 | `~/.claude/commands/risk.md` | §3 |
| 20 | `~/.claude/hooks/process-gate.py` | §3 |

比較結果を以下の形式でテーブルにまとめてください:

```
| ファイル | 状態 | 変更内容（差分がある場合） |
|---------|------|-------------------------|
| CLAUDE.md | ✅ 最新 / 🔄 変更あり / 🆕 新規 | 変更の概要 |
| ... | ... | ... |
```

#### Step 0-2: 知識ベースの差分チェック

```bash
# リポジトリをクローン
git clone https://github.com/akaganenakajima-jpg/claude-code-quality-framework.git /tmp/ccqf 2>/dev/null

# 知識ベースの差分を一括チェック
for dir in ipa stats ds-advanced ds-expert math-strategist e-cert python3 ux-psychology; do
  if [ -d ~/.claude/knowledge/$dir ]; then
    echo "=== $dir ==="
    diff -rq /tmp/ccqf/knowledge/$dir/ ~/.claude/knowledge/$dir/ 2>/dev/null || echo "(差分なし)"
  else
    echo "=== $dir === 🆕 新規（未インストール）"
  fi
done

# Apple HIG スキルの差分チェック
echo "=== apple-hig-designer ==="
if [ -d ~/.claude/skills/apple-hig-designer ]; then
  diff -rq /tmp/ccqf/skills/apple-hig-designer/ ~/.claude/skills/apple-hig-designer/ 2>/dev/null || echo "(差分なし)"
else
  echo "🆕 新規（未インストール）"
fi

rm -rf /tmp/ccqf
```

Windows (Git Bash) の場合:
```bash
git clone https://github.com/akaganenakajima-jpg/claude-code-quality-framework.git "$TEMP/ccqf" 2>/dev/null

for dir in ipa stats ds-advanced ds-expert math-strategist e-cert python3 ux-psychology; do
  if [ -d ~/.claude/knowledge/$dir ]; then
    echo "=== $dir ==="
    diff -rq "$TEMP/ccqf/knowledge/$dir/" ~/.claude/knowledge/$dir/ 2>/dev/null || echo "(差分なし)"
  else
    echo "=== $dir === 🆕 新規（未インストール）"
  fi
done

echo "=== apple-hig-designer ==="
if [ -d ~/.claude/skills/apple-hig-designer ]; then
  diff -rq "$TEMP/ccqf/skills/apple-hig-designer/" ~/.claude/skills/apple-hig-designer/ 2>/dev/null || echo "(差分なし)"
else
  echo "🆕 新規（未インストール）"
fi

rm -rf "$TEMP/ccqf"
```

#### Step 0-3: ユーザーに確認

差分チェック結果をまとめて、AskUserQuestion で以下を提示:

**質問**: 「インストール済みのフレームワークとの差分を検出しました。どのように更新しますか？」

| 選択肢 | 動作 |
|--------|------|
| **🔄 変更ファイルのみ更新** | 差分があるファイルと新規ファイルだけを書き込む。変更なしのファイルはスキップ |
| **🆕 全て上書き（フルインストール）** | セクション1〜6を通常通り全て実行 |
| **📋 差分一覧だけ表示** | 更新せず、差分の詳細を表示して終了 |

「変更ファイルのみ更新」が選択された場合:
- content ファイル: 差分があるものだけ該当セクションの `<content>` で上書き
- 知識ベース: 差分があるディレクトリだけ `git clone + cp` で更新
- §5（前提プログラム）と §6（検証）は常に実行

---

## 1. グローバルルール

`~/.claude/CLAUDE.md` に以下を書き込んでください:

<content>
# CLAUDE.md — グローバル設定（全プロジェクト共通）

> プロジェクト固有ルールは各リポジトリの `CLAUDE.md` を参照

## Conversation Guidelines
- 常に日本語で会話する

## GitHub Operations
- GitHubのリソース（リポジトリ、Issue、PR、コード等）を操作する際は、`gh` コマンド（GitHub CLI）を使用する
- WebFetchやWebSearchではなく、`gh` コマンドを優先する

## 品質管理 (ISO9001:2015準拠)
品質方針: 「証拠に基づき、正しく・安全に・持続的に動くシステムを提供する」
詳細・品質目標 → `~/.claude/quality/policy.md`

### PDCAゲート（全タスクに適用。省略禁止）
1. **Plan（計画）**: まず「何を作るか・何に影響するか・どうなったら完成か」を整理してから着手 → `quality/process.md`
2. **Do（実行）**: 先にテストを書く → テストが通るコードを書く → 品質チェックを通す → `quality/gates.md`（詳細手順 → `practices/testing.md`）
3. **Check（確認）**: 3段階で確認（ユニットテスト → 全体テスト → 本番で動作確認） → `quality/review.md`
4. **Act（改善）**: 問題が出たら → なぜ起きたか → 直す → 他にも同じ問題がないか確認 → `quality/nonconformity.md`

### リスク判定（変更前に必ず実施）→ `quality/risks.md`
- 🟢 低リスク: 新しいファイルを追加する・テストを増やす・コメントだけ直す
- 🟡 中リスク: 動いているコードを修正する・設定を変える（元に戻せる範囲）→ 先にコミットしてから着手
- 🟠 高リスク: 複数の画面や機能に影響する変更・外部連携の変更 → 影響範囲を洗い出してから着手
- 🔴 最高リスク: データベース構造の変更・定期実行の変更・本番公開 → 隔離環境（Worktree）で作業

### 品質記録
- バグや問題が発生 → `tasks/` にファイルを作り（原因・対応・横展開を記載）
- セッション終了時 → 品質KPI更新 → `quality/metrics.md`
- 文書管理ルール → `quality/docs.md`

## 5S — 新タスク開始前の準備（省略禁止）
新しいタスクに取り掛かる前に、必ず以下を実施する。

### 1. 片付け — 前のタスクの残骸がないか
- 裏で動きっぱなしのプロセスがないか確認（あれば止める）
- 前のタスクで作った一時ファイルが残っていたら削除

### 2. 現状確認 — 今どこにいるか
- 今どのブランチにいるか、保存していない変更がないか確認（`git status`）
- 作業フォルダが正しいか確認
- 必要なファイル・データが揃っているか確認

### 3. 健康チェック — PCが重くないか
- CPU / メモリ / ディスクの使用率を確認
- 異常（CPU高負荷が続く、メモリ80%超、ディスク90%超）があれば先に解決
- **手動で毎回対処するのではなく、仕組み（自動制限/監視）で解決する**

### 4. ルール確認 — 設定は最新か
- プロジェクトの CLAUDE.md / memory が最新か確認
- 前のタスクで学んだことがメモリに記録されているか確認

### 5. 手順開始 — やることリストを作る
- タスク管理（TodoWrite）を開始
- 必要ならタスクファイル（`tasks/`）を作成

## 知識ベース自動参照
タスクを受けたら（またはこれから自分が作業するとき）、**課題の本質を分析**し、該当する知識ファイルを Read してから作業する。

### Step 1: 大分類 — 「何をする課題か？」（複数該当OK）

| 大分類 | 判断基準 | 参照ファイル |
|---|---|---|
| 🏗️ つくる | ソフトウェア・システム・APIなどを設計・実装する | `ipa/sa.md`（構成）, `ipa/ap.md`（実装）, `python3/`（言語） |
| 🗄️ 貯める・出す | データを保存・検索・構造化する | `ipa/db.md` |
| 🌐 つなぐ | 機器・サービス同士を通信させる | `ipa/nw.md` |
| 📊 数字で理解する | データを分析・集計・可視化して意味を読み取る | `stats/prob.md`, `stats/inference.md`, `ds-advanced/analytics.md` |
| 🔮 予測・発見する | 未来を予測する/パターンを見つける/原因を特定する | `stats/regression.md`, `stats/ts.md`, `stats/multivariate.md`, `stats/ml.md` |
| 🤖 AIに任せる | 機械学習・深層学習で自動化する | `ds-advanced/modeling.md`, `e-cert/` → `index.md` |
| 🧪 比べる・試す | A/Bテスト・実験・効果検証・因果推論 | `stats/doe.md`, `stats/bayes.md`, `stats/stochastic.md` |
| 🚀 届ける・動かす | 本番デプロイ・CI/CD・MLOps・監視・障害対応 | `ipa/sm.md`, `ds-expert/system-design.md` |
| 📋 まわす | プロジェクト管理・スケジュール・体制・見積もり | `ipa/pm.md` |
| 💰 決める | 投資判断・費用対効果・経営報告・KPI設計 | `ipa/st.md`, `ds-expert/business.md` |
| 🧹 整える | データ前処理・クレンジング・ドキュメント整備 | `ds-advanced/data-engineering.md` |
| 🔌 組み込む | ハードウェア制御・IoT・センサー・リアルタイム処理 | `ipa/es.md` |
| 🎨 UIを設計する | 画面設計・レイアウト・UX改善・コンバージョン最適化 | `ux-psychology/` → `index.md` |

### Step 2: 横断チェック — 「どの課題でも確認すべき観点」

大分類で知識ファイルを引いた後、以下を**全タスクに対してチェック**する。該当したら追加で参照する。

| 観点 | 問い | 該当したら参照 |
|---|---|---|
| 🛡️ 安全 | 攻撃される可能性は？認証・認可は必要？ | `ipa/ap.md` + `ipa/au.md` |
| ⚖️ 倫理・法令 | 個人情報を扱う？公平性は？法的リスクは？ | `ds-advanced/ethics.md` |
| ⚡ 性能 | 遅くならない？リソースは足りる？ | `ipa/fe.md` |
| ✅ テスト | どうやって正しさを確認する？ | `python3/best-practices.md` §5 |
| 📝 伝達 | 結果を人に説明する必要がある？ | `ds-advanced/analytics.md`, `ds-expert/business.md` |
| 🔢 数学的裏付け | 理論的な根拠が必要？ | `math-strategist/` → `index.md` |
| 📏 コード品質 | コードを書く・変える？ | `practices/` → `index.md` |
| 🎨 UX心理学 | UIを設計・レビューする？ユーザー行動に影響する？ | `ux-psychology/` → `index.md` |

### 参照ルール
- 大分類は**複数該当するのが普通**。全て参照する
- 横断チェックは**毎回全項目を走査**する（該当なしならスキップ）
- 知識ファイルの具体的なセクション番号（§）を引用して根拠を示す
- 分類に迷ったら各分野の `index.md` の横断マップで確認する
- 知識ファイルの内容が自身の学習済み知識と**矛盾する場合、その旨をユーザーに報告**し、どちらが正しいか判断を仰ぐ

## UI デザインのデフォルト
- UI/フロントエンドを作成・修正する場合、**デフォルトで Apple HIG スタイルを適用**する
- `~/.claude/skills/apple-hig-designer/SKILL.md` を参照し、SF Pro Typography・System Colors・8pt Grid に準拠する
- 心理学的根拠が必要な場合は `ux-psychology/` → `index.md` を併用する
- ユーザーが別のスタイル（Material Design等）を明示的に指定した場合のみ、HIG 以外を使用する

## 開発の考え方
### 作り始める前に必ず確認
- 同じ機能が既にコードベースのどこかにないか探す
- 使っているライブラリに同じ機能がないか確認する
- Context7 MCP でライブラリのドキュメントを参照する
- **「自分で作る」より「既にあるものを使う」を優先する**

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

### テスト・開発フロー・セキュリティ
- TDD手順・予測モデル検証・カバレッジ → `practices/testing.md`
- ブランチ戦略・コミット規約・PR・ロールバック → `practices/git-workflow.md`
- 入力検証・認証認可・秘密管理・ログ安全性 → `practices/security.md`
- コーディングスタイル・命名・関数設計 → `practices/coding-style.md`
- 調査→計画→実装→レビューの全体フロー → `practices/dev-workflow.md`

## 困ったときのルール
- **コマンドが3分返ってこない**: 止めて原因を調べる。何が起きたか報告する
- **同じエラーが5回続く**: 同じやり方を繰り返さない。「何を試した / なぜダメだった / 次にどうする」を報告する
- **大きく変える前に保存**: リファクタリングや大改修の前に、今の状態をコミットして戻れるようにする
- **変えた後は確認**: 修正したら差分を見て、何が変わったかユーザーに要点を報告する

## サブエージェントの使い分け
別のエージェントに任せるとき:
- 調べることが3つ以上あって、同時に進められる場合
- 重い検索で会話の流れを止めたくない場合
- 時間がかかる処理をバックグラウンドで走らせたい場合

自分でやるとき:
- どのファイルか分かっていて、すぐ見つかる場合
- 2〜3ファイルの読み書きで終わる場合

## Claude Code の注意点
- `preview_eval` で `return` を使う場合は即時関数 `(function(){ ... return ...; })()` で包む
- スマホ表示の確認は `preview_resize preset:mobile` を使う

## Claude Code 高度機能の活用

### Worktrees — 「壊しても大丈夫な別世界」で作業する
- 大きな変更や実験をする時は、隔離環境（Worktree）を提案する
- 本番は常に安全な状態を保つ。失敗してもworktreeを消すだけで元通り
- こう言われたら提案する:
  - 「試しに〜してみたい」「大幅に変えたい」「壊れても構わないから試して」

### Headless mode — Claudeを自動実行する
- `env -u CLAUDECODE claude -p "プロンプト"` でスクリプトから呼び出せる
- こう言われたら提案する:
  - 「毎日自動でやりたい」「定期実行したい」「APIの結果を自動分析したい」
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

## 3. 開発プラクティス（6ファイル）・コマンド（4ファイル）・Hook（1ファイル）

CLAUDE.mdから分離した実装ルール群。コードを書く・変えるタスクで横断チェック「📏 コード品質」が発火すると参照される。

### `~/.claude/knowledge/practices/index.md`:
<content>
# practices/ — 開発プラクティス索引

> **プロジェクト CLAUDE.md の指定が優先**。ここは汎用デフォルト。

## ファイル一覧

| ファイル | 内容 | 関連IPA知識 |
|---|---|---|
| `coding-style.md` | 命名・関数設計・エラー処理・ファイル構成 | `ipa/ap.md` §SOLID |
| `security.md` | 入力検証・認証認可・秘密管理・ログ・インシデント対応 | `ipa/ap.md` + `ipa/au.md` |
| `testing.md` | TDD手順・予測モデル検証・カバレッジ戦略 | `ipa/sm.md` §テスト管理 |
| `git-workflow.md` | ブランチ戦略・コミット規約・PR・ロールバック | `ipa/pm.md` §構成管理 |
| `dev-workflow.md` | 調査→計画→実装→レビュー（PDCA対応） | `quality/process.md` |

## 課題→ファイル逆引き

| やりたいこと | 参照ファイル |
|---|---|
| コードを書く・変える | `coding-style.md` → `security.md` → `testing.md` |
| バグを直す | `testing.md` §バグ修正手順 → `dev-workflow.md` |
| 新機能を追加する | `dev-workflow.md` → `coding-style.md` → `testing.md` |
| PRを出す・レビューする | `git-workflow.md` → `testing.md` §カバレッジ |
| リファクタリングする | `coding-style.md` → `testing.md` §回帰テスト → `git-workflow.md` |
| デプロイする | `git-workflow.md` §ロールバック → `security.md` §インシデント対応 |
| 予測モデルを作る | `testing.md` §予測モデル検証（TDDではない） |
</content>

### `~/.claude/knowledge/practices/coding-style.md`:
<content>
# コーディングスタイル

> **プロジェクト CLAUDE.md の指定が優先**。ここは汎用デフォルト。

## 1. 基本原則
- 自明なコードコメントは書かない（コード自体が説明になるよう命名する）
- 不要な空白は削除する
- 新規ファイルは必ず末尾に改行を入れる
- 「自分で作る」より「既にあるものを使う」を優先する

## 2. 命名規則
- **変数・関数**: 何をするか/何を表すかが名前だけで分かること
- **真偽値**: `is`, `has`, `can`, `should` プレフィックス
- **定数**: UPPER_SNAKE_CASE
- **略語禁止**: `cnt` → `count`, `mgr` → `manager`（ドメイン用語は例外）

## 3. 関数設計（SOLID原則準拠 — `ipa/ap.md` §6）
- **単一責任**: 1関数 = 1つの仕事。20行を超えたら分割を検討
- **開放閉鎖**: 既存コードを変えずに拡張できる設計
- **依存性逆転**: 具象ではなく抽象に依存する
- **副作用の明示**: 状態を変更する関数は名前で明示（`updateX`, `deleteY`）

## 4. エラー処理
- **早期リターン**: 異常系を先に処理し、正常系のネストを浅く保つ
- **エラーの握りつぶし禁止**: catch したら必ずログ出力 or 再throw
- **ユーザー向け vs 開発向け**: エラーメッセージは2層

## 5. ファイル構成
- 1ファイル = 1つの責務（モジュール単位）
- インポートは標準ライブラリ → サードパーティ → 自プロジェクトの順
- 未使用のインポート・変数は残さない
- マジックナンバー禁止（定数または設定値として定義）
</content>

### `~/.claude/knowledge/practices/security.md`:
<content>
# セキュリティプラクティス

> **プロジェクト CLAUDE.md の指定が優先**。ここは汎用デフォルト。

## 1. 入力検証（ゼロトラスト原則）
- ユーザー/API/外部サービスからのデータは**全て信頼しない**
- 検証項目: 型・範囲・形式・長さ・文字種

## 2. 認証・認可
- 管理系エンドポイントには必ず認証を設ける
- トークン/APIキーはリクエストヘッダーで受け渡し（URLパラメータ禁止）
- 最小権限の原則

## 3. 秘密情報管理
- APIキー・パスワード・トークンをコードに直書き**禁止**
- 環境変数 or 秘密管理ツールを使う
- `.env` ファイルは `.gitignore` に必ず含める

## 4. エラー情報の保護
- 本番環境でスタックトレースを外部に返さない
- 内部パス・DB構造をエラーレスポンスに含めない

## 5. 依存パッケージの安全性
- 定期的に `npm audit` / `pip audit` で脆弱性チェック

## 6. ログの安全性
- 個人情報・パスワード・トークンをログに出力しない
- ログには操作者・日時・操作内容・結果を記録

## 7. インシデント対応
- 発生時: 検知 → 影響範囲特定 → 封じ込め → 復旧 → 原因分析
- 再発防止: 根本原因に対する是正処置 + 水平展開
</content>

### `~/.claude/knowledge/practices/testing.md`:
<content>
# テストプラクティス

> **プロジェクト CLAUDE.md の指定が優先**。ここは汎用デフォルト。

## 1. テスト駆動開発（TDD）— 入出力が明確なコード
1. テストを先に書く → 失敗を確認（Red）
2. テストをパスさせる最小限の実装（Green）
3. リファクタリング（Refactor）
4. 繰り返す

## 2. 予測モデル検証 — TDDではなく仮説検証型
適用: 機械学習・統計予測等、正解が事前に分からないもの
1. 仮説を立てる → 2. ベースライン記録 → 3. 実験 → 4. 評価 → 5. 採用/棄却 → 6. 記録
- データパイプラインや特徴量計算はTDD、予測精度は仮説検証型

## 3. バグ修正手順
1. 再現テスト作成 → 2. 原因特定 → 3. 最小修正 → 4. 回帰確認 → 5. 水平展開

## 4. カバレッジ戦略
- 新規コード: TDD / 既存修正: テスト先追加 / リファクタ: 振る舞い固定テスト

## 5. テストの3層構造
| 層 | 対象 | タイミング |
|---|---|---|
| ユニットテスト | 関数・モジュール | コード変更の都度 |
| 統合/E2Eテスト | API・画面フロー | PR作成時・デプロイ前 |
| 本番動作確認 | 実環境 | デプロイ後 |
</content>

### `~/.claude/knowledge/practices/git-workflow.md`:
<content>
# Git ワークフロー

> **プロジェクト CLAUDE.md の指定が優先**。ここは汎用デフォルト。

## 1. ブランチ戦略（GitHub Flow）
- `main` は常にデプロイ可能。変更は feature ブランチ → PR → マージ

## 2. コミット規約
- 1機能/1バグ修正 = 1コミット。動詞で始める（Add/Fix/Update/Remove/Refactor）

## 3. 変更前の安全策
- 大きな変更の前に現状をコミット。高リスクはWorktreeで作業

## 4. PR
- タイトル70文字以内。本文に背景・変更内容・テスト計画

## 5. ロールバック
- デプロイ前にロールバック手順を確認。問題時は即座に前バージョンに戻す

## 6. リスクレベル別の運用
| リスク | 対応 |
|---|---|
| 🟢 低 | 通常フロー |
| 🟡 中 | 先にコミットしてから着手 |
| 🟠 高 | 影響範囲を洗い出してから着手 |
| 🔴 最高 | Worktreeで作業 |
</content>

### `~/.claude/knowledge/practices/dev-workflow.md`:
<content>
# 開発ワークフロー

> **プロジェクト CLAUDE.md の指定が優先**。ここは汎用デフォルト。

## 全体フロー: 受入 → 調査 → 計画(Plan) → 実装(Do) → 検証(Check) → 改善(Act)

## 1. 受入 — 目的と完了条件を確認。不明点は先に質問
## 2. 調査 — 既存コード検索、ライブラリ確認、影響範囲特定
## 3. 計画（Plan） — 受入基準明文化、リスク判定、実装方針
## 4. 実装（Do） — TDD or 仮説検証型。1機能=1コミット
## 5. 検証（Check） — ユニット→統合→本番の3層。diff確認・報告
## 6. 改善（Act） — 問題時は根本原因分析→是正→水平展開
</content>

### `~/.claude/commands/5s.md`:
<content>
# /5s — 作業開始前の5Sチェック

新しいタスクを始める前に、作業環境を整える。

## 実行内容
1. 片付け — 裏で動きっぱなしのプロセスがないか確認
2. 現状確認 — `git status` でブランチ・未コミット変更を確認
3. 健康チェック — CPU/メモリ/ディスク使用率を確認
4. ルール確認 — CLAUDE.md / memory が最新か確認
5. 手順開始 — TodoWrite でタスクリスト作成

全チェック結果を一覧で報告する。異常があれば対処を提案する。
</content>

### `~/.claude/commands/knowledge.md`:
<content>
# /knowledge — 知識ベース参照

課題を分析し、必要な知識ファイルを特定して参照する。
1. ユーザーの課題を分析
2. CLAUDE.md §知識ベース自動参照 の2層構造（大分類12 + 横断チェック7）で分類
3. 該当する知識ファイルを Read
4. 要約して課題への適用方法を提示

$ARGUMENTS に課題の説明がある場合はそれを分析対象にする。
</content>

### `~/.claude/commands/quality-review.md`:
<content>
# /quality-review — PDCA完了状況チェック

現在のタスクについて、PDCAの各段階の完了状況を確認する。
- Plan: 受入基準・リスク判定・影響範囲
- Do: テスト先行・品質ゲート・コミット粒度
- Check: テスト通過・diff確認・報告
- Act: 根本原因分析・水平展開

未完了の項目があれば指摘する。
</content>

### `~/.claude/commands/risk.md`:
<content>
# /risk — リスクレベル自動判定

git diff を分析し、変更のリスクレベルを判定する。
- 🟢 低: 新ファイル/テスト追加/20行以下
- 🟡 中: 既存コード修正/100行以下 → 先にコミット
- 🟠 高: 複数機能影響/300行以下 → 影響範囲洗い出し
- 🔴 最高: DB/cron変更/300行超 → Worktree

判定結果と推奨アクションを表示する。
</content>

### `~/.claude/hooks/process-gate.py`:
<content>
#!/usr/bin/env python3
"""
process-gate.py — コミット前リスク判定リマインダー
PreToolUse / Bash hook: git commit を検知してリスクレベルを推定表示する。
ブロックしない（常に exit 0）。リマインダーのみ。
"""
import sys
import io
import json
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")
    if "git commit" not in command:
        sys.exit(0)

    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--stat"],
            capture_output=True, text=True, timeout=5
        )
        stat = result.stdout.strip()
    except Exception:
        sys.exit(0)

    if not stat:
        sys.exit(0)

    lines = stat.split("\n")
    summary = lines[-1] if lines else ""

    files_changed = 0
    insertions = 0
    deletions = 0
    for part in summary.split(","):
        part = part.strip()
        if "file" in part:
            files_changed = int(part.split()[0])
        elif "insertion" in part:
            insertions = int(part.split()[0])
        elif "deletion" in part:
            deletions = int(part.split()[0])

    total_changes = insertions + deletions

    if total_changes <= 20 and files_changed <= 2:
        level = "🟢 低リスク"
    elif total_changes <= 100 and files_changed <= 5:
        level = "🟡 中リスク"
    elif total_changes <= 300 or files_changed <= 10:
        level = "🟠 高リスク"
    else:
        level = "🔴 最高リスク"

    print(
        f"\n⚙️ リスク判定リマインダー: {level}\n"
        f"   {files_changed}ファイル / +{insertions} -{deletions} 行\n"
        f"   → リスクに応じた品質ゲートを確認してください（quality/risks.md）\n",
        file=sys.stderr
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
</content>

Hookを有効化するには `~/.claude/settings.json` に以下を追加（既存設定とマージ）:

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

## 4. 知識ベース & Apple HIG スキル

8分野の専門知識リファレンスと Apple HIG デザインスキルを導入します。
GitHubからリポジトリをクローンし、ファイルをコピーしてください。

```bash
# 1. リポジトリをクローン（一時ディレクトリ）
git clone https://github.com/akaganenakajima-jpg/claude-code-quality-framework.git /tmp/ccqf

# 2. 知識ベースをコピー
for dir in ipa stats ds-advanced ds-expert math-strategist e-cert python3 ux-psychology; do
  mkdir -p ~/.claude/knowledge/$dir
  cp /tmp/ccqf/knowledge/$dir/*.md ~/.claude/knowledge/$dir/
done

# 3. Apple HIG スキルをコピー
mkdir -p ~/.claude/skills/apple-hig-designer/resources
cp /tmp/ccqf/skills/apple-hig-designer/SKILL.md ~/.claude/skills/apple-hig-designer/
cp /tmp/ccqf/skills/apple-hig-designer/REFERENCE.md ~/.claude/skills/apple-hig-designer/
cp /tmp/ccqf/skills/apple-hig-designer/LICENSE ~/.claude/skills/apple-hig-designer/
cp /tmp/ccqf/skills/apple-hig-designer/resources/* ~/.claude/skills/apple-hig-designer/resources/

# 4. 一時ディレクトリを削除
rm -rf /tmp/ccqf
```

Windows (Git Bash) の場合:
```bash
git clone https://github.com/akaganenakajima-jpg/claude-code-quality-framework.git "$TEMP/ccqf"
for dir in ipa stats ds-advanced ds-expert math-strategist e-cert python3 ux-psychology; do
  mkdir -p ~/.claude/knowledge/$dir
  cp "$TEMP/ccqf/knowledge/$dir/"*.md ~/.claude/knowledge/$dir/
done
mkdir -p ~/.claude/skills/apple-hig-designer/resources
cp "$TEMP/ccqf/skills/apple-hig-designer/SKILL.md" ~/.claude/skills/apple-hig-designer/
cp "$TEMP/ccqf/skills/apple-hig-designer/REFERENCE.md" ~/.claude/skills/apple-hig-designer/
cp "$TEMP/ccqf/skills/apple-hig-designer/LICENSE" ~/.claude/skills/apple-hig-designer/
cp "$TEMP/ccqf/skills/apple-hig-designer/resources/"* ~/.claude/skills/apple-hig-designer/resources/
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
├── python3/                ← Python3基礎（4分野・5ファイル）
│   ├── index.md            ← 分野横断マップ
│   ├── core-syntax.md      ← 構文・データ型・関数
│   ├── stdlib.md           ← 標準ライブラリ
│   ├── oop.md              ← オブジェクト指向
│   └── best-practices.md   ← PEP8・テスト・パフォーマンス
└── ux-psychology/          ← UX心理学（5クラスタ・6ファイル）
    ├── index.md            ← 全43法則早見表・シナリオ逆引き
    ├── information.md      ← 情報設計（認知負荷・段階的開示・視覚的階層）
    ├── choice.md           ← 選択設計（アンカー・おとり・フレーミング・損失回避）
    ├── motivation.md       ← 動機設計（目標勾配・変動報酬・ゲーミフィケーション）
    ├── impression.md       ← 印象設計（美的ユーザビリティ・社会的証明・ピークエンド）
    └── bias.md             ← 認知の罠（確証バイアス・共感ギャップ・ホーソン効果）
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
| UI画面設計・UX改善・コンバージョン最適化 | `ux-psychology/index.md`, `ux-psychology/choice.md` |
| オンボーディング・リテンション設計 | `ux-psychology/motivation.md`, `ux-psychology/impression.md` |
| UXリサーチ・A/Bテスト設計のバイアス回避 | `ux-psychology/bias.md` |

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

### 5-3. Everything Claude Code (ECC) のインストール

[everything-claude-code](https://github.com/affaan-m/everything-claude-code) は、コード品質（フォーマット・型・テスト実行）に特化した Claude Code 拡張パッケージです。
当フレームワーク（プロセス品質）と **競合ゼロ** で併用できます。

| 項目 | 当フレームワーク | ECC |
|---|---|---|
| 対象 | プロセス品質（判断/知識/規律/デザイン） | コード品質（フォーマット/型/テスト実行） |
| 格納先 | `~/.claude/CLAUDE.md` + `knowledge/` + `skills/` | `~/.claude/rules/` |

#### 前提条件
- Node.js >= 18（§5-1 でインストール済みであること）

#### 手順

**AskUserQuestion** でユーザーに確認:

**質問**: 「Everything Claude Code (ECC) をインストールしますか？コード品質ルール（フォーマット・型・テスト等）が追加されます。当フレームワークとの競合はありません。」

| 選択肢 | 動作 |
|--------|------|
| **🚀 インストールする** | 使用言語を選んで npx でインストール |
| **⏭️ スキップ** | §6（検証）に進む |

「インストールする」が選択された場合:

1. **AskUserQuestion** で主要言語を選択:

**質問**: 「メインで使用するプログラミング言語を選んでください（ECC のルールセットが言語に合わせて最適化されます）:」

| 選択肢 |
|--------|
| **TypeScript** |
| **Python** |
| **Golang** |
| **Swift** |
| **Kotlin** |
| **PHP** |
| **Perl** |
| **C++** |

2. 選択された言語で ECC をインストール:
```bash
npx ecc-install <選択された言語>
```

3. インストール結果を確認:
```bash
# ECC のルールファイルが配置されたか確認
ls ~/.claude/rules/ 2>/dev/null && echo "✅ ECC ルール配置完了" || echo "❌ ECC ルールが見つかりません"
# インストール状態の確認
cat ~/.claude/ecc/install-state.json 2>/dev/null && echo "✅ ECC インストール状態記録あり" || echo "⚠️ インストール状態ファイルなし"
```

⚠️ ECC は `npx` 経由で常に最新版をインストールします。アップデート時も同じコマンドを再実行するだけでOKです。

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
   - `~/.claude/knowledge/ux-psychology/` — 6ファイル（`index.md`, `information.md`, `choice.md`, `motivation.md`, `impression.md`, `bias.md`）
8. Apple HIG スキルフォルダに以下のファイルが存在する:
   - `~/.claude/skills/apple-hig-designer/SKILL.md`
   - `~/.claude/skills/apple-hig-designer/REFERENCE.md`
   - `~/.claude/skills/apple-hig-designer/LICENSE`
   - `~/.claude/skills/apple-hig-designer/resources/design-tokens.css`
   - `~/.claude/skills/apple-hig-designer/resources/components.jsx`
   - `~/.claude/skills/apple-hig-designer/resources/ui-patterns.md`
9. ECC をインストールした場合:
   - `~/.claude/rules/` フォルダが存在し、ルールファイルが配置されている
   - `~/.claude/ecc/install-state.json` が存在する

全て確認できたら、以下の形式でセットアップ結果をユーザーに表示してください:

**新規インストールの場合:**
```
## ✅ セットアップ完了

| コンポーネント | 状態 |
|--------------|------|
| CLAUDE.md（グローバルルール） | ✅ |
| 品質管理ファイル（8個） | ✅ |
| 開発プラクティス（6ファイル） | ✅ |
| スラッシュコマンド（4ファイル） | ✅ |
| Hook（process-gate.py） | ✅ |
| Apple HIG スキル（6ファイル） | ✅ |
| 知識ベース — IPA（11ファイル） | ✅ |
| 知識ベース — 統計検定1級（10ファイル） | ✅ |
| 知識ベース — DS発展（5ファイル） | ✅ |
| 知識ベース — DSエキスパート（5ファイル） | ✅ |
| 知識ベース — DS数学ストラテジスト上級（5ファイル） | ✅ |
| 知識ベース — E資格（5ファイル） | ✅ |
| 知識ベース — Python3基礎（5ファイル） | ✅ |
| 知識ベース — UX心理学（6ファイル） | ✅ |
| ECC（everything-claude-code） | ✅ インストール済 / ⏭️ スキップ |
| 前提プログラム（Node.js/Python/uvx） | ✅ 確認済 / ⏭️ スキップ |

💡 MCPサーバーの追加は recommended-tools.md を参照してください。
```

**アップデートの場合:**
```
## 🔄 アップデート完了

| コンポーネント | 状態 |
|--------------|------|
| CLAUDE.md（グローバルルール） | 🔄 更新 / ✅ 変更なし |
| 品質管理ファイル（8個） | 🔄 N個更新 / ✅ 変更なし |
| 開発プラクティス（6ファイル） | 🔄 N個更新 / ✅ 変更なし |
| スラッシュコマンド（4ファイル） | 🔄 N個更新 / ✅ 変更なし |
| Hook（process-gate.py） | 🔄 更新 / ✅ 変更なし |
| Apple HIG スキル | 🔄 更新 / ✅ 変更なし |
| 知識ベース（8分野） | 🔄 N分野更新 / ✅ 変更なし |
| ECC（everything-claude-code） | 🔄 更新 / ✅ 変更なし / ⏭️ スキップ |
| 前提プログラム（Node.js/Python/uvx） | ✅ 確認済 / ⏭️ スキップ |

📝 更新されたファイル:
- (変更されたファイルのパスを列挙)

💡 MCPサーバーの追加は recommended-tools.md を参照してください。
```
