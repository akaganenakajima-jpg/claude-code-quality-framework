# 学習手法・最適化 — E資格リファレンス

> JDLA E資格 満点レベル。最適化アルゴリズム・分散学習・転移学習・モデル圧縮を網羅。

---

## 1. 最適化アルゴリズム

### 1.1 確率的勾配降下法 (SGD)

```
θₜ₊₁ = θₜ - η ∇L(θₜ; xᵢ, yᵢ)
```

- ミニバッチ: 1サンプルではなくBサンプルの平均勾配
- **利点**: メモリ効率、勾配ノイズが正則化効果、局所最適解からの脱出
- **欠点**: 学習率の設定が難しい、収束が遅い、条件数が悪い問題で振動

#### バッチサイズの影響

| バッチサイズ | 勾配ノイズ | 汎化性能 | 学習速度 |
|-------------|----------|---------|---------|
| 小 (32-128) | 大 | 良い傾向 | 遅い |
| 大 (1024+) | 小 | やや悪化 | GPU効率良い |

- **線形スケーリング則**: バッチサイズをk倍 → 学習率もk倍（warmup必要）
- **LARS/LAMB**: 大バッチでも学習率を自動調整

### 1.2 モメンタム (Momentum)

```
vₜ = γvₜ₋₁ + η ∇L(θₜ)    [γ=0.9 が典型]
θₜ₊₁ = θₜ - vₜ
```

- 物理的アナロジー: 重いボールが谷を転がる（慣性）
- **効果**: 振動を抑制、平坦な方向に加速
- 損失関数の谷が細長い（条件数が大きい）場合に特に有効

### 1.3 Nesterov Accelerated Gradient (NAG)

```
vₜ = γvₜ₋₁ + η ∇L(θₜ - γvₜ₋₁)    [先読み位置で勾配計算]
θₜ₊₁ = θₜ - vₜ
```

- 「先に進んでから勾配を見る」→ オーバーシュートの抑制
- モメンタムより収束が速い（理論的保証あり）

### 1.4 AdaGrad

```
gₜ = ∇L(θₜ)
Gₜ = Gₜ₋₁ + gₜ²           [勾配の二乗の累積]
θₜ₊₁ = θₜ - η/√(Gₜ + ε) · gₜ
```

- **適応的学習率**: 頻繁に更新されるパラメータは学習率↓、稀なパラメータは学習率↑
- **問題**: 学習率が単調減少 → 学習が早期に停止
- **用途**: スパースデータ（NLP、推薦システム）

### 1.5 RMSprop

```
Eₜ[g²] = ρ Eₜ₋₁[g²] + (1-ρ) gₜ²    [指数移動平均、ρ=0.9]
θₜ₊₁ = θₜ - η/√(Eₜ[g²] + ε) · gₜ
```

- AdaGradの学習率減衰問題を解決（指数移動平均で「忘れる」）
- 非定常問題に適応

### 1.6 Adam (Adaptive Moment Estimation)

```
mₜ = β₁ mₜ₋₁ + (1-β₁) gₜ           [1次モーメント（平均）]
vₜ = β₂ vₜ₋₁ + (1-β₂) gₜ²          [2次モーメント（分散）]
m̂ₜ = mₜ / (1 - β₁ᵗ)                 [バイアス補正]
v̂ₜ = vₜ / (1 - β₂ᵗ)                 [バイアス補正]
θₜ₊₁ = θₜ - η m̂ₜ / (√v̂ₜ + ε)
```

- デフォルト: β₁=0.9, β₂=0.999, ε=1e-8, η=0.001
- **バイアス補正**: 初期ステップで m,v が0に偏るのを補正
  - t=1: `m̂₁ = m₁/(1-0.9) = 10m₁` → 初期の過小評価を補正

- **利点**: ほぼ全ての問題で安定動作、ハイパーパラメータ調整が少ない
- **欠点**: SGD+Momentumより汎化性能が劣ることがある（sharp minima）

### 1.7 AdamW (Weight Decay の正しい実装)

```
[Adam + L2正則化]（誤り）:
  gₜ = ∇L(θₜ) + λθₜ    → 適応的学習率がweight decayを打ち消す

[AdamW]（正しい decoupled weight decay）:
  θₜ₊₁ = θₜ - η m̂ₜ/(√v̂ₜ+ε) - ηλθₜ   → weight decayを勾配更新と分離
```

- Loshchilov & Hutter, 2019
- **実務**: AdamW が現在のデファクトスタンダード（BERT, GPT, ViT全て）

### 1.8 LAMB / LARS（大バッチ最適化）

```
LARS: レイヤーごとに学習率をスケーリング
  ηₗ = η × ‖θₗ‖ / (‖∇L(θₗ)‖ + λ‖θₗ‖)

LAMB: LARS + Adam の組合せ
  レイヤーごとの信頼比率でスケーリング
```

- バッチサイズ 32K-64K でも安定学習
- **用途**: BERT等の大規模モデルの学習時間短縮

### 1.9 学習率スケジューラ

| スケジューラ | 数式/挙動 | 用途 |
|-------------|----------|------|
| StepLR | `η × γ^(epoch//step)` | 定期的に減衰 |
| ExponentialLR | `η × γ^epoch` | 滑らかな減衰 |
| CosineAnnealing | `η_min + 0.5(η_max-η_min)(1+cos(πt/T))` | 周期的に減衰・回復 |
| Warmup + Cosine | 線形warmup → cosine decay | Transformer標準 |
| OneCycleLR | warmup→max→cooldown（1サイクル） | 高速収束 |
| ReduceLROnPlateau | val_loss停滞時に減衰 | 汎用 |

#### Warmup の必要性
- 学習初期: 重みがランダム → 大きな勾配 → 不安定
- Warmup: 学習率を0から徐々に上げる（通常1000-4000ステップ）
- Pre-LN Transformerではwarmupが短くて済む

### 1.10 最適化アルゴリズムの選択指針

```
まず試す: AdamW (lr=1e-4 ~ 3e-4, weight_decay=0.01)
画像分類（CNN）: SGD+Momentum+CosineAnnealing が最強のことも
NLP/Transformer: AdamW + Warmup+Cosine が標準
大バッチ: LAMB/LARS
ファインチューニング: 低い学習率 (1e-5 ~ 5e-5)
```

### 1.11 実務活用

- 学習率は最も重要なハイパーパラメータ → Learning Rate Finder で探索
- AdamW + Warmup+CosineDecay が現在の安全な選択
- 学習が不安定 → 学習率を下げる / warmupを長くする / 勾配クリッピング
- 学習曲線の監視: train_loss と val_loss を同時にプロット

---

## 2. 分散学習

### 2.1 データ並列 (Data Parallelism)

```
[同期SGD]
各GPU: 異なるミニバッチ → 勾配計算
AllReduce: 全GPUの勾配を平均
全GPU: 同じ重みで更新

[非同期SGD]
各GPU: 勾配計算 → パラメータサーバーに送信
パラメータサーバー: 到着順に更新（stale gradient問題）
```

| 方式 | 利点 | 欠点 |
|------|------|------|
| 同期SGD | 収束が安定 | 最遅GPUに律速 |
| 非同期SGD | 待ち時間なし | stale gradient で収束悪化 |

- **AllReduce**: Ring-AllReduce（帯域効率最大）
- **DDP (Distributed Data Parallel)**: PyTorch標準。DataParallelよりGIL問題なし

### 2.2 モデル並列 (Model Parallelism)

#### パイプライン並列
```
GPU 0: Layer 1-10  →  出力をGPU 1に転送
GPU 1: Layer 11-20 →  出力をGPU 2に転送
GPU 2: Layer 21-30

GPipe: マイクロバッチに分割して並列度を上げる
```
- **バブル問題**: パイプラインの充填/排出時にGPUがアイドル
- 対策: マイクロバッチ数を増やす

#### テンソル並列
```
行列乗算 Y = XA を分割:
  A = [A₁, A₂]  → Y = [XA₁, XA₂]  [列分割]
  X = [X₁, X₂], A分割 → Y = X₁A₁ + X₂A₂  [行分割]
```
- Megatron-LM: Transformer の MHA と FFN を効率的にテンソル並列化
- 通信量は大きいが、1層内の並列度が高い

### 2.3 DeepSpeed ZeRO (Zero Redundancy Optimizer)

```
Stage 1: オプティマイザ状態を分割（メモリ4倍削減）
Stage 2: + 勾配を分割（メモリ8倍削減）
Stage 3: + パラメータを分割（メモリ ∝ 1/GPU数）
```

| Stage | 分割対象 | メモリ削減 | 通信量 |
|-------|---------|----------|--------|
| 0 (DDP) | なし | 1× | AllReduce |
| 1 | Optimizer States | ~4× | AllReduce |
| 2 | + Gradients | ~8× | AllReduce |
| 3 | + Parameters | ~N× | AllGather |

- ZeRO-Offload: CPU/NVMe にオフロード（GPU少でも大モデル）

### 2.4 混合精度学習 (Mixed Precision Training)

```
FP32 (32bit): マスター重み保持
FP16/BF16 (16bit): 前向き計算、後ろ向き計算

手順:
1. FP32 重み → FP16にキャスト
2. FP16で前向き・後ろ向き計算
3. FP16勾配 → FP32にキャスト
4. FP32で重み更新
```

#### Loss Scaling
- FP16: 最小値 ≈ 6e-8 → 小さい勾配がアンダーフロー
- 対策: 損失を S 倍してからbackward → 勾配を S で割ってから更新
- Dynamic Loss Scaling: Sを適応的に調整

#### FP16 vs BF16

| 形式 | 指数部 | 仮数部 | 特徴 |
|------|--------|--------|------|
| FP16 | 5bit | 10bit | 精度高、値域狭い（loss scaling必要） |
| BF16 | 8bit | 7bit | 精度低、FP32と同じ値域（安定） |

- BF16: A100以降のGPU対応。loss scaling不要で実装簡単

### 2.5 勾配累積 (Gradient Accumulation)

```
for i in range(accumulation_steps):
    loss = model(batch_i) / accumulation_steps
    loss.backward()       # 勾配を累積

optimizer.step()          # accumulation_steps回分の勾配で更新
optimizer.zero_grad()
```

- 実効バッチサイズ = ミニバッチ × 累積ステップ数
- GPUメモリが足りない場合の対策（速度は低下）
- BNの統計量はミニバッチ単位（累積バッチではない）→ 注意

### 2.6 実務活用

```
GPU 1台: 混合精度(BF16) + 勾配累積
GPU 2-8台: DDP (Distributed Data Parallel)
GPU 8-64台: DDP + パイプライン並列
GPU 64台以上: DeepSpeed ZeRO Stage 2-3

10B+パラメータ: ZeRO-3 + テンソル並列 + パイプライン並列（3D並列）
```

---

## 3. 転移学習・ファインチューニング

### 3.1 基本概念

```
Pre-training (事前学習):
  大規模データで汎用表現を学習（例: ImageNet, Wikipedia）

Fine-tuning (ファインチューニング):
  タスク固有データで全層/一部を更新
```

#### フィーチャー抽出 vs ファインチューニング

| 方式 | 更新パラメータ | データ量 | 精度 |
|------|-------------|---------|------|
| フィーチャー抽出 | 最終層のみ | 少量OK | やや低い |
| 最終数層を更新 | 後ろの数層 | 中程度 | 中程度 |
| 全層更新 | 全層 | 多め推奨 | 最高（過学習リスク） |

- **差分学習率**: 浅い層は低学習率、深い層は高学習率
  ```
  layer_lr = base_lr × decay^(num_layers - layer_idx)
  ```

### 3.2 Parameter-Efficient Fine-Tuning (PEFT)

大規模モデルの全層更新はコスト・メモリが大きい → 少数パラメータのみ更新。

#### LoRA (Low-Rank Adaptation)

```
元の重み W₀ (d×d) は凍結
追加: ΔW = BA    [B: d×r, A: r×d,  r << d]

出力: h = W₀x + BAx

マージ: 推論時に W = W₀ + BA （追加コストなし）
```

- ランク r = 4-64（フルランク d=4096 の1%未満）
- 学習パラメータ: 2dr（元の d² の 2r/d ≈ 0.1-1%）
- **適用先**: Attention の Q, V 射影（K, FFNは効果が薄い傾向）

#### QLoRA (Quantized LoRA)

```
1. ベースモデルを4bit量子化（NF4: Normal Float 4）
2. 量子化された重みは凍結
3. LoRAアダプタのみFP16で学習
4. 二重量子化: 量子化パラメータも量子化
```

- 65Bモデルを単一48GB GPUでファインチューニング可能
- QLoRA ≈ フル精度ファインチューニングの性能（実験的に）

#### Adapter

```
元のTransformerブロック:
  Attention → FFN

Adapter挿入:
  Attention → [Adapter] → FFN → [Adapter]

Adapter: Down-project (d→r) → ReLU → Up-project (r→d) + 残差
```

- LoRAより先行（Houlsby et al., 2019）
- LoRAと違い推論時に追加レイテンシ（マージ不可）

#### Prompt Tuning

```
入力: [soft_prompt_1, ..., soft_prompt_k, x₁, x₂, ..., xₙ]
学習: soft_prompt の埋め込みベクトルのみ更新（モデルは凍結）
```

- 学習パラメータ: k × d（kはプロンプト長、通常20-100）
- モデルが大きいほど全層ファインチューニングに近い性能

#### Prefix Tuning

```
各Transformer層のKey/Valueに学習可能なプレフィックスを追加:
  K = [P_K; K_input]
  V = [P_V; V_input]
```

- Prompt Tuningの一般化（全層にプレフィックス）

### 3.3 PEFT手法の比較

| 手法 | パラメータ数 | 推論コスト | マルチタスク | 実装の簡易さ |
|------|-----------|----------|------------|------------|
| Full FT | 100% | なし | 重み別保存 | 簡単 |
| LoRA | 0.1-1% | なし（マージ可） | アダプタ切替 | 簡単 |
| QLoRA | 0.1-1% | 量子化コスト | アダプタ切替 | やや複雑 |
| Adapter | 1-5% | 追加レイヤー | モジュール差替 | 中程度 |
| Prompt Tuning | 0.01% | プレフィックス | プロンプト差替 | 簡単 |
| Prefix Tuning | 0.1% | プレフィックス | プレフィックス差替 | 中程度 |

### 3.4 実務活用

```
データ多い + GPUリソース豊富: Full Fine-tuning
データ少ない + LLM: LoRA (r=8-16)
GPUメモリ限界: QLoRA (4bit + LoRA)
多タスク同時運用: LoRA（タスクごとにアダプタ切替）
APIのみ利用可: Prompt Tuning / In-Context Learning
```

---

## 4. 知識蒸留 (Knowledge Distillation)

### 4.1 基本フレームワーク

```
Teacher (大モデル、事前学習済み): 凍結
Student (小モデル): 学習対象

損失:
L = α · L_hard + (1-α) · L_soft

L_hard = CE(y_true, σ(z_s))                    [正解ラベルとの交差エントロピー]
L_soft = T² · KL(σ(z_t/T) ‖ σ(z_s/T))         [ソフトラベルのKLダイバージェンス]
```

- **温度 T**: 高いほどソフトラベルが均一化
  - T=1: 通常のSoftmax
  - T=5-20: クラス間の相対関係が強調される
- **T²のスケーリング**: 勾配の大きさを温度で補正

### 4.2 ソフトラベルの意味

```
Teacher出力 (T=1): [0.92, 0.05, 0.03]   — 「猫」に集中
Teacher出力 (T=5): [0.56, 0.24, 0.20]   — 「犬に似ている」情報も含む
```

- 「犬と猫は似ている」というダークナレッジを伝達
- 正解ラベル [1,0,0] にはないクラス間関係の情報

### 4.3 特徴量蒸留

```
L_feat = ‖f_teacher(x) - g(f_student(x))‖²
```

- 中間層の特徴量を模倣（FitNets）
- g: 次元変換用の射影層
- 出力だけでなく「理解の過程」も伝達

### 4.4 自己蒸留 (Self-Distillation)

```
同じアーキテクチャの Teacher → Student
Born-Again Networks: 蒸留を繰り返すと性能が向上
```

### 4.5 実務活用

- BERT → DistilBERT（6層、97%の性能を60%の速度で）
- GPT-4 → 小モデルへの蒸留（APIコスト削減）
- α=0.1-0.5, T=3-20 が典型的な設定範囲
- Teacherが十分大きいことが前提（小さいTeacherからの蒸留は効果薄い）

---

## 5. 量子化・プルーニング

### 5.1 量子化 (Quantization)

FP32 → 低ビット（INT8/INT4）で推論を高速化。

#### 量子化の基本

```
対称量子化:
  q = round(x / scale)
  scale = max(|x|) / (2^(b-1) - 1)

非対称量子化:
  q = round(x / scale) + zero_point
  scale = (max(x) - min(x)) / (2^b - 1)
  zero_point = round(-min(x) / scale)
```

#### PTQ (Post-Training Quantization)

```
学習済みモデル → キャリブレーションデータで統計量取得 → 量子化
```

- 追加学習不要（数百サンプルでキャリブレーション）
- INT8: 精度低下ほぼなし
- INT4: 精度低下あり（大モデルほど頑健）

| 手法 | 特徴 |
|------|------|
| MinMax | 最大最小値でスケール決定（外れ値に弱い） |
| Percentile | 99.9パーセンタイルでクリッピング |
| MSE最小化 | 量子化誤差を最小化するスケール探索 |
| GPTQ | 列ごとの最適量子化（LLM向け） |
| AWQ | 重要な重みを高精度に保つ（活性化分布ベース） |

#### QAT (Quantization-Aware Training)

```
学習時:
  前向き: 量子化→逆量子化をシミュレート（Fake Quantization）
  後ろ向き: Straight-Through Estimator (STE) で勾配を近似
    round() の勾配 ≈ 1（勾配をそのまま通す）

推論時:
  実際の量子化重みで推論
```

- PTQより高精度（特にINT4以下）
- 追加学習コストがかかる

### 5.2 プルーニング (Pruning)

不要な重み/ニューロンを除去してモデルを軽量化。

#### 非構造化プルーニング (Unstructured)
```
閾値以下の重みを0にマスク:
  mask = |w| > threshold
  w_pruned = w ⊙ mask
```
- 任意の重みを個別に除去 → スパース行列
- 高い圧縮率（90-95%除去可能）
- **問題**: スパース行列の高速化にはハードウェアサポートが必要

#### 構造化プルーニング (Structured)
```
フィルタ単位/チャネル単位/ヘッド単位で除去
基準: L1ノルム / Taylor展開 / 勾配ベース
```
- チャネルごと除去 → 密な小さいモデル → 標準ハードウェアで高速化
- 圧縮率は低め（50-70%）

#### Lottery Ticket Hypothesis（宝くじ仮説）

> 大きなランダム初期化ネットワークに、同等の性能を持つ小さなサブネットワーク（当たりくじ）が存在する。

```
1. ランダム初期化 → 学習 → プルーニング
2. 残ったネットワークを初期重みに戻して再学習
3. 「初期値+マスク」がLottery Ticket
```

- 実用的には Iterative Magnitude Pruning (IMP) で実現

### 5.3 その他の軽量化手法

| 手法 | 説明 |
|------|------|
| 蒸留 + プルーニング | Teacher蒸留 → プルーニング → 再蒸留 |
| Neural Architecture Search (NAS) | 自動で最適なアーキテクチャを探索 |
| MobileNet/ShuffleNet | 設計段階で軽量（Depthwise Separable Conv） |
| TensorRT | NVIDIA推論最適化（レイヤー融合、カーネル最適化） |
| ONNX Runtime | クロスプラットフォーム推論最適化 |

### 5.4 実務活用

```
サーバー推論:
  FP32 → BF16/FP16（2倍高速、精度ほぼ同じ）
  → INT8 PTQ（4倍高速、精度わずかに低下）

エッジデバイス:
  INT8 QAT（精度維持）
  + 構造化プルーニング（50%削減）
  + 知識蒸留（小モデルでTeacher同等の精度）

LLM推論:
  GPTQ / AWQ で INT4 量子化
  → 70Bモデルを単一GPU（80GB）で推論可能
```

---

## 付録: ハイパーパラメータ探索

### A. グリッドサーチ
- 全組合せを試す → 次元の呪い（パラメータ数が増えると指数爆発）

### B. ランダムサーチ
- ランダムにサンプリング → グリッドより効率的（Bergstra & Bengio, 2012）
- 重要なパラメータに偶然当たる確率が高い

### C. ベイズ最適化
```
1. 目的関数 f(x) のサロゲートモデル（ガウス過程）を構築
2. 獲得関数（EI, UCB）で次の探索点を決定
3. 実際に評価してサロゲートモデルを更新
4. 繰り返し
```
- 評価回数が少ない場合に有効（1回の評価が高コスト）
- Optuna, Weights & Biases Sweeps

### D. Population Based Training (PBT)
- 複数モデルを並列学習、定期的に成績の良いモデルのHPをコピー+摂動
- HPスケジュールの最適化も同時に実現
