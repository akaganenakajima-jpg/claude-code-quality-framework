# モデル選定と実行パラメータ — どのモデルを、どの effort で

> **最終検証日: 2026-09-25** ／ 出典: Anthropic 公式移行ガイド（platform.claude.com/docs/en/about-claude/models/migration-guide、`claude-api` スキル 2.1.280 に同梱）・Claude Code 公式 model-config / settings / changelog（v2.1.282 時点）
> モデルは数ヶ月で世代交代し、**振る舞いの指針まで反転する**（`agentic-operating.md` §9）。本ファイルはスナップショット。新モデルが出たら `agentic-operating.md` §10 の再監査手順で更新する。「要確認」印は公式で未確認の項目。

## 1. 現行モデル（Claude API の正式 ID）

| モデル | ID | 位置づけ | 入力 / 出力 $/MTok | thinking | effort |
|---|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | 最上位。最難関の推論・長時間の自律エージェント作業・複数ステップ調査・文書/表計算/スライド生成 | $10 / $50（cache read $0.25） | 常時 ON（無効化不可） | low〜max、既定 high |
| Claude Opus 5.5 | `claude-opus-5-5` | Opus 系の現行。長時間エージェントコーディング・ナレッジワーク。Opus 5 より安く、解決タスクあたりのトークンも少ない | $4 / $20（cache read $0.20） | 常時 ON（無効化不可） | low〜max、**既定 medium** |
| Claude Opus 5 | `claude-opus-5` | 前世代 Opus（継続提供） | $5 / $25 | 既定 ON（high 以下で無効化可） | 既定 high |
| Claude Sonnet 5 | `claude-sonnet-5` | 速度と知性のバランス。コーディング・エージェント作業で旧 Opus 級 | $2 / $10 | 既定 ON | 既定 high |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 最速・最安。定型・機械的作業 | $1 / $5 | 旧方式（`budget_tokens`） | effort 非対応 |

- コンテキスト / 最大出力: Haiku 4.5 は 200K / 64K、他は 1M / 128K。大きな入力を扱う作業は低リスクでも `haiku` は不適。
- 公式の位置づけ: 「まず Opus で始め、要求の厳しい推論・長期エージェント作業、または Opus を高 effort で回しても評価が届かないときに Fable」（公式文言は Opus 5 だが、Claude Code の `opus` は 5.5 に解決する）。Claude Code の既定モデルも v2.1.280 で Opus 5.5 になった（Pro / Team Standard は Sonnet から Opus へ変更）。なお `claude-api` スキルで API コードを書く際の既定は `claude-opus-5` で、5.5 はユーザーが名指しした場合のみ。
- Fable 5.1 と Opus 5.5 には安全分類器（cyber / bio / reasoning_extraction 等）があり、正当な要求でも稀に `refusal` で止まる。`reasoning_extraction` はフォールバックで再試行されない。Claude Code に分類器拒否時の組み込みフォールバックがあるかは未確認（公式は「消費者向けサーフェスには Opus 4.8 への組み込みフォールバックがある」とのみ記す。`fallbackModel` は HTTP 200 の分類器拒否では発動しない可能性が高い）。セキュリティ寄りの作業で不自然に止まったらこれを疑い、§4 の「黙って下位モデルで続行しない」に従う。Fable 5.1 については「コンパイルエラーはあるか」より「バグはあるか」と聞くと誤検知が減ると公式は助言している（Opus 5.5 については回避策の公式記載なし）。
- Fable 5.1 は 30 日データ保持が必須（Anthropic の明示的な許可がない限り ZDR 組織では使えない）。Opus 5.5 は Opus 5 と同じ扱い（ZDR 可）。Priority Tier は Opus 5 / Opus 5.5 / Sonnet 5 / Fable 5.1 で非対応。

## 2. effort — 主レバー（「どのモデルか」より先に「どの effort か」）

effort は思考の深さ・トークン消費・所要時間を一括で決める。コスト調整の順番は、キャッシュなど無料の改善 → effort → モデル切替（公式）。現行世代では effort の効きが大きく、モデルを下げる前に測る価値がある。Claude Code では `/effort <level>`（引数なしでスライダー、`/effort auto` で解除）、起動時 `--effort`、環境変数 `CLAUDE_CODE_EFFORT_LEVEL` で指定する。設定はモデルごとに保存される（`modelSettings`。上限は `maxEffortLevel`）。

| effort | 使いどころ |
|---|---|
| `low` | 短い定型作業・対話的な軽い往復。Fable 5.1 の low は旧世代の xhigh を上回ることが多い |
| `medium` | Opus 5.5 の既定。Opus 5 の high 相当の結果を約半分のトークンで出す（公式のエージェントコーディング評価） |
| `high` | 知性が要る作業の最低ライン。Fable 5.1・Sonnet 5 の既定、推奨起点 |
| `xhigh` | コーディング・エージェント作業で測定して効果があるとき（Opus 4.7 時代の Claude Code 既定。現在の既定ではない） |
| `max` | 正確さがコストより重要なとき。過剰思考になりうるので測って使う |

Claude Code の既定（公式 model-config）: **effort 対応モデルは全て `high`、ただし Opus 5.5 は `medium`、Opus 4.7 は `xhigh`**。注意点として、旧形式の `effortLevel`（settings のトップレベルキー）は Opus 5.5 以降の新モデルには適用されず、新モデルは `/effort` で選ぶまで各自の既定で動く。組織既定モデルに effort が設定されていればそれが優先。

運用原則:
- **上位モデル × 低 effort を、下位モデル × 高 effort より先に試す。** 比べるのは「解決タスクあたりのコスト」。安いリクエストが再試行を増やせば結局高い。
- Opus 5.5 は同じ effort 名でも Opus 5 より多く思考する。旧設定を持ち越さず、medium 起点で隣接レベルを試す。
- 長い成果物（ファイル全体・長文書）を xhigh / max で頼むと、思考で下書きしてから書き直して出力が倍になる。high で頼む。
- 思考は無効化できない（5.5 / 5.1）。「考えるな」系の指示は効かず、副作用（内部タグの漏れ）を増やすので書かない。減らしたいなら effort を下げる。
- 5.1 / 5.5 では、ツール呼び出しの合間の短い進捗メモが `thinking` ブロックとして返る。API を直接使う場合は `display: "updates"` を指定しないと長いターンが無言に見える（Claude Code での表示挙動は未確認）。

## 3. Claude Code でのモデル指定（リスク判定と対応させる）

`/model` またはセッション設定で切り替える。エイリアスの解決先（公式 model-config、v2.1.280 以降）: `opus` → Opus 5.5、`sonnet` → Sonnet 5、`haiku` → 最新 Haiku、`fable` → Fable 5.1、`best` → Fable が使えれば `fable` と同じ・使えなければ `opus` と同じ（エラーにはならない）、`default` → 上書き解除（Opus 5.5）。プラットフォームで解決先が変わる（Foundry の `opus` は 4.6、AWS の `sonnet` は 4.6、Bedrock / Vertex / Foundry の `sonnet` は 4.5、apps gateway の `fable` は Fable 5）。

| 作業の性質 | 目安リスク | エイリアス |
|---|---|---|
| 定型・機械的（検索・一覧化・整形・単純変換・ログ抽出・テスト実行） | 🟢 | `haiku` |
| 通常の実装・レビュー・調査・文書作成 | 🟢🟡 | `sonnet`（低 effort では過少思考の恐れ。難しい作業は xhigh）または `opus` を medium で |
| 複雑な推論・設計判断・原因不明のバグ・複数ファイル横断の変更 | 🟠 | `opus`（Opus 5.5。既定 effort が medium である点に注意） |
| 最難関・長時間（アーキテクチャ設計・DB 構造変更・横断監査・本番公開の影響分析） | 🔴 | `best`（Fable 5.1） |

- 上位モデルは「難しいから」ではなく「**判断を誤ると手戻りが大きいから**」使う。ただし §2 のとおり、公式比較では Opus 5.5 の medium が Opus 5 の high に約半分のトークンで並ぶ。Sonnet 5 との比較は公式に無いので、迷ったら「上位 × 低 effort」を自前で一度測る。
- 計画だけ上位で足りるなら `opusplan`（Plan モード中は `opus`、実行時は `sonnet` に自動切替）。長文脈は `sonnet[1m]` / `opus[1m]`（Sonnet 5 はネイティブ 1M のため効果なし）。
- **Fast mode**（`/fast`、settings `fastMode`）: 公式移行ガイドでは Opus 5 / 5.5 / 4.8 のみ・Claude API 経由のみ。同じモデルを最大 2.5 倍の出力速度で回す代わりに料金 2 倍（5.5 は $8 / $40 とされるが要確認）。対応モデル一覧と料金の最終値は要確認（§5）。
- サブエージェントのモデル解決順位: 呼び出し時指定 > agent 定義（`~/.claude/agents/*.md`）の `model:` > 環境変数 `CLAUDE_CODE_SUBAGENT_MODEL` > 親会話のモデル。ただし定義が `model: inherit` の場合は「定義の指定」として扱われ、環境変数より親のモデルが勝つ。サブエージェントには原則 `sonnet` / `haiku` と低〜中 effort を割り当て、統合判断だけ親が担う（§2「上位 × 低 effort」の例外。委譲先は範囲が限定されるため）。

## 4. 上位モデルが使えないとき — 原因で対処を分ける

1. **過負荷・利用不可・非再試行のサーバエラー** → `settings.json` の `fallbackModel`（または `--fallback-model`、フラグが settings より優先）が自動で一段下げる。チェーンは重複除去後 3 つまで、そのターン限り（次のメッセージは再び上位から試行）。複数の settings ファイルにある場合はマージせず最上位ファイルの値を採用。プロンプトでの対処は不要。
2. **使用量上限・レート制限・課金・認証・リクエストサイズ・トランスポートエラー・組織ポリシー拒否** → `fallbackModel` は発動しない（公式に明示除外）。このときだけ:
   - 上限に当たった事実をユーザーに報告する（黙って下位モデルで続行しない）
   - 一段下（`best` → `opus` → `sonnet` → `haiku`）を明示指定して再実行する
   - 下げた事実と精度が落ちうる箇所を成果物に明記する（`quality/nonconformity.md`）
   - 🔴 作業は下位モデルで代替しない。回復を待つか、ユーザーに判断を仰ぐ

## 5. 要確認（公式で未確認・リリース直後の記述）
- Fast mode の対応モデル一覧と Opus 5.5 の料金（Claude Code の `fast-mode` ページで確認）
- Opus 5.5 のフォールバック先モデルの最終値
- `haiku` エイリアスが解決する具体バージョン
- Claude Code に分類器拒否時の組み込みフォールバックがあるか、あるならその着地先
