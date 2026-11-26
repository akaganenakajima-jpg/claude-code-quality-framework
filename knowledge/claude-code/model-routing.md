# モデル選定と実行パラメータ — どのモデルを、どの effort で

> **最終検証日: 2026-11-27** ／ Claude Code v2.1.332（Desktop 2.1.331 で確認）／ 出典: Claude Code 公式 model-config・sub-agents・workflows・fast-mode・costs・settings・env-vars、CHANGELOG（v2.1.332 まで）、`claude-api` スキル（2.1.331 同梱）の Current Models と移行ガイド、claude.dev ブログ「Which Claude model should you build with?」（2026-11-09）
> モデルは数ヶ月で世代交代し、振る舞いの指針まで反転する（`agentic-operating.md` §9）。本ファイルはスナップショット。新モデルが出たら `agentic-operating.md` §10 の再監査手順で更新する。CLAUDE.md「サブエージェントの使い分け」の表は §3 の要約で、食い違ったらこのファイルを優先する。確かめられていない項目は §5 にまとめる。

## 0. 最低版 — 古い CLI では書いてあるとおりに動かない

このファイルは **v2.1.321 以上**を前提にする。

| 版 | 変わったこと | 出典 |
|---|---|---|
| v2.1.283 | `/doctor prompt-audit` が入った（再監査に使う） | CHANGELOG 2.1.283 |
| v2.1.292 | Agent ツールに `effort` 引数が入った | CHANGELOG 2.1.292 |
| v2.1.293 | `haiku` が Haiku 5.5 を指す（`sonnet` は v2.1.284、`opus` は v2.1.280 で 5.5 系に） | model-config『Version history』 |
| v2.1.317 | 親と別のモデルで動くサブエージェントは、親の effort ではなく、そのモデルの保存値か既定値で動く | CHANGELOG 2.1.317 |
| v2.1.321 | Fable 5.2 が入り、`fable` が Fable 5.2 を指す。`best` は `opus` と同じに解決するようになった | model-config『Version history』 |

- Desktop アプリが動かす Claude Code と、ターミナルの PATH 上の `claude` は、版が別になることがある。
- PATH 上の CLI が v2.1.321 より前だと、同じ PC でも旧挙動になる（`best` が Fable を指す、Fable 5.2 を選べない）。v2.1.317 より前だと、別モデルのサブエージェントが親の effort を引き継ぐ。
- `claude --version` で確かめ、古ければ `claude update` で上げる（実行は利用者の了承を得てから）。

## 1. 現行モデル（Anthropic API）

| モデル | ID | 位置づけ | 入力 / 出力 $/MTok | コンテキスト | API の既定 effort | Claude Code の既定 effort |
|---|---|---|---|---|---|---|
| Fable 5.2 | `claude-fable-5-2` | 最上位。大規模なリファクタ・移行、アーキテクチャ計画、多数のサブエージェントの指揮、長時間の無人実行。Opus 5.5 を high にしても届かない作業 | $8 / $40 | 1M | high | medium |
| Opus 5.5 | `claude-opus-5-5` | 大半の作業の起点で、Claude Code の既定モデル。日常のエンジニアリング・デバッグ・複数 PR にまたがる機能 | $4 / $20 | 1M | medium | medium |
| Sonnet 5.5 | `claude-sonnet-5-5` | 範囲が明確な日常作業（バグ修正・仕様どおりの機能）、繰り返す調査・レビュー・下書き。Opus 5.5 の半額で速い | $2 / $10 | 1M | high | medium |
| Haiku 5.5 | `claude-haiku-5-5` | 大量の分類・振り分け・抽出。誤りを見つけやすい補助作業（ファイル探し・ログ読み） | $0.10 / $0.50（プロンプト 100K 以下）、$0.50 / $2.50（100K 超） | 1M | medium | medium |

- 出典: which-claude-model ブログ『TL;DR』『Pick a model by task』『The four models side by side』、`claude-api` スキル『Current Models』、model-config『Adjust effort level』。
- キャッシュ読み取りは Fable 5.2・Opus 5.5 が $0.20、Sonnet 5.5 が $0.10、Haiku 5.5 が $0.01（100K 超は $0.05）。最大出力は4モデルとも 128K。
- **既定 effort は API と Claude Code で違う。** Claude Code では4モデルとも medium。`CLAUDE_CODE_EFFORT_LEVEL=auto`（または `unset`）で起動すると effort を送らず、API の既定（Fable 5.2・Sonnet 5.5 は high）が効く（model-config『Send no effort level』）。
- Haiku 5.5 はプロンプトが 100K を超えると単価が5倍になる（それでも Sonnet 5.5 の4分の1）。長いプロンプトを毎回送る作業は、Sonnet 5.5 と「完了1件あたりの費用」で比べる。
- 4モデルとも、Claude Code では思考（thinking）を切れない。減らしたいときは effort を下げる（model-config『Where you can't turn thinking off』）。
- 他のプロバイダ（Bedrock・Agent Platform・Foundry など）では、`sonnet`・`haiku` などが旧版を指すことがある。解決先は版でも変わる（v2.1.332 で Agent Platform・Foundry の `sonnet` が Sonnet 5.5 に）。使う前に model-config『Model aliases』で確かめる。

### プランと席で変わる課金

| 対象 | 内容 | 出典 |
|---|---|---|
| Fable | Pro、Team の Standard 席、席課金型 Enterprise の Standard 席では、最初のリクエストから usage credits（従量課金）でしか動かない。`/model` の Fable の行に「Requires usage credits」と出る | サポート記事「Claude Fable models on your plan」、model-config『Fable and usage credits』 |
| Fable の同意 | 対話セッションでは、usage credits に課金する前に同意を求める。`-p` と、確認を出さない Agent SDK アプリでは、同意なしに課金する。Remote Control・background セッション・agent teams のチームメイトでは `dialogExpiry`（既定5分）まで待ち、答えが無ければリクエストを送らずにターンを終える | model-config『Fable and usage credits』 |
| fast mode | Fable 5.2・Opus 5.5 が正式対応（Opus 5 はリサーチプレビュー）。Sonnet・Haiku は使えない。単価は標準の2倍（Fable 5.2 は $16 / $80、Opus 5.5 は $8 / $40）。サブスクリプションでは、プラン枠が残っていても常に usage credits から払う。会話の途中で初めてオンにすると、それまでの文脈をキャッシュなしの fast 単価で読み直す | fast-mode『Understand the cost tradeoff』『Requirements』 |
| サブエージェント・Workflow | メイン会話と同じプランの使用量に数える。モデルを指定しなければセッションのモデルで動くので、`/model` を上位にすると委譲先も上位になる | costs『Choose the right model』『Delegate verbose operations to subagents』、workflows『Cost』 |

## 2. effort — モデルを替える前に動かすつまみ

effort は、思考の深さ・ツール呼び出しの量・自己検証の量をまとめて決める。モデルを替える前に、まず effort を1段動かす。ただし effort は、モデルに無い知識や技能を与えない（which-claude-model『TL;DR』）。

| effort | 使いどころ（model-config『Choose an effort level』） |
|---|---|
| `low` | 結果を毎回見て次を指示する短いやりとり（ブレスト・最初の下書き・リネームのような小さな変更） |
| `medium` | 4モデルの Claude Code での既定。範囲が明確な日常のエンジニアリング（新機能の実装など） |
| `high` | 検証が重要な作業、境界ケースが多い作業（既存コードのバグ修正など） |
| `xhigh` | より深い推論。トークンも増える |
| `max` | 人がいない間に解かせたい難問（脆弱性の探索など）。効果が逓減し、考えすぎになりやすい。広く使う前に試す |

- 公式の試験では、高い effort ほど境界ケースを多く試し、答える前の検証が増え、自分で決める選択も増えた。低い effort では、たたき台が早く返る（同節）。
- effort を上げると、境界ケースの見落としは減る。取り組み方の誤りは直らない（ブログ「Spending your effort」）。
- 段の幅はモデルごとに違い、同じ名前でも中身は同じではない。モデルを替えたら、前の設定を持ち越さずに測り直す。
- Sonnet 5.5 は low で、Haiku 5.5 は low と medium で、コードの変更を確かめずに「完了」と報告することがある（移行ガイド『Verification on coding tasks』）。結果を自動で確かめる手段（テストなど）が無いかぎり、コードを変える委譲に low を使わない（確かめられる場合は下の「全件を low で回し、失敗した分だけ high」）。

### effort を上げるか、モデルを上げるか

| 結果の悪さ | 打ち手 | 出典 |
|---|---|---|
| ファイルを読み飛ばした・テストを回さなかった・境界ケースを落とした | effort を1段上げる | ブログ「Choosing a Claude model and effort level in Claude Code」（境界ケースは同ブログ『Spending your effort』） |
| 文脈はそろい、きちんと取り組んだのに誤った | モデルを1段上げる（opus から fable へ上げるのは利用者が Fable を使うことに同意したと確かめられるときだけ） | 同上 |
| 量が多く、判断が要らない | モデルを下げる | which-claude-model『Pick a model by task』 |
| high より上が欲しくなった | 先に1つ上のモデルを低い effort で試す（opus から fable へ上げるのは利用者が Fable を使うことに同意したと確かめられるときだけ。プランによっては従量課金）。high を超えると、1段上のモデル並みの費用になりうる（例: Fable 5.2 の high は Opus 5.5 の max とほぼ同点で、費用は約半分） | which-claude-model『TL;DR』『Capability and cost per finished task』 |

- 足りないときの順番（which-claude-model『Latency against accuracy』）: ①自分の仕事を確かめる手段（テスト・ビルド・呼び出し確認のスクリプト）があるか確かめる → ②effort を1段上げる → ③1つ上のモデルへ（opus から fable へは利用者が Fable を使うことに同意したと確かめられるときだけ）。下のモデルで使ったより低い effort から始める。
- **結果を自動で確かめられるなら**、全件を low で回し、失敗した分だけ high で再実行する。同ブログの例では、Opus 5.5 でこのやり方が合格率約97%・1件約$0.17 となり、全件 high（95.3%・約$0.29）を上回った。

### 「指定しない」の定義

「指定しない」とは、呼び出し時の引数にも、エージェント定義にも effort を書かないこと。そのときサブエージェントは、次のうち最初に当たるもので動く（sub-agents『When a subagent has no effort field or parameter』。v2.1.317 以降）。

1. `CLAUDE_CODE_EFFORT_LEVEL`（設定していれば）
2. 起動元のサブエージェントの effort、またはそのターンだけの effort（スキルの `effort` など）
3. `CLAUDE_CODE_SUBAGENT_EFFORT`
4. どれも無ければ、親と同じモデルならセッションの effort（`/effort`・`--effort`）。別のモデルなら、そのモデルの保存値か既定値（4モデルとも medium）

- `CLAUDE_CODE_EFFORT_LEVEL` は、`--effort`・`/effort`・設定・frontmatter・呼び出し時の引数のすべてより優先する（env-vars、sub-agents『Choose an effort level』）。これを固定すると、§3 の表の effort 列は効かない。
- v2.1.317 より前は、別モデルのサブエージェントも親のセッションの effort を引き継いでいた。

## 3. QCD とモデル指定

### QCD の定義

| 記号 | 意味 | 見方 |
|---|---|---|
| Q | 誤ったときの手戻りの大きさ | 誤りに気づくまでの距離と、直す範囲。判断をメイン会話が持つ読むだけの作業は小さい。設計・セキュリティ・DB は大きい |
| C | 費用。2段階で見る | ①プラン枠の消費が増える（上限に早く当たる）。②従量課金になる（usage credits・API 課金）。②に当たるのは、プランによっては Fable、サブスクリプションでの fast mode、API キーでの利用。②は利用者が決める |
| D | 待ち時間 | 結果を人が待つか。上位モデル・高い effort ほど遅い |

### 作業ごとのモデルと effort（CLAUDE.md の表の完全版）

| 作業（リスク） | 重み | model | effort | 理由 | 出典 |
|---|---|---|---|---|---|
| 読むだけの検索・一覧化・ログ抽出・要約（🟢） | C・D | haiku | 指定しない | 誤りが安く見つかり、判断はメイン会話に残る。公式は、検索・ログ読み・要約のサブエージェントを Haiku 5.5 か Sonnet 5.5 の既定 effort で回すよう勧める。入力が 100K を超えるなら sonnet と比べる | which-claude-model『Pick a model by task』『Put subagents on smaller models』 |
| 範囲の明確な実装・文書作成・調査のまとめ（🟢🟡） | D・C | sonnet | 指定しない | 範囲が明確な日常作業は Sonnet 5.5 に下げる。medium は範囲が明確な日常のエンジニアリング向け。仕様が明確でも、移行や性能改善のように難しい作業は opus にする | which-claude-model『TL;DR』『Pick a model by task』、model-config『Choose an effort level』 |
| レビュー・テスト結果の検証（🟡） | Q | sonnet | high | 結果は、読む量と検証の量で決まる。別モデルのサブエージェントは指定しないと medium で動くので、high を明示する | model-config『Choose an effort level』、sub-agents『When a subagent has no effort field or parameter』 |
| 設計判断・原因不明のバグ・セキュリティ/権限/DB のレビュー（🟠） | Q | opus | high | 見落としの手戻りが大きい。知識の上限はモデルで、丁寧さは effort で上げる | which-claude-model『TL;DR』、model-config『Choose an effort level』 |
| 最難関・長時間（🔴。合意を得るときに、Fable を使うこと（プランによっては従量課金）も伝える） | Q 最優先 | fable | 指定しない（結果の品質が足りなければ high で再実行） | 公式は、大規模なリファクタ・移行、アーキテクチャ計画、多数のサブエージェントの指揮に、Fable 5.2 を medium から（次に high）勧める。プランによっては従量課金になるので、合意のときに伝える | which-claude-model『Pick a model by task』、model-config『Fable and usage credits』 |

### 表の適用範囲と前提

- 行は、親のタスクではなく、委譲する作業そのものの難易度とリスクで選ぶ。
- model 列が効くのは、定義に `model` が無いエージェント（汎用のサブエージェントなど）だけ。定義に `model` があるエージェントは、定義が正（下の解決順②）。
- inherit（model を渡さない）に頼らない。親が fable だと、定義の無い委譲先は全部 Fable で動く。
- 親が Fable のとき Opus に下がるのは、組み込みの Explore だけ（sub-agents『Built-in subagents』。サブスクリプション・Console・`ANTHROPIC_BASE_URL` のゲートウェイのとき。Bedrock などでは Fable のまま）。
- 表に無い作業:
  - 結果を毎回人が見る短い往復は、委譲せず、メイン会話で effort を下げる。
  - 依存が一本の鎖になる作業と、1つのコンテキストに収まる作業は分けない。計画と統合の費用が上回る（which-claude-model『Delegate bulk work to cheaper workers』）。
  - 1つのコンテキストに収まらない大量の作業は、上位モデルが分けて、安いワーカーに並列で渡すと得になりうる（同節。Opus 5.5 のリードと Sonnet 5.5 のワーカーで、費用が約3分の1減り、結果はほぼ同じだった）。

### エイリアスの解決先（Anthropic API）

| エイリアス | 解決先・扱い | 使いどころ |
|---|---|---|
| `haiku` | Haiku 5.5 | 読むだけの補助 |
| `sonnet` | Sonnet 5.5 | 範囲が明確な作業、レビュー・検証 |
| `opus` | Opus 5.5 | 設計・原因不明のバグ・🟠のレビュー |
| `fable` | Fable 5.2（Claude apps gateway では Fable 5） | 🔴だけ。合意を得てから |
| `best` | 使わない。v2.1.321 から `opus` と同じに解決し、それより前は Fable を指した。版で意味が変わり、frontmatter の正式な値にも無い | — |
| `default` | 上書きを外し、アカウントの既定に戻す（エイリアスではない） | — |
| `opusplan` | Plan モード中は opus、実行は sonnet。コード編集が sonnet に乗るので、既定にする前に自分の作業で測る | — |

出典: model-config『Model aliases』『Version history』、sub-agents『Frontmatter reference』、which-claude-model『Put subagents on smaller models』。

### サブエージェントのモデルと effort の解決順

| 項目 | 先に当たったものが勝つ | 出典 |
|---|---|---|
| model | ①呼び出し時の `model` → ②定義の `model`（`inherit` を含む）→ ③`CLAUDE_CODE_SUBAGENT_MODEL` → ④親のモデル（入れ子なら、起動元のサブエージェントのモデル） | sub-agents『Choose a model』 |
| effort | `CLAUDE_CODE_EFFORT_LEVEL` がすべてに優先する。その下で ①呼び出し時の `effort` → ②定義の `effort` → ③起動元のサブエージェント・スキルの effort → ④`CLAUDE_CODE_SUBAGENT_EFFORT` → ⑤親と同じモデルならセッションの effort、別モデルならそのモデルの保存値・既定値 | sub-agents『Choose an effort level』『When a subagent has no effort field or parameter』 |

- `CLAUDE_CODE_SUBAGENT_MODEL` にモデルを入れ、`CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` を併せて設定すると（v2.1.257 以降）、定義の model も呼び出し時の model も無視され、fork などを除く全サブエージェントがそのモデルで動く（sub-agents『Run every subagent on one model』）。
- fork（会話の分岐）には、呼び出し時の model・effort が効かない（Agent ツールの説明文）。
- 実際に動いたモデルと effort は、`/tasks` で確かめられる（sub-agents『Check a subagent's model』）。

### 効かせ方（CLAUDE.md の規則の根拠）

- 汎用のサブエージェントには、表の model と effort を Agent ツールの引数で渡す。
- エージェント定義に書かれた項目は、呼び出し時に渡さない（定義が正）。定義に無い項目は、表に従って渡す。例: model だけ定義されたレビュー系には `effort: high` を渡す。
- 例外: 委譲する作業そのものが🔴に当たるときは、定義に model があっても、呼び出し時に `model: fable` を渡す（呼び出し時の指定は定義より優先する）。ただし Fable への同意が確かめられるときに限る（下の「セッション単位の変更と無人実行」）。
- Agent ツールの `model` は、エイリアス（`sonnet`・`opus`・`haiku`・`fable`）だけを受け付ける。完全な ID や `inherit` は渡せない。
- Agent ツールの `effort`（v2.1.292 以降）は、**利用者か、CLAUDE.md・スキルなどの指示が特定の effort を明示したときだけ**使う。Claude 自身の判断では使わない。
  - 根拠は、ランタイムの Agent ツールの説明文（v2.1.331 で 2026-11-27 に確認）。公式ドキュメント（sub-agents『Choose an effort level』）は「利用者が特定の effort を頼んだとき」とだけ書き、CLAUDE.md の指示が根拠になることは明記していない。
  - そのため CLAUDE.md の表は命令形で書く。渡ったかは、トランスクリプトの Agent 呼び出しの入力か `/tasks` で確かめる。
  - 2026-11-27 に v2.1.331 で確かめた結果: CLAUDE.md にこの表だけを置いた非対話の実行で、汎用サブエージェントには `model: haiku`・`model: fable` が、model だけ定義されたエージェントには model なしで `effort: high` が渡り、それぞれ指定どおりのモデルで動いた（サブエージェントの meta.json にも effort が残る）。
  - 確実に効かせたいものは、エージェント定義の frontmatter に `effort` を書く（ランタイムが直接当てる公式の経路）。

### Workflow の agent()

- model は原則省略する。省略するとセッションのモデルで動く。スクリプトが名指ししたモデルは、呼び出し時の指定と同じ扱いになる（workflows『Cost』）。
- メイン会話が fable のときは、🔴以外の段に opus 以下を明示する（省略すると全段が Fable で動く）。
- effort は、機械的な段（大量の分類・抽出・整形）だけ low にする。根拠は、Workflow を書くためのスキル（workflow-authoring、v2.1.331 同梱）の本文で、公開ドキュメントには書かれていない。
- 最上位のモデルが要らない段は、小さいモデルを指定してよい（workflows『Cost』）。読むだけで大量・機械的だと確信できる段は haiku を明示する。
- 25 体を超えるか、見込みが 150 万トークンを超えると「Large workflow」の警告が出る。警告だけで、止まりはしない。大きな作業は、先に小さく試す（workflows『Cost』）。

### エージェント定義（frontmatter）の推奨値

| 役割 | model | effort | 補足 |
|---|---|---|---|
| 探索・要約（読むだけ） | haiku | 書かない | 名前を `Explore` にすると、組み込みの Explore を置き換えられる（組み込みは親のモデルで動く。親が Fable のときの扱いは「表の適用範囲と前提」） |
| レビュー・検証 | sonnet | high | |
| セキュリティ・DB のレビュー | opus | high | |
| 設計 | opus | 書かない | 🔴のときだけ、呼び出し時に `model: fable` を渡す。effort を書かないのは、🟠では呼び出し時に `effort: high` を渡し、🔴では `model: fable` だけを渡して表どおり effort なしで動かすため |

- frontmatter に `fable` を書かない。書くと、呼ばれるたびに利用者の了承を挟まず Fable が選ばれる（プランによっては従量課金。サブエージェントでの課金同意の扱いは §5 のとおり未確認）。
- ECC などの配布物を入れ直すと、書き換えた frontmatter が上書きされるおそれがある（§5）。入れ直したら、この表と突き合わせる。
- `omitClaudeMd: true`（v2.1.271 以降）は、読むだけの検索・要約用エージェントに限って任意で使う。外すと、CLAUDE.md の安全規則（承認の境界・秘密情報の扱い・言語の指定・この表）も委譲先に届かない（sub-agents『Frontmatter reference』）。組み込みの Explore・Plan は、もともと CLAUDE.md を読まない。

### セッション単位の変更と無人実行

- `/model`・`/effort`・Desktop のセッション管理ツール（`set_session_model`・`set_session_effort`・`set_session_fast_mode`）・fast mode（`/fast`）は、セッション全体と、モデルを指定しない委譲先に効く。**利用者が頼んだときだけ**変える。bypass などの許可モードでは確認画面が出ないので、規則として守る。
- fable を指定するのは、利用者が Fable を使うことに同意したと会話の中で確かめられるときだけ（🔴の作業への合意だけでは足りない）。確かめられないとき（依頼文に Fable の明示が無い無人実行〈`-p`・Routines・Workflow〉を含む）は🔴の行も opus・high で動かし、そのことを結果に書く。モデルは自分が無人で動いているかを確実には見分けられないので、条件は「無人かどうか」ではなく「Fable への同意を確かめられるか」で置く（2026-11-27 の受け入れテストで、無人かどうかを条件にした書き方は効いたり効かなかったりした）。これはモデルの選び方の話で、🔴の合意が要る操作そのもの（DB 構造の変更・本番公開など）は、無人では実行せず未実行で返す。`-p` では、Fable が usage credits 払いになるプラン・席の場合、同意を求めずに課金される（model-config『Fable and usage credits』）。

## 4. 上位モデルが使えないとき — 原因で対処を分ける

1. **過負荷・利用不可・再試行しないサーバエラー** → フォールバックチェーンが自動で切り替える（model-config『Fallback model chains』）。
   - settings の `fallbackModel`（配列）か、`--fallback-model`（カンマ区切り。設定より優先）で指定する。各項目はモデル名かエイリアスで、`"default"` は既定モデルに展開される。
   - 試すのは、重複を除いて3つまで。切り替えはそのターン限りで、次のメッセージは元のモデルから試す。
   - 複数の settings ファイルにあるときは結合せず、優先度の最も高いファイルの値をそのまま使う（settings『Lists merge instead of overriding』）。
   - 起動時や `/status` には出ない。切り替わったときの通知で初めて分かる。
   - `availableModels` で許されない項目は外れる。圧縮（compaction）では、コンテキストが小さいモデルに落とさない。auto モードでは、非対応のモデルを飛ばす。
   - サブエージェントにも効く。セッションのモデルは変わらない。
2. **認証・課金・レート制限（使用量上限）・リクエストサイズ・通信エラー・組織のポリシーによる拒否** → チェーンは動かない（公式に明記）。このときだけ:
   - 上限に当たった事実を利用者に報告する（黙って下位モデルで続けない）
   - 一段下（fable → opus → sonnet → haiku）を明示して再実行する
   - 下げた事実と、精度が落ちうる箇所を成果物に書く（`quality/nonconformity.md`）
   - 🔴の作業は下位モデルで代替しない。回復を待つか、利用者に判断を仰ぐ（Fable への同意が確かめられないときに opus で動かすのは §3 の規則による選択で、この代替には当たらない）
3. **安全分類器による拒否** → 内容による自動フォールバック（model-config『Automatic model fallback』）。
   - Fable・Opus 5.5・Sonnet 5.5・Opus 5 には分類器があり、主にサイバーセキュリティと生物学の内容で反応する。
   - Fable と Opus 5.5 は、生物学なら Opus 5、サイバーなら旧世代の Opus で再実行する。Sonnet 5.5 は、サイバーなら Sonnet 5 で再実行し、生物学は拒否で終わる。
   - メイン会話は、切り替わったあともフォールバック先のモデルで続く（戻すには `/model`）。effort は、拒否されたリクエストの値を引き継ぐ。
   - `/config` の「Switch models when a message is flagged」を「Ask each time」（`switchModelsOnFlag: false`）にすると、メイン会話では毎回確認する。Agent ツールで起動したサブエージェントは確認しない。自動切替なら再実行し、「Ask each time」なら失敗して Claude に戻る。
   - 最初のリクエストにも CLAUDE.md や git status が載る。セキュリティや生物学の資料があるリポジトリでは、最初から反応することがある。`claude --safe-mode` で切り分ける。
   - 不自然に止まったら、これを疑う。下位モデルで黙って続けない（2. と同じ扱い）。

## 5. 要確認（公式で確かめられていない項目）

- サブエージェントで、Fable の usage credits の同意がどう扱われるか（公式は、Remote Control・background セッション・チームメイトの扱いだけを書いている）
- coordinator mode: 公式ドキュメントが無い。そのとき、サブエージェントのモデル指定が効くかは未検証
- frontmatter に `model: best` と書いたときの挙動（公式の値に無いので使わない）
- ECC などを入れ直したとき、書き換えたエージェント定義の model が上書きされるか
- usage credits が有効なとき、Workflow の「上限で一時停止」が効くか
