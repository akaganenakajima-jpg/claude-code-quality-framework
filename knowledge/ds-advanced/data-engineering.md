# データエンジニアリング — DS発展リファレンス

> 統計検定データサイエンス発展 満点レベル対応
> 各セクション末尾に「実務活用」を収録

---

## 1. データ収集・前処理

### 1.1 データソースの種類

| 分類 | 形式 | 例 | 処理ツール |
|---|---|---|---|
| 構造化データ | 行×列の表形式 | RDB、CSV、Excel | pandas, SQL |
| 半構造化データ | スキーマ付き階層 | JSON, XML, Parquet | json, lxml, pyarrow |
| 非構造化データ | スキーマなし | テキスト、画像、音声、動画 | NLP/CV専用ライブラリ |

**データ収集手法**:
- **API連携**: REST/GraphQL。レートリミット・ページネーション対応が必須
- **Webスクレイピング**: robots.txt尊重、利用規約確認、過度なアクセス回避
- **ログ収集**: Fluentd/Logstash。構造化ログ（JSON）推奨
- **IoTセンサー**: MQTT/HTTP。エッジでの前処理（フィルタリング・集約）

### 1.2 ETL/ELTパイプライン設計

**ETL（Extract → Transform → Load）**:
- 変換後にDWHへロード。データ品質を保証しやすい
- バッチ処理向き。スキーマオンライト（書き込み時にスキーマ適用）

**ELT（Extract → Load → Transform）**:
- まず生データをデータレイクへロード、必要時に変換
- 大規模データ向き。スキーマオンリード（読み取り時にスキーマ適用）
- クラウドDWH（BigQuery, Snowflake, Redshift）のコンピュートパワーを活用

**パイプライン設計原則**:
- **冪等性（Idempotency）**: 同じ入力で再実行しても同じ結果
- **再現性**: パイプラインのバージョン管理（dbt, Airflow DAG）
- **監視**: データ行数・NULL率・型異常の自動チェック（Great Expectations等）
- **リトライ戦略**: 指数バックオフ + Dead Letter Queue

### 1.3 データクレンジング

#### 欠損値の分類と処理

| 分類 | 定義 | 検定 | 処理方法 |
|---|---|---|---|
| MCAR (Missing Completely At Random) | 欠損が完全にランダム | Little's MCAR検定 | リストワイズ削除が許容 |
| MAR (Missing At Random) | 欠損が他の観測変数に依存 | ロジスティック回帰で欠損フラグ予測 | 多重代入法（MICE） |
| MNAR (Missing Not At Random) | 欠損が欠損値自身に依存 | 感度分析 | ドメイン知識による補完、パターン混合モデル |

**欠損値処理手法**:
- **削除**: リストワイズ（行削除）、ペアワイズ（分析ごとに利用可能なペアを使用）
- **単一代入**: 平均値/中央値/最頻値、前方補完(ffill)/後方補完(bfill)
- **多重代入法（MICE）**: 欠損を条件付き分布から複数回サンプリング → 統合（Rubinの規則）
- **モデルベース**: k-NN代入、ランダムフォレスト代入

```
# MICEの概念フロー
for m in 1..M:  # M回の代入
  for 各欠損変数 j:
    他の変数を予測子として回帰 → 欠損値をサンプリング
  完全データセット_m を生成
最終推定 = M個の結果の統合（Rubinの規則）
```

#### 外れ値検出

| 手法 | 原理 | 適用場面 |
|---|---|---|
| IQR法 | Q1-1.5*IQR〜Q3+1.5*IQR の範囲外 | 単変量、分布の仮定なし |
| Zスコア | \|z\| > 3 を外れ値とする | 正規分布を仮定する場合 |
| Modified Z-score | MAD（中央絶対偏差）基準 | ロバスト、歪んだ分布にも適用可 |
| Isolation Forest | ランダム分割で早く孤立する点 | 多変量、非線形 |
| LOF | 局所密度比に基づく | 密度が不均一なデータ |
| Mahalanobis距離 | 共分散を考慮した距離 | 多変量正規分布 |

**外れ値の処理方針**:
1. まずドメイン知識で「異常値」か「極端な正常値」かを判断
2. 異常値 → 除外 or 修正（Winsorization: パーセンタイルでキャップ）
3. 極端な正常値 → ロバストな手法を選択（中央値、MAE、Huber回帰等）

#### 重複除去
- **完全一致**: `df.drop_duplicates()`
- **あいまい一致**: 文字列類似度（Levenshtein距離、Jaro-Winkler）でレコードリンケージ
- **時系列重複**: タイムスタンプ±許容範囲での重複検出

### 1.4 特徴量エンジニアリング

#### スケーリング

| 手法 | 式 | 用途 |
|---|---|---|
| 標準化 (Z-score) | (x - μ) / σ | 平均0・分散1。勾配法ベースのモデル |
| Min-Max正規化 | (x - min) / (max - min) | [0,1]に変換。距離ベースのモデル |
| ロバストスケーリング | (x - Q2) / (Q3 - Q1) | 外れ値に強い |
| 対数変換 | log(x + 1) | 右裾が重い分布（売上、アクセス数） |
| Box-Cox変換 | (x^λ - 1) / λ | 正規分布に近づける。λを自動推定 |
| Yeo-Johnson変換 | Box-Coxの拡張（負値対応） | 負値を含むデータの正規化 |

#### カテゴリカル変数エンコーディング

| 手法 | 説明 | 注意点 |
|---|---|---|
| ラベルエンコーディング | カテゴリ→整数 | 順序がある場合のみ。木モデルは順序仮定なしで使用可 |
| One-Hotエンコーディング | カテゴリ→ダミー変数 | 高カーディナリティでは次元爆発 |
| Ordinalエンコーディング | 順序カテゴリ→順序付き整数 | 順序関係が明確な場合 |
| Targetエンコーディング | カテゴリ→目的変数の平均 | リーク防止のためfold内で計算 |
| Frequency/Countエンコーディング | カテゴリ→出現頻度 | 情報量は少ないが安全 |
| Binary/Hashエンコーディング | カテゴリ→ビット/ハッシュ | 超高カーディナリティ向け |

#### その他の特徴量生成
- **ビニング**: 連続値→カテゴリ（等幅/等頻度/決定木ベース）
- **多項式特徴量**: x₁², x₁×x₂（交互作用項）
- **日時特徴量**: 年/月/日/曜日/時間帯/祝日フラグ/サイクル（sin/cos変換）
- **集約特徴量**: グループごとの統計量（mean/std/min/max/count）
- **ラグ特徴量**: 過去の値（t-1, t-7, t-30）。時系列漏洩に注意
- **ローリング特徴量**: 移動平均、移動標準偏差

### 1.5 実務活用: 前処理パイプライン設計

```python
# scikit-learn Pipeline + ColumnTransformer の基本構成
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer([
    ('num', numeric_pipeline, numeric_features),
    ('cat', categorical_pipeline, categorical_features)
])
```

**パイプライン設計チェックリスト**:
1. 学習データのみでfit → テストデータにtransform（データ漏洩防止）
2. 欠損値処理 → 外れ値処理 → エンコーディング → スケーリング の順序
3. 特徴量選択はクロスバリデーション内で実施
4. 前処理パラメータも含めてバージョン管理

---

## 2. データベース・SQL

### 2.1 リレーショナルDB設計

#### 正規化

| 正規形 | 条件 | 解消する問題 |
|---|---|---|
| 第1正規形 (1NF) | 全属性が原子値 | 繰り返しグループ |
| 第2正規形 (2NF) | 1NF + 部分関数従属の排除 | 複合キーの一部への依存 |
| 第3正規形 (3NF) | 2NF + 推移的関数従属の排除 | 非キー属性間の依存 |
| BCNF | 全ての決定項が候補キー | 候補キーでない決定項 |

**分析用DBでは意図的な非正規化も有効**:
- スタースキーマ: 中心にファクトテーブル（数値）、周囲にディメンションテーブル（属性）
- スノーフレークスキーマ: ディメンションをさらに正規化
- ワイドテーブル: JOINを減らすための非正規化（BQ/Redshift等で有効）

#### インデックス設計

| 種類 | 特徴 | 用途 |
|---|---|---|
| B-Treeインデックス | 範囲検索・ソート効率的 | 汎用（WHERE, ORDER BY） |
| ハッシュインデックス | 等値検索のみ。O(1) | 完全一致検索 |
| GINインデックス | 転置インデックス | 全文検索、配列、JSONB |
| カラムナインデックス | 列指向圧縮 | OLAP、集計クエリ |
| カバリングインデックス | 必要な列をすべて含む | インデックスのみで応答 |

### 2.2 Window関数

```sql
-- ROW_NUMBER: 行番号付与（重複なし）
SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
FROM employees;

-- RANK / DENSE_RANK: 順位付け
-- RANK: 同順位があると次の順位を飛ばす (1,2,2,4)
-- DENSE_RANK: 飛ばさない (1,2,2,3)

-- LAG / LEAD: 前後の行の値を参照
SELECT date, sales,
       LAG(sales, 1) OVER (ORDER BY date) AS prev_day_sales,
       sales - LAG(sales, 1) OVER (ORDER BY date) AS daily_diff
FROM daily_sales;

-- 移動平均
SELECT date, sales,
       AVG(sales) OVER (
         ORDER BY date
         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ) AS moving_avg_7d
FROM daily_sales;

-- 累積合計
SELECT date, sales,
       SUM(sales) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) AS cumulative_sales
FROM daily_sales;

-- NTILE: N等分
SELECT *, NTILE(4) OVER (ORDER BY score) AS quartile
FROM students;

-- FIRST_VALUE / LAST_VALUE
SELECT dept, employee, salary,
       FIRST_VALUE(employee) OVER (
         PARTITION BY dept ORDER BY salary DESC
       ) AS top_earner
FROM employees;
```

**Window関数のフレーム指定**:
- `ROWS BETWEEN ... AND ...`: 物理行数ベース
- `RANGE BETWEEN ... AND ...`: 値ベース（同値をまとめて扱う）
- `UNBOUNDED PRECEDING` / `CURRENT ROW` / `UNBOUNDED FOLLOWING`

### 2.3 CTE・サブクエリ最適化

```sql
-- CTE (Common Table Expression): 可読性向上+再利用
WITH monthly_sales AS (
  SELECT DATE_TRUNC('month', date) AS month,
         SUM(amount) AS total
  FROM orders
  GROUP BY 1
),
growth AS (
  SELECT month, total,
         LAG(total) OVER (ORDER BY month) AS prev_total,
         (total - LAG(total) OVER (ORDER BY month))
           / NULLIF(LAG(total) OVER (ORDER BY month), 0) AS growth_rate
  FROM monthly_sales
)
SELECT * FROM growth WHERE growth_rate > 0.1;

-- 再帰CTE: 階層構造の探索
WITH RECURSIVE org_tree AS (
  SELECT id, name, manager_id, 1 AS depth
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, e.manager_id, t.depth + 1
  FROM employees e JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree;
```

**最適化ポイント**:
- `SELECT *` を避け、必要な列のみ取得
- `WHERE` で早期フィルタ（プッシュダウン）
- `JOIN` は小テーブルを先に（オプティマイザ依存だが意識する）
- `EXPLAIN ANALYZE` で実行計画を確認
- マテリアライズドビューで集計結果をキャッシュ

### 2.4 NoSQL

| 種類 | 代表例 | データモデル | 用途 |
|---|---|---|---|
| ドキュメント型 | MongoDB, Firestore | JSON/BSON | 柔軟なスキーマ、CMS |
| Key-Value | Redis, DynamoDB | キー→値 | キャッシュ、セッション |
| カラムナ | Cassandra, HBase | カラムファミリ | 大規模書き込み、時系列 |
| グラフ | Neo4j, Neptune | ノード+エッジ | ソーシャルグラフ、推薦 |
| 時系列 | InfluxDB, TimescaleDB | タイムスタンプ+値 | IoT、監視メトリクス |

**CAP定理**: 分散システムは Consistency / Availability / Partition tolerance の3つのうち同時に2つまでしか保証できない
- CP: MongoDB（パーティション時に一貫性優先）
- AP: Cassandra（パーティション時に可用性優先）

### 2.5 実務活用: 分析用SQLの高速化

**パフォーマンスチューニング手順**:
1. `EXPLAIN ANALYZE` で実行計画を取得
2. フルテーブルスキャン → インデックス追加を検討
3. 大量JOIN → 非正規化 or マテリアライズドビュー
4. 重い集計 → 事前集計テーブル（日次/週次バッチ）
5. パーティションプルーニングが効いているか確認

---

## 3. 分散処理・ビッグデータ

### 3.1 Hadoop/Sparkアーキテクチャ

**Hadoop エコシステム**:
- **HDFS**: 分散ファイルシステム。ブロック（128MB）単位でレプリケーション（デフォルト3）
- **YARN**: リソース管理（CPU/メモリのスケジューリング）
- **MapReduce**: バッチ処理フレームワーク（Map→Shuffle→Reduce）

**Apache Spark**:
- インメモリ処理でMapReduceの10〜100倍高速
- **RDD (Resilient Distributed Dataset)**: 不変の分散コレクション。障害時にリネージから再計算
- **DataFrame API**: RDDの上にスキーマ。Catalyst Optimizerによる最適化
- **Spark SQL**: DataFrameに対するSQL実行
- **Spark Streaming**: マイクロバッチ方式のストリーム処理
- **MLlib**: 分散機械学習ライブラリ

### 3.2 MapReduceパラダイム

```
例: 単語カウント
Input: ["hello world", "hello spark"]

Map Phase:
  "hello world" → [("hello", 1), ("world", 1)]
  "hello spark" → [("hello", 1), ("spark", 1)]

Shuffle Phase:
  "hello" → [1, 1]
  "world" → [1]
  "spark" → [1]

Reduce Phase:
  "hello" → 2
  "world" → 1
  "spark" → 1
```

**MapReduceで表現できる計算**:
- 集計（COUNT, SUM, AVG）
- フィルタリング（Map段階で除外）
- JOIN（Map-side join / Reduce-side join）
- ソート（全順序はTeraSort方式）

### 3.3 パーティショニング戦略

| 戦略 | 説明 | 用途 |
|---|---|---|
| ハッシュパーティション | キーのハッシュ値で分割 | 均等分散、JOIN最適化 |
| レンジパーティション | 値の範囲で分割 | 範囲クエリ、時系列 |
| 日付パーティション | 日/月/年で分割 | ログ、イベントデータ |
| リストパーティション | 特定の値リストで分割 | 地域、カテゴリ |

**データスキュー対策**:
- ソルティング: キーにランダムプレフィックスを付加→後で集約
- ブロードキャスト結合: 小テーブルを全ノードに配布
- Adaptive Query Execution (Spark 3.x): 実行時にスキュー検出・自動対策

### 3.4 ストリーム処理

| フレームワーク | 処理方式 | レイテンシ | 特徴 |
|---|---|---|---|
| Apache Kafka | メッセージブローカー | ms〜s | 耐久性、高スループット |
| Apache Flink | ネイティブストリーム | ms | 正確な1回処理、イベント時間 |
| Spark Structured Streaming | マイクロバッチ | s〜min | Spark統合、DataFrame API |
| Apache Kafka Streams | ライブラリ型 | ms | デプロイ簡易、JVMアプリ内蔵 |

**ストリーム処理の時間概念**:
- **イベント時間**: データが生成された時刻
- **処理時間**: データが処理された時刻
- **ウォーターマーク**: 遅延データの許容閾値。ウォーターマーク超過 → ドロップ or サイドアウトプット

**処理保証レベル**:
- At-most-once: 重複なし、欠損あり
- At-least-once: 欠損なし、重複あり
- Exactly-once: 重複も欠損もなし（Flink/Kafka Transactionsで実現）

### 3.5 データレイク vs DWH vs レイクハウス

| 特徴 | データレイク | DWH | レイクハウス |
|---|---|---|---|
| ストレージ | オブジェクトストレージ | 専用エンジン | オブジェクト+メタデータ層 |
| スキーマ | On-Read | On-Write | On-Read + 制約 |
| データ形式 | 生データ（any） | 構造化のみ | 構造化+半構造化 |
| コスト | 低い | 高い | 中程度 |
| ACID | なし | あり | あり（Delta Lake等） |
| 代表例 | S3 + Glue | Snowflake, BigQuery | Delta Lake, Apache Iceberg |

**レイクハウスの要素技術**:
- **Delta Lake / Apache Iceberg / Apache Hudi**: ACID対応テーブル形式
- **タイムトラベル**: 過去の任意時点のデータを参照
- **スキーマ進化**: 後方互換なスキーマ変更を安全に実施
- **Zオーダリング/パーティション進化**: 多次元クラスタリングで読み取り最適化

### 3.6 実務活用: 大規模データの効率的処理

**規模別の技術選定目安**:
- 〜1GB: pandas（単一マシン）
- 1〜100GB: polars, DuckDB（シングルノード高速処理）
- 100GB〜1TB: Spark（小規模クラスタ）or クラウドDWH
- 1TB〜: Spark + オブジェクトストレージ or クラウドDWH（BigQuery, Snowflake）

**polars vs pandas**:
- polars: Rust製、遅延評価、マルチスレッド、メモリ効率が高い
- pandas: エコシステム豊富、学習コスト低い、レガシー互換

---

## 4. データ品質管理

### 4.1 データ品質の6次元

| 次元 | 定義 | 測定例 |
|---|---|---|
| 正確性 (Accuracy) | 現実を正しく反映 | 住所の表記ゆれ率、数値の異常値率 |
| 完全性 (Completeness) | 欠損がない | NULL率、レコード欠損率 |
| 一貫性 (Consistency) | システム間で矛盾がない | マスタ間の不一致件数 |
| 適時性 (Timeliness) | 必要な時に最新 | データ遅延時間、更新頻度 |
| 有効性 (Validity) | 定義されたルールに適合 | フォーマット違反率、値域逸脱率 |
| 一意性 (Uniqueness) | 重複がない | 重複レコード率 |

### 4.2 データリネージ・データカタログ

**データリネージ（系譜）**:
- データの「どこから来て、どう加工され、どこへ行くか」を追跡
- カラムレベルリネージ: 各列がどのソース列に由来するかを特定
- ツール: Apache Atlas, dbt lineage, OpenLineage

**データカタログ**:
- メタデータの検索・閲覧プラットフォーム
- 技術メタデータ: テーブル名、カラム型、行数、更新日時
- ビジネスメタデータ: オーナー、説明、タグ、利用用途
- ツール: DataHub, Amundsen, Google Data Catalog

### 4.3 データガバナンス

**データガバナンスフレームワーク**:
- **データオーナー**: データの品質・セキュリティに責任を持つ事業部門
- **データスチュワード**: 日常のデータ品質管理を実行する担当者
- **データポリシー**: アクセス制御、保持期間、匿名化ルール
- **データカタログ**: メタデータの一元管理

**マスターデータ管理 (MDM)**:
- 顧客/商品/従業員等のマスターデータを一元化
- ゴールデンレコード: 複数ソースからの統合（名寄せ）
- 変更管理: 有効開始日/終了日による履歴管理（SCD Type 2）

### 4.4 データ品質テスト

**テスト種類**:
- **スキーマテスト**: カラムの存在・型・NOT NULL制約
- **ボリュームテスト**: レコード数の妥当性（前日比±N%以内）
- **値域テスト**: 最小値/最大値/ユニーク数の範囲
- **関係性テスト**: 参照整合性、外部キー制約
- **鮮度テスト**: 最新レコードのタイムスタンプが許容範囲内

```yaml
# dbt testsの例
models:
  - name: orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: amount
        tests:
          - not_null
          - accepted_values:
              values: ['>0']
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'confirmed', 'shipped', 'delivered']
```

### 4.5 実務活用: データ品質監視ダッシュボード

**品質監視の構成**:
1. **自動チェック**: パイプライン実行ごとにGreat Expectations / dbt testを実行
2. **アラート**: NULL率急増、行数急減、値域逸脱をSlack/PagerDutyに通知
3. **ダッシュボード**: 品質スコアの時系列推移を可視化
4. **SLA**: 「データ遅延10分以内」「NULL率1%以下」等の目標を設定・計測

**Great Expectations 基本フロー**:
1. Expectation Suite定義（期待されるデータ品質条件）
2. Validator実行（データに対してExpectationを検証）
3. Data Docs生成（HTML形式のレポート）
4. Checkpoint自動実行（パイプラインに組み込み）
