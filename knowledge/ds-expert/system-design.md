# データサイエンスシステム設計 — DSエキスパートリファレンス

> 統計検定データサイエンスエキスパート 満点レベル対応
> セクション番号（§）は `index.md` の横断マップから参照される

---

## §1. MLシステムアーキテクチャ

### 1.1 バッチ推論 vs リアルタイム推論

| 特性 | バッチ推論 | リアルタイム推論 |
|------|-----------|-----------------|
| レイテンシ | 分〜時間 | ミリ秒〜秒 |
| スループット | 高（大量一括処理） | 低（1リクエスト単位） |
| 実装複雑度 | 低 | 高（サービング基盤が必要） |
| 用途 | 日次レポート、バッチレコメンド | 検索ランキング、不正検知 |
| コスト | 低（オフピーク活用） | 高（常時稼働） |

**ニアリアルタイム（マイクロバッチ）**: 数秒〜数分間隔でバッチ処理。ストリーム処理のシンプルな代替。

**判断基準**:
- ビジネス要件のレイテンシ許容度が最優先
- バッチで済むならバッチを選ぶ（運用が単純）
- 特徴量の鮮度要件: リアルタイム特徴量が必要ならリアルタイム推論

### 1.2 Feature Store

**目的**: 特徴量の計算・管理・提供を一元化し、学習と推論で同じ特徴量を使う。

**二重計算問題（Training-Serving Skew）**:
- 学習時: バッチパイプラインで過去データから特徴量計算
- 推論時: リアルタイムで同じ特徴量を計算 → ロジック不一致のリスク
- Feature Store が統一的なインターフェースを提供

**構成要素**:
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Offline Store│ ←── │ Feature Store │ ──→ │ Online Store │
│ (データレイク)│     │ (メタデータ)  │     │ (Redis等)    │
└─────────────┘     └──────────────┘     └─────────────┘
     ↑ バッチ計算           │                  ↑ ストリーム
     │                   特徴量定義             │
  学習パイプライン         バージョン管理      推論パイプライン
```

**Offline Store**: 学習用。大量の履歴データをバッチで提供（Parquet/Delta Lake等）。
**Online Store**: 推論用。低レイテンシで最新の特徴量を提供（Redis/DynamoDB等）。

**ツール**: Feast（OSS）、Tecton、Vertex AI Feature Store、SageMaker Feature Store。

**特徴量エンジニアリングの原則**:
- Point-in-Time Join: 予測時点で利用可能だったデータのみ使用（未来情報リーク防止）
- 特徴量のバージョン管理: 計算ロジックの変更をトラッキング
- 特徴量の再利用: チーム間で共有し二重開発を防ぐ

### 1.3 モデルサービング

**TensorFlow Serving**:
- SavedModel形式のモデルを HTTP/gRPC で提供
- バージョン管理（複数バージョン同時稼働可）
- バッチ推論の自動バッチング

**Triton Inference Server (NVIDIA)**:
- TensorRT/ONNX/PyTorch/TensorFlow 等マルチフレームワーク対応
- Dynamic Batching: 個別リクエストを自動的にバッチ化
- Model Ensemble: 複数モデルのパイプラインを定義可能

**ONNX Runtime**:
- フレームワーク非依存の推論ランタイム
- 最適化（グラフ最適化、量子化）が充実
- Edge デプロイにも対応

**モデル最適化**:
| 手法 | 効果 | トレードオフ |
|------|------|------------|
| 量子化 (Quantization) | 推論速度2-4倍、メモリ半減 | 精度微減 |
| 枝刈り (Pruning) | モデルサイズ削減 | 精度微減 |
| 知識蒸留 (Distillation) | 小モデルで大モデルに近い精度 | 学習コスト |
| ONNX変換 | フレームワーク非依存 | 一部の演算子非対応 |

### 1.4 マイクロサービスアーキテクチャ

**MLシステムのサービス分割**:
```
┌──────────┐  ┌───────────┐  ┌──────────┐  ┌─────────┐
│ API GW   │→ │Feature Svc│→ │Predict Svc│→ │Result DB│
└──────────┘  └───────────┘  └──────────┘  └─────────┘
                                    ↓
                             ┌──────────┐
                             │Logging Svc│
                             └──────────┘
```

**設計ポイント**:
- **サーキットブレーカー**: モデルサービス障害時のフォールバック（デフォルト値、キャッシュ値）
- **ヘルスチェック**: モデルの推論レイテンシ監視、しきい値超過で自動再起動
- **カナリアリリース**: 新モデルを一部トラフィックに適用→段階的にロールアウト
- **Shadow Mode**: 新モデルを本番トラフィックで同時実行するが結果は返さない（性能評価のみ）

### 1.5 実務活用

- **EC検索**: Feature Store で直近の閲覧/購入特徴量をリアルタイム提供 → ランキングモデルで推論
- **金融不正検知**: Triton + ストリーム処理でリアルタイムスコアリング（レイテンシ < 100ms）
- **広告CTR予測**: マイクロバッチで特徴量更新 + A/Bテスト基盤で新モデル評価
- **製造業品質管理**: バッチ推論で日次品質レポート + エッジ推論で即座の不良品検出

---

## §2. MLOps

### 2.1 CI/CD for ML

**従来のCI/CDとの違い**:
| 要素 | ソフトウェアCI/CD | ML CI/CD |
|------|-----------------|---------|
| テスト対象 | コード | コード + データ + モデル |
| 成果物 | バイナリ | モデル + 設定 + 特徴量変換パイプライン |
| 再現性 | コードで決定 | コード + データ + 環境 + シード |
| デプロイ後の品質 | バグ有無 | 性能劣化の継続監視 |

**ML CI/CDパイプライン**:
```
┌────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│データ検証│→ │特徴量変換 │→ │モデル学習 │→ │モデル評価 │→ │デプロイ  │
└────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
     ↓              ↓              ↓              ↓
  スキーマ検証   変換の単体テスト  ハイパーパラメータ  性能ゲート
  統計量チェック                   実験トラッキング   閾値チェック
```

**テスト戦略**:
- **データテスト**: スキーマ検証、欠損率、値域チェック、分布ドリフト検出
- **モデルテスト**: 性能閾値（AUC > 0.85等）、スライスベース評価（サブグループ別精度）
- **インフラテスト**: 推論レイテンシ、メモリ使用量、スループット

### 2.2 実験管理

**MLflow**:
```python
import mlflow
with mlflow.start_run():
    mlflow.log_params({"lr": 0.01, "epochs": 100})
    mlflow.log_metrics({"auc": 0.92, "f1": 0.85})
    mlflow.sklearn.log_model(model, "model")
```

**Weights & Biases (wandb)**:
```python
import wandb
wandb.init(project="my-project")
wandb.log({"loss": loss, "accuracy": acc})
wandb.watch(model)
```

**記録すべき情報**:
- ハイパーパラメータ全体
- データのバージョン / 分割方法
- モデルアーキテクチャ
- 評価メトリクス（複数の指標）
- 学習カーブ（過学習の検出）
- ハードウェア環境

### 2.3 モデルレジストリ

**目的**: モデルのライフサイクル管理（開発→ステージング→本番→アーカイブ）。

**管理対象**:
- モデルのアーティファクト（重みファイル）
- メタデータ（学習データバージョン、ハイパーパラメータ、評価結果）
- ステージ遷移の承認フロー
- 依存ライブラリのバージョン

**モデルバージョニング**:
- セマンティックバージョニング: major.minor.patch（API互換性で判断）
- タイムスタンプベース: YYYYMMDD-HHMM
- ハッシュベース: データ+コードのハッシュで一意に特定

### 2.4 データバージョニング

**DVC (Data Version Control)**:
```bash
dvc init
dvc add data/training_data.csv
git add data/training_data.csv.dvc .gitignore
git commit -m "Add training data v1"
dvc push  # リモートストレージにアップロード
```

- Git で `.dvc` ファイル（メタデータ）を管理
- 実データはリモートストレージ（S3/GCS等）に保存
- `dvc checkout` でデータのバージョン切り替え

**Delta Lake / Lakehouse**:
- ACID トランザクション対応のデータレイク
- タイムトラベル: 過去の任意時点のデータにアクセス
- スキーマ強制 / スキーマ進化

### 2.5 モデル監視

**データドリフト検出**:
| 手法 | 特徴 |
|------|------|
| PSI (Population Stability Index) | ビニングベース。PSI > 0.2 で有意なドリフト |
| KS検定 | 2つの分布の最大差。連続変数向き |
| JS距離 (Jensen-Shannon) | 対称なKLダイバージェンス。0〜1の範囲 |
| MMD (Maximum Mean Discrepancy) | カーネルベース。高次元データ対応 |

**概念ドリフト**:
- 入力分布は同じだが P(Y|X) が変化 → モデルの前提が崩壊
- 検出: 予測性能の時系列監視（ウィンドウ比較）
- 対処: 定期的な再学習 / トリガーベースの再学習

**監視ダッシュボード**:
- 推論レイテンシ（P50/P95/P99）
- 予測分布のシフト
- 特徴量の統計量変化
- ビジネスKPIとの相関

**ツール**: Evidently AI、NannyML、WhyLabs、Arize。

### 2.6 実務活用

- **金融**: モデルレジストリで規制対応（モデルの系譜・評価記録の保持）
- **EC**: A/Bテスト基盤とMLflowの統合で新モデルの段階的ロールアウト
- **医療**: DVC + Delta Lake で学習データの完全な監査証跡
- **製造業**: Evidentlyで入力画像の分布変化を監視（照明条件の変化等）

---

## §3. データパイプライン設計

### 3.1 ワークフローオーケストレーション

**Apache Airflow**:
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

dag = DAG('ml_pipeline', start_date=datetime(2024,1,1), schedule_interval='@daily')

extract = PythonOperator(task_id='extract', python_callable=extract_data, dag=dag)
transform = PythonOperator(task_id='transform', python_callable=transform_data, dag=dag)
train = PythonOperator(task_id='train', python_callable=train_model, dag=dag)

extract >> transform >> train
```

**Dagster**:
- Software-Defined Assets: データ資産中心の設計思想
- 型安全: 入出力の型定義によるパイプラインの整合性検証
- テスト容易: 単体テストが書きやすいアーキテクチャ

**Prefect**: Pythonネイティブ。デコレータベースのシンプルなAPI。

**ツール比較**:
| 特性 | Airflow | Dagster | Prefect |
|------|---------|---------|---------|
| パラダイム | タスク中心 | 資産中心 | タスク中心 |
| 設定 | 複雑 | 中程度 | シンプル |
| テスト性 | 低 | 高 | 中 |
| スケーラビリティ | 高（実績豊富） | 高 | 高 |
| コミュニティ | 最大 | 成長中 | 成長中 |

### 3.2 ストリーム処理 vs バッチ処理

**バッチ処理**:
- Apache Spark: 大規模データの分散バッチ処理。DataFrame API。
- 実行頻度: 時間/日次/週次
- 用途: ETL、特徴量計算、モデル学習

**ストリーム処理**:
- Apache Kafka: メッセージキュー。プロデューサ→トピック→コンシューマ
- Apache Flink: ストリーム処理エンジン。Exactly-Once保証。
- Kafka Streams: Kafkaネイティブのストリーム処理ライブラリ。

**Lambda Architecture**:
```
┌─────────────────────────────────────────┐
│            Serving Layer                │
│  (バッチ結果 + リアルタイム結果を統合)     │
└──────────────┬──────────────────────────┘
               │
   ┌───────────┴───────────┐
   │                       │
┌──┴──────────┐  ┌────────┴─────────┐
│ Batch Layer │  │ Speed Layer      │
│ (Spark等)   │  │ (Flink/Kafka等)  │
│ 正確、遅い   │  │ 近似、速い       │
└─────────────┘  └──────────────────┘
```

**Kappa Architecture**: ストリーム処理のみで構成（バッチ層なし）。シンプルだが全てのユースケースに適するわけではない。

### 3.3 データ品質チェック

**Great Expectations**:
```python
import great_expectations as gx

context = gx.get_context()
validator = context.sources.pandas_default.read_dataframe(df)
validator.expect_column_values_to_not_be_null("user_id")
validator.expect_column_values_to_be_between("age", min_value=0, max_value=150)
validator.expect_column_mean_to_be_between("purchase_amount", 10, 1000)
```

**チェック項目**:
| カテゴリ | チェック内容 |
|----------|------------|
| スキーマ | カラム名、型、順序 |
| 完全性 | 欠損率、レコード数 |
| 値域 | 最小/最大、列挙値 |
| 統計 | 平均、分散、分布形状の変化 |
| 一意性 | 主キーの重複 |
| 参照整合性 | 外部キーの整合性 |
| 鮮度 | データの更新タイムスタンプ |

**データコントラクト**: プロデューサとコンシューマ間のスキーマ・品質の取り決め。SLA的な位置づけ。

### 3.4 冪等性の設計

**冪等性**: 同じ処理を複数回実行しても結果が同一。

**パイプラインでの実現**:
- **UPSERT (INSERT ON CONFLICT UPDATE)**: 重複挿入を回避
- **日付パーティション上書き**: 同じ日の再実行で前回結果を完全に上書き
- **処理済みマーカー**: 処理済みデータにフラグを付与し二重処理を防止
- **トランザクション**: 中間状態を外部に公開しない

**リトライ戦略**:
- Exponential Backoff: 1s → 2s → 4s → ... → 最大待ち時間
- Dead Letter Queue: 規定回数失敗したメッセージを隔離
- 冪等性が保証されていればリトライ安全

### 3.5 実務活用

- **データレイクハウス**: Delta Lake でバッチ+ストリームの統一処理 + Great Expectations でデータ品質ゲート
- **リアルタイム推薦**: Kafka → Flink（特徴量計算）→ Feature Store → 推論API
- **ETLパイプライン**: Airflow で日次ETL + dbt でSQLベースの変換 + テスト
- **ML学習パイプライン**: Dagster でデータ取得→前処理→学習→評価→レジストリ登録を自動化

---

## §4. スケーラビリティ

### 4.1 水平スケーリング

**推論サービスのスケーリング**:
- **Kubernetes (K8s)**: Pod の HPA (Horizontal Pod Autoscaler) でリクエスト量に応じた自動スケール
- **Serverless**: AWS Lambda / Cloud Functions で完全自動スケール（コールドスタート注意）
- **ロードバランシング**: ラウンドロビン、最小接続数、加重方式

**スケーリングの指標**:
| 指標 | スケールアウト判断 | スケールイン判断 |
|------|------------------|-----------------|
| CPU使用率 | > 70% | < 30% |
| リクエストキュー長 | 閾値超過 | キュー空 |
| レイテンシ P95 | SLA超過 | SLA内 |
| GPU使用率 | > 80% | < 20% |

### 4.2 分散学習

**データ並列**:
```
┌──────┐  ┌──────┐  ┌──────┐
│GPU 0 │  │GPU 1 │  │GPU 2 │  ← 同じモデルのコピー
│Data₀ │  │Data₁ │  │Data₂ │  ← データを分割
└──┬───┘  └──┬───┘  └──┬───┘
   └────────┼────────┘
         AllReduce           ← 勾配を集約
```
- **同期**: 全GPUの勾配を待って更新（精度安定、遅いGPUがボトルネック）
- **非同期**: 各GPUが独立に更新（高速だがStale Gradient問題）
- **勾配圧縮**: 通信量削減（Top-K、量子化）

**モデル並列**:
- モデルが1GPUに載らない場合に使用
- レイヤー単位の分割（パイプライン並列）
- テンソル単位の分割（テンソル並列）

**PyTorch分散学習**:
```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

dist.init_process_group("nccl")
model = DDP(model.to(rank), device_ids=[rank])
```

**FSDP (Fully Sharded Data Parallel)**: パラメータ+勾配+オプティマイザ状態を全GPU間でシャーディング → メモリ効率最大化。

**DeepSpeed**: ZeRO Stage 1-3 でメモリ最適化。Stage 3 はFSDPと同等。

### 4.3 GPU活用戦略

**GPU選択ガイド**:
| 用途 | 推奨GPU | VRAM |
|------|---------|------|
| 学習（中規模） | A100 40GB | 40GB |
| 学習（大規模LLM） | A100 80GB / H100 | 80GB+ |
| 推論 | T4 / L4 | 16-24GB |
| 推論（大規模） | A10G / L40S | 24-48GB |

**Mixed Precision Training**:
- FP16/BF16 で計算、FP32 でマスター重み保持
- 学習速度2倍、VRAM半減
- BF16 推奨（Ampere以降のGPU）: FP16よりオーバーフローに強い

**推論最適化**:
- TensorRT: NVIDIAのGPU推論最適化エンジン
- vLLM: LLM推論の高速化（PagedAttention、Continuous Batching）
- Flash Attention: メモリ効率的なAttention計算（O(n)メモリ）

### 4.4 コスト最適化

**スポットインスタンス / Preemptible VM**:
- 通常の60-90%オフ
- チェックポイント必須（中断に備える）
- 学習ジョブに適する（推論サービスには不向き）

**コスト計算の原則**:
```
MLシステム総コスト = 学習コスト + 推論コスト + ストレージ + データ転送
```
- 学習コスト: 一回の実験コスト × 実験回数
- 推論コスト: 通常は学習の10-100倍（長期稼働のため）→ 推論最適化の ROI が高い

**コスト削減戦略**:
| 手法 | 効果 | 実装難易度 |
|------|------|-----------|
| モデル量子化 | 推論コスト50%減 | 低 |
| 知識蒸留 | 推論コスト70%減 | 中 |
| キャッシング | 同一リクエストのコスト0 | 低 |
| 自動スケーリング | オフピーク時のコスト削減 | 中 |
| スポットインスタンス | 学習コスト70%減 | 中 |
| Feature Store共有 | 特徴量計算の重複排除 | 高 |

### 4.5 実務活用

- **LLMファインチューニング**: DeepSpeed ZeRO Stage 3 + スポットインスタンスで学習コスト80%削減
- **推薦サービス**: K8s HPA + TensorRTで推論レイテンシ半減＋自動スケーリング
- **大規模画像分類**: データ並列（DDP）+ Mixed Precision で学習時間を1/4に
- **コスト管理**: 学習=スポット、推論=リザーブドの組み合わせで年間コスト40%削減

---

## 試験対策チェックリスト

- [ ] バッチ推論/リアルタイム推論の選択基準を説明できる
- [ ] Feature Store のOnline/Offline Storeの役割と Training-Serving Skew を説明できる
- [ ] モデルサービングの選択肢（TF Serving/Triton/ONNX）を比較できる
- [ ] カナリアリリース/Shadow Modeの違いと使い分けを判断できる
- [ ] ML CI/CDパイプラインの各ステージのテスト項目を列挙できる
- [ ] MLflow/wandbで記録すべき情報を説明できる
- [ ] データドリフト検出手法（PSI/KS/MMD）の使い分けができる
- [ ] 概念ドリフトとデータドリフトの違いを説明できる
- [ ] Airflow/Dagster/Prefectの設計思想の違いを説明できる
- [ ] Lambda/Kappa Architecture の構造と使い分けを判断できる
- [ ] Great Expectations でのデータ品質チェック項目を設計できる
- [ ] 冪等性の設計パターン（UPSERT/パーティション上書き等）を説明できる
- [ ] データ並列/モデル並列/FSDPの仕組みと使い分けを説明できる
- [ ] Mixed Precision Training（FP16/BF16）の利点と注意点を述べられる
- [ ] MLシステムのコスト最適化戦略を3つ以上挙げられる
