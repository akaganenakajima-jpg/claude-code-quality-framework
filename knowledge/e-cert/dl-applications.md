# 応用技術 — E資格リファレンス

> JDLA E資格 満点レベル。物体検出・セグメンテーション・NLP・音声・強化学習・マルチモーダルを網羅。

---

## 1. 物体検出 (Object Detection)

### 1.1 タスク定義

入力: 画像
出力: バウンディングボックス (x, y, w, h) + クラスラベル + 信頼度スコア

### 1.2 2段階検出器 (Two-Stage Detector)

#### R-CNN → Fast R-CNN → Faster R-CNN の進化

| モデル | 候補領域生成 | 特徴抽出 | 速度 |
|--------|------------|---------|------|
| R-CNN | Selective Search | 候補ごとにCNN | ~50秒/枚 |
| Fast R-CNN | Selective Search | CNN共有+ROI Pooling | ~2秒/枚 |
| Faster R-CNN | RPN (学習ベース) | CNN共有+ROI Pooling | ~0.2秒/枚 |

#### Faster R-CNN の構造

```
画像 → Backbone CNN → 特徴マップ
                         ↓
                   RPN (Region Proposal Network)
                   ├── 物体/背景の二値分類
                   └── バウンディングボックス回帰
                         ↓
                   ROI Pooling/Align
                         ↓
                   分類ヘッド + 回帰ヘッド
```

- **RPN**: 各位置にアンカーボックス（複数のスケール×アスペクト比）を配置
  - 3スケール × 3アスペクト比 = 9アンカー/位置が典型
- **ROI Pooling**: 可変サイズの候補領域を固定サイズに変換
  - ROI Align: 双線形補間で量子化誤差を解消（Mask R-CNN）
- **NMS後に上位N個の候補を分類ヘッドに入力**

#### Feature Pyramid Network (FPN)

```
Bottom-up: C2 → C3 → C4 → C5  [Backbone]
Top-down:  P5 → P4 → P3 → P2  [1×1 Conv + 2× Upsample + 横結合]
```

- マルチスケールの特徴マップで大小の物体を同時に検出
- 小物体: 高解像度の低層特徴 / 大物体: 低解像度の高層特徴

### 1.3 1段階検出器 (One-Stage Detector)

#### YOLO (You Only Look Once)

```
画像 → CNN → S×S グリッド
各セルが:
  B個のバウンディングボックス (x, y, w, h, conf)
  C個のクラス確率
出力テンソル: S × S × (B×5 + C)
```

- 全体を一度に処理 → 高速（リアルタイム30-60fps）
- **YOLOv1**: グリッド1セル2ボックス、解像度低い
- **YOLOv3**: FPN導入、3スケール検出
- **YOLOv5-v8**: anchor-free化、データ拡張強化

#### SSD (Single Shot MultiBox Detector)

```
特徴マップの各位置にアンカーボックス配置
複数スケールの特徴マップから同時に検出
```

- YOLOより多スケール検出に強い（FPN導入前の比較）

#### RetinaNet

```
Backbone + FPN
+ 分類サブネット（Focal Loss）
+ 回帰サブネット
```

- **Focal Loss**: 簡単な背景例のlossを下げ、難しい例に集中
  - `FL = -αₜ(1-pₜ)^γ log(pₜ)`
  - γ=2, α=0.25 が典型
- 1段階で2段階に匹敵する精度を実現（Focal Lossが鍵）

### 1.4 アンカーフリー検出器

#### CenterNet
```
物体中心のヒートマップ → (w, h) を回帰
```
- アンカー不要 → ハイパーパラメータ削減
- NMS不要（中心が1点に定まる）

#### FCOS (Fully Convolutional One-Stage)
```
各ピクセルから4辺への距離 (l, t, r, b) を回帰
+ centerness スコアで中心付近の予測を重視
```

### 1.5 NMS (Non-Maximum Suppression)

```
1. 信頼度スコアでソート
2. 最高スコアのボックスを選択
3. IoU > 閾値のボックスを除去
4. 残りで2-3を繰り返し

Soft-NMS: 除去ではなくスコアを減衰
  score *= exp(-IoU²/σ)    [ガウス減衰]
```

### 1.6 評価指標

#### IoU (Intersection over Union)
```
IoU = |A ∩ B| / |A ∪ B|
    = 交差面積 / (A面積 + B面積 - 交差面積)
```

#### mAP (mean Average Precision)
```
1. 各クラスでPR曲線を作成（IoU閾値で正解/不正解判定）
2. AP = PR曲線下面積（11点補間 or 全点補間）
3. mAP = 全クラスのAPの平均

mAP@0.5: IoU閾値0.5（PASCAL VOC基準）
mAP@[0.5:0.95]: IoU=0.5~0.95を0.05刻み（COCO基準、より厳密）
```

### 1.7 実務活用

- リアルタイム（自動運転、監視）: YOLOv8 / YOLOv5
- 高精度（医療画像）: Faster R-CNN + FPN
- 小物体: FPN + 高解像度入力
- 評価: COCO mAP@[0.5:0.95] が標準

---

## 2. セマンティックセグメンテーション

### 2.1 タスク定義

入力: 画像 (H×W×3)
出力: ピクセルごとのクラスラベル (H×W)

### 2.2 FCN (Fully Convolutional Network)

```
入力 → CNN Encoder（プーリングで解像度低下）
→ 1×1 Conv（クラス数チャネル）
→ 転置畳み込みでアップサンプリング
→ ピクセルごとの予測
```

- FC層をConv層に置換 → 任意サイズ入力に対応
- スキップ接続: 低層（高解像度）と高層（高セマンティクス）を結合

### 2.3 U-Net

```
Encoder (左側):            Decoder (右側):
Conv×2 + MaxPool → 64     UpConv + Concat(Skip) + Conv×2 → 64
Conv×2 + MaxPool → 128    UpConv + Concat(Skip) + Conv×2 → 128
Conv×2 + MaxPool → 256    UpConv + Concat(Skip) + Conv×2 → 256
Conv×2 + MaxPool → 512    UpConv + Concat(Skip) + Conv×2 → 512
     ↓ Bottleneck (1024) ↑

Skip Connection: Encoderの各レベルの出力をDecoderに結合（Concat）
```

- **Skip Connection**: 高解像度の空間情報を保持
- 少ないデータでも学習可能（医用画像で特に有効）
- **用途**: 医用画像セグメンテーション（細胞、臓器）

### 2.4 DeepLab

#### Atrous Convolution (Dilated Convolution)
```
通常: 受容野 = 3×3, パラメータ 9
Atrous (rate=2): 受容野 = 5×5, パラメータ 9（間を空ける）
Atrous (rate=4): 受容野 = 9×9, パラメータ 9
```
- 解像度を保ちながら受容野を拡大（プーリングなし → 情報損失なし）

#### ASPP (Atrous Spatial Pyramid Pooling)
```
特徴マップに複数のrateのAtrous Convを並列適用:
rate=1 (1×1 Conv) ─┐
rate=6  ────────────┤
rate=12 ────────────┤── Concat → 1×1 Conv → 出力
rate=18 ────────────┤
GAP ────────────────┘
```
- マルチスケールの文脈情報を捕捉

#### DeepLab v3+
```
Encoder: ResNet/Xception + ASPP
Decoder: 低層特徴量との結合 + アップサンプリング
```

### 2.5 その他のアーキテクチャ

| モデル | 特徴 |
|--------|------|
| PSPNet | Pyramid Pooling Module（4スケールのプーリング結合） |
| SegFormer | Transformer Encoder + 軽量MLPデコーダ |
| Mask2Former | ユニバーサルセグメンテーション（セマンティック/インスタンス/パノプティック） |
| SAM (Segment Anything) | プロンプトベースのゼロショットセグメンテーション |

### 2.6 インスタンスセグメンテーション

```
セマンティック: 「車」クラスのピクセル全部が同じラベル
インスタンス: 「車A」「車B」を区別

Mask R-CNN:
  Faster R-CNN + マスクブランチ（ROIごとにバイナリマスク予測）
  ROI Align が精密なマスク予測に重要
```

### 2.7 評価指標

```
IoU (Intersection over Union):
  IoU_c = |予測∩正解| / |予測∪正解|    [クラスcについて]

mIoU = (1/C) Σ IoU_c    [全クラスの平均]

Dice係数:
  Dice = 2|A∩B| / (|A| + |B|) = 2TP / (2TP + FP + FN)
  IoUとの関係: Dice = 2IoU / (1 + IoU)
```

- **Dice Loss**: `L = 1 - Dice`（クラス不均衡に強い、微分可能な近似を使用）

### 2.8 実務活用

- 医用画像: U-Net（少データ）、nnU-Net（自動設定）
- 自動運転: DeepLab v3+ / SegFormer
- ゼロショット: SAM（プロンプトベース）
- 損失関数: Cross-Entropy + Dice Loss の組合せが一般的

---

## 3. 自然言語処理 (NLP)

### 3.1 トークナイゼーション

#### BPE (Byte Pair Encoding)
```
1. 文字単位の語彙で開始
2. 最頻出の文字ペアを1トークンに統合
3. 語彙サイズに達するまで繰り返し

例: "low" "lower" "newest"
→ l,o,w / l,o,w,e,r / n,e,w,e,s,t
→ lo,w / lo,w,er / ne,w,es,t  (lo統合)
→ low / low,er / new,es,t      (low統合)
```
- GPT系で使用

#### WordPiece
```
BPEと類似だが、尤度ベースで統合ペアを選択
対数尤度の増分が最大のペアを統合
```
- BERT で使用
- 未知語は `##` プレフィックスで分割

#### SentencePiece
```
言語非依存（スペースも1文字として扱う: ▁）
Unigram LM: 全候補からスコア最低のトークンを順に削除
```
- 多言語モデル（mBERT, T5, LLaMA）で使用
- 前処理なし（生テキスト → トークン列）

### 3.2 言語モデル

#### 自己回帰モデル (Autoregressive LM)
```
P(x₁, ..., xₙ) = Π P(xₜ | x₁, ..., xₜ₋₁)
```
- 左→右に逐次生成
- GPT系
- 生成タスクに自然

#### マスク言語モデル (Masked LM)
```
入力: "The [MASK] sat on the [MASK]"
出力: "The cat sat on the mat"
P(x_mask | x_context)
```
- 双方向の文脈を利用
- BERT系
- 理解タスク（分類、QA）に強い

### 3.3 事前学習タスク

| タスク | モデル | 説明 |
|--------|--------|------|
| MLM (Masked LM) | BERT | 15%マスク予測 |
| NSP (Next Sentence) | BERT | 2文の連続性判定 |
| SOP (Sentence Order) | ALBERT | 2文の順序判定（NSPの改良） |
| CLM (Causal LM) | GPT | 次トークン予測 |
| Denoising | T5, BART | ノイズ付きテキストの復元 |
| Span Corruption | T5 | 連続トークンをマスクして復元 |

### 3.4 下流タスク

#### 固有表現認識 (NER)
```
入力: "山田太郎は東京大学の教授です"
出力: [山田太郎/PERSON] は [東京大学/ORG] の教授です

手法: BERT + トークンレベル分類ヘッド（BIOタグ）
  B-PER I-PER O B-ORG I-ORG I-ORG O O O
```

#### 質問応答 (QA)
```
抽出型QA:
  入力: [CLS] 質問 [SEP] 文脈 [SEP]
  出力: 開始位置、終了位置の予測

生成型QA:
  Encoder-Decoder / Decoder-only で回答を生成
```

#### 文書要約
- **抽出型**: 重要な文を選択
- **生成型**: 新しい文を生成（Encoder-Decoder: BART, T5）

### 3.5 LLM (Large Language Model) の基礎

#### スケーリング則 (Scaling Laws)
```
L(N, D, C) ∝ N^(-α_N)    [パラメータ数]
L(N, D, C) ∝ D^(-α_D)    [データ量]
L(N, D, C) ∝ C^(-α_C)    [計算量]

Chinchilla Scaling: 最適にはパラメータ数とデータ量を同比率でスケール
  → 70Bモデルには1.4Tトークン（20×パラメータ数）
```

#### 創発的能力 (Emergent Abilities)
- 一定のモデルサイズを超えると突然現れる能力
  - Few-shot推論、Chain-of-Thought、コード生成
- 閾値は能力・評価指標に依存（連続的に改善している可能性も）

#### RLHF (Reinforcement Learning from Human Feedback)
```
Phase 1: SFT (Supervised Fine-Tuning)
  人間が書いた高品質応答でファインチューニング

Phase 2: Reward Model Training
  人間が複数応答をランク付け → 報酬モデルを学習

Phase 3: PPO (Proximal Policy Optimization)
  報酬モデルのスコアを最大化するようにLLMを更新
  KLペナルティ: SFTモデルから離れすぎないように制約
```

- DPO (Direct Preference Optimization): 報酬モデルなしで直接最適化
  ```
  L_DPO = -log σ(β(log π(y_w|x)/π_ref(y_w|x) - log π(y_l|x)/π_ref(y_l|x)))
  ```

### 3.6 実務活用

- テキスト分類: BERT ファインチューニング（F1で評価）
- 生成: GPT系 + デコーディング戦略（temperature, top-k, top-p）
  - Greedy: 常に最高確率トークン（多様性なし）
  - Beam Search: 上位k候補を保持（翻訳向き）
  - Top-p (Nucleus): 累積確率pまでのトークンからサンプル
- LLMデプロイ: vLLM / TGI（KVキャッシュ + 連続バッチ + PagedAttention）

---

## 4. 音声処理

### 4.1 音声特徴量

#### MFCC (Mel-Frequency Cepstral Coefficients)
```
音声波形 → フレーム分割（25ms窓, 10msシフト）
→ FFT → パワースペクトル → メルフィルタバンク
→ 対数 → DCT → MFCC（通常13次元 + Δ + ΔΔ = 39次元）
```

- メルスケール: 人間の聴覚特性を模倣（低周波は細かく、高周波は粗く）
  - `mel = 2595 log₁₀(1 + f/700)`

#### メルスペクトログラム
```
音声波形 → STFT → パワースペクトル → メルフィルタバンク → 対数
出力: (時間フレーム数, メルビン数) の2D行列
```
- 画像として扱える → CNNで処理可能
- End-to-Endモデルでは生波形入力も（Wav2Vec）

### 4.2 音声認識モデル

#### CTC (Connectionist Temporal Classification)

```
問題: 入力フレーム数 >> 出力文字数（アラインメントが不明）

解法:
  ブランク記号 (ε) を導入
  全ての有効なアラインメントの確率を合計
  P(y|x) = Σ_{a∈Align(y)} Πₜ P(aₜ|x)

デコード: "aaε-bb-εcc" → "abc"（重複とε除去）
```

- 前向き-後ろ向きアルゴリズムで効率的に計算
- **仮定**: 各フレームの出力が独立（言語モデル情報なし）
- **用途**: DeepSpeech, 初期のEnd-to-End音声認識

#### Attention-based Encoder-Decoder
```
入力: 音声特徴量系列
Encoder: CNN + Transformer (or LSTM)
Decoder: 自己回帰で文字/トークンを生成
```
- CTC+Attentionのハイブリッドが主流

#### Wav2Vec 2.0
```
生波形 → CNN Feature Encoder → Transformer
自己教師学習: マスクされたフレームのコンテキスト表現を予測
→ 少量のラベルデータでファインチューニング
```
- 10分のラベル付きデータでも実用的な精度

#### Whisper (OpenAI)
```
入力: 30秒メルスペクトログラム
Encoder: Transformer
Decoder: 自己回帰（テキスト生成）

マルチタスク: 言語検出 / 文字起こし / 翻訳 / タイムスタンプ
68万時間の弱教師データで学習
```
- 多言語対応、ノイズ耐性が高い

### 4.3 音声合成 (Text-to-Speech)

| モデル | 方式 | 特徴 |
|--------|------|------|
| Tacotron 2 | Encoder-Decoder + WaveNet | 高品質、逐次生成 |
| FastSpeech | 非自己回帰 | 高速、並列生成 |
| VITS | VAE + Flow + GAN | End-to-End、高品質 |

### 4.4 実務活用

- 音声認識: Whisper（ゼロショット多言語）
- ストリーミング: CTC系（低遅延）
- 音声合成: VITS / FastSpeech 2
- 音声分類（感情認識等）: Wav2Vec特徴量 + 分類ヘッド
- 話者認識: ECAPA-TDNN / 埋め込みベクトルのコサイン類似度

---

## 5. 強化学習 (Reinforcement Learning)

### 5.1 基本概念

```
エージェント ←→ 環境

状態 sₜ → エージェント → 行動 aₜ → 環境 → 報酬 rₜ + 次の状態 sₜ₊₁

目標: 累積報酬の期待値を最大化
  G = Σ γᵗ rₜ    [γ: 割引率, 0 < γ < 1]
```

#### 価値関数
```
状態価値: V^π(s) = E_π[G | s₀ = s]
行動価値: Q^π(s, a) = E_π[G | s₀ = s, a₀ = a]

ベルマン方程式:
  V^π(s) = Σ_a π(a|s) Σ_{s'} P(s'|s,a)[r + γV^π(s')]
  Q^π(s,a) = Σ_{s'} P(s'|s,a)[r + γΣ_{a'} π(a'|s')Q^π(s',a')]
```

### 5.2 DQN (Deep Q-Network)

```
Q(s, a; θ) ≈ Q*(s, a)    [NNでQ関数を近似]

損失: L = (r + γ max_{a'} Q(s', a'; θ⁻) - Q(s, a; θ))²
```

- **θ⁻**: ターゲットネットワーク（定期的にθをコピー → 学習安定化）

#### Experience Replay
```
遷移 (s, a, r, s') をバッファに保存
ランダムサンプルしてバッチ学習
```
- 効果1: データ効率（同じ経験を複数回使用）
- 効果2: 時間的相関の破壊（i.i.d.に近づける）

#### 改良手法

| 手法 | 改良点 |
|------|--------|
| Double DQN | max の過大評価を修正（行動選択と評価を分離） |
| Dueling DQN | Q = V(s) + A(s,a) に分解（状態価値と優位性） |
| Prioritized ER | TD誤差が大きい経験を優先サンプル |
| Rainbow | 上記全部 + NoisyNet + Categorical DQN + N-step |

### 5.3 方策勾配法 (Policy Gradient)

```
π(a|s; θ)   [NNで方策を直接パラメータ化]

目標: J(θ) = E_π[Σ γᵗ rₜ] を最大化

方策勾配定理:
  ∇J(θ) = E_π[Σₜ ∇log π(aₜ|sₜ;θ) · Gₜ]

REINFORCE:
  θ ← θ + α ∇log π(aₜ|sₜ;θ) · (Gₜ - b)   [b: ベースライン]
```

- **ベースライン b**: 分散を減らす（V(s)が一般的）
- REINFORCE: 高分散（モンテカルロ推定）

### 5.4 Actor-Critic

```
Actor:  方策 π(a|s; θ)
Critic: 価値関数 V(s; w) または Q(s,a; w)

Advantage: A(s,a) = Q(s,a) - V(s) ≈ r + γV(s') - V(s)  [TD誤差]

Actor更新:  θ ← θ + α ∇log π(a|s;θ) · A(s,a)
Critic更新: w ← w - β ∇(r + γV(s';w) - V(s;w))²
```

#### A3C (Asynchronous Advantage Actor-Critic)
- 複数ワーカーが非同期に環境と対話 → パラメータサーバーに勾配を送信
- Experience Replay不要（非同期性が相関を破壊）

### 5.5 PPO (Proximal Policy Optimization)

```
目的関数:
L_CLIP = E[min(rₜ(θ) Âₜ, clip(rₜ(θ), 1-ε, 1+ε) Âₜ)]

rₜ(θ) = π(aₜ|sₜ;θ) / π(aₜ|sₜ;θ_old)   [確率比]
ε = 0.1 ~ 0.2  [クリッピング範囲]
```

- 方策の大きな変更を防ぐ（保守的な更新）
- TRPO（信頼領域制約）の簡易版
- **用途**: ゲーム、ロボット制御、RLHF（LLMの学習）

### 5.6 AlphaGo / AlphaZero

#### AlphaGo (2016)
```
1. 人間の棋譜で教師あり学習（方策ネットワーク）
2. 自己対戦で強化学習（方策改善）
3. 価値ネットワーク（盤面評価）
4. MCTS (Monte Carlo Tree Search) で探索
```

#### AlphaZero (2017)
```
人間の棋譜なし（自己対戦のみ）
入力: 盤面 → ResNet → (方策 p, 価値 v)

MCTS:
  選択: UCB(s,a) = Q(s,a) + c · p(s,a) · √N(s) / (1+N(s,a))
  展開: NN で評価
  更新: Q値を平均報酬で更新
  行動: 訪問回数に比例してサンプル
```

- 囲碁・チェス・将棋を統一アルゴリズムで超人的性能
- NN + MCTS の組合せが鍵

### 5.7 実務活用

- ゲーム: DQN（離散行動）、PPO（連続行動）
- ロボット制御: SAC (Soft Actor-Critic)、TD3
- LLMアラインメント: PPO + 報酬モデル（RLHF）
- 推薦システム: バンディットアルゴリズム（探索と活用のバランス）
- シミュレーション環境: OpenAI Gym / Gymnasium

---

## 6. マルチモーダル

### 6.1 CLIP (Contrastive Language-Image Pre-training)

```
画像 → Image Encoder (ViT/ResNet) → 画像埋め込み eᵢ
テキスト → Text Encoder (Transformer) → テキスト埋め込み eₜ

対照学習:
  正ペア（対応する画像-テキスト）: 類似度を最大化
  負ペア（非対応ペア）: 類似度を最小化

損失: InfoNCE (対称的な交差エントロピー)
  L = -log(exp(sim(eᵢ,eₜ)/τ) / Σⱼ exp(sim(eᵢ,eⱼ)/τ))
```

- 4億画像-テキストペアで学習
- **ゼロショット分類**: テキストプロンプト "a photo of a {class}" との類似度で分類
- **用途**: 画像検索、画像分類（ゼロショット）、Stable Diffusionのテキストエンコーダ

### 6.2 マルチモーダル Transformer

#### ViLBERT / LXMERT
```
画像特徴量（物体検出器）+ テキストトークン
→ Cross-Attention で相互参照
→ タスクヘッド
```

#### Flamingo / GPT-4V / Gemini
```
大規模LLM + 視覚エンコーダ
画像 → Visual Encoder → 視覚トークン
[視覚トークン + テキストトークン] → LLM → テキスト出力
```

- Perceiver Resampler: 可変数の視覚特徴を固定数のトークンに圧縮
- In-Context Learning: Few-shot で画像タスクを指示

### 6.3 画像キャプション

```
画像 → CNN/ViT → 特徴量 → Transformer Decoder → キャプション生成
```

- Encoder-Decoder型（Show and Tell）
- BLIP/BLIP-2: 事前学習済みの画像-テキストモデル

### 6.4 VQA (Visual Question Answering)

```
入力: 画像 + 質問テキスト
処理: 画像特徴量 + テキスト特徴量 → 融合 → 回答生成/選択
```

- 融合方法: Cross-Attention、Bilinear Pooling、MLP融合
- 現在はLMM（Large Multimodal Model）がEnd-to-Endで解決

### 6.5 テキスト→画像生成

```
DALL-E: dVAE + 自己回帰Transformer
DALL-E 2: CLIP画像埋め込み → 拡散モデルで画像生成
Stable Diffusion: CLIPテキストエンコーダ + 潜在空間拡散 + VAEデコーダ
Imagen: T5テキストエンコーダ + カスケード拡散モデル
```

### 6.6 音声-テキストマルチモーダル

```
AudioLM: 音声→テキスト→音声の統一モデル
SpeechGPT: LLMに音声トークンを追加
```

### 6.7 実務活用

- 画像検索: CLIP埋め込みのコサイン類似度
- 画像理解: GPT-4V / Gemini（汎用VQA）
- 画像生成: Stable Diffusion + ControlNet（条件付き生成）
- 動画理解: 時系列フレームのマルチモーダル処理
- 評価: CLIPScore（画像-テキスト一致度）

---

## 付録: 応用技術の試験対策ポイント

### A. 物体検出の計算問題
- アンカーボックスの数: 特徴マップサイズ × アンカー数/位置
- NMSの手順を正確に記述できること

### B. Transformerの応用パターン
| タスク | エンコーダ | デコーダ |
|--------|----------|---------|
| 分類 | BERT (Encoder-only) | - |
| 生成 | - | GPT (Decoder-only) |
| 翻訳/要約 | T5/BART (Enc-Dec) | T5/BART |
| 画像分類 | ViT (Encoder-only) | - |
| 物体検出 | DETR (Enc-Dec) | DETR |

### C. 強化学習の分類
| 手法 | 方策 | 価値関数 | On/Off Policy |
|------|------|---------|--------------|
| Q-learning/DQN | 暗黙的(ε-greedy) | Q(s,a) | Off-policy |
| REINFORCE | 明示的 π(a|s) | なし | On-policy |
| A3C/A2C | π(a|s) | V(s) | On-policy |
| PPO | π(a|s) | V(s) | On-policy |
| SAC | π(a|s) | Q(s,a) | Off-policy |
| DDPG/TD3 | μ(s) (決定的) | Q(s,a) | Off-policy |
