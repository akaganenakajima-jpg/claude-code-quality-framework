# 深層学習アーキテクチャ — E資格リファレンス

> JDLA E資格 満点レベル。各アーキテクチャの数理・構造・計算量・実装を網羅。

---

## 1. 畳み込みニューラルネットワーク (CNN)

### 1.1 畳み込み演算

#### 基本パラメータ
- **カーネル (フィルタ)**: K×K の重み行列（学習パラメータ）
- **ストライド (S)**: カーネルの移動幅
- **パディング (P)**: 入力の周囲にゼロを追加
- **ディレーション (D)**: カーネル要素間の間隔（Atrous/Dilated Convolution）

#### 出力サイズ計算（超頻出）

```
出力サイズ = floor((入力サイズ + 2P - D(K-1) - 1) / S) + 1

D=1（通常の畳み込み）の場合:
  出力サイズ = floor((入力サイズ + 2P - K) / S) + 1
```

例: 入力 32×32, K=5, S=1, P=2
→ `(32 + 4 - 5)/1 + 1 = 32` (same padding)

例: 入力 32×32, K=5, S=2, P=0
→ `(32 + 0 - 5)/2 + 1 = 14`

#### パラメータ数の計算

```
パラメータ数 = K × K × Cᵢₙ × Cₒᵤₜ + Cₒᵤₜ (bias)
```

例: 3×3, 入力64ch, 出力128ch
→ `3×3×64×128 + 128 = 73,856`

#### 計算量 (FLOPs)

```
FLOPs = K × K × Cᵢₙ × Cₒᵤₜ × Hₒᵤₜ × Wₒᵤₜ × 2
```
（乗算と加算を別々にカウントする場合は×2を省略）

### 1.2 プーリング

| 種類 | 計算 | 特徴 |
|------|------|------|
| Max Pooling | 領域内の最大値 | エッジ・テクスチャの保持 |
| Average Pooling | 領域内の平均値 | 滑らかなダウンサンプリング |
| Global Average Pooling (GAP) | チャネル全体の平均 | FC層の代替（パラメータ削減） |

- Max Pooling: 微小な位置ずれに頑健（平行移動不変性）
- GAP: 入力サイズに依存しない → 可変サイズ入力に対応

### 1.3 1×1 畳み込み

```
パラメータ数 = 1 × 1 × Cᵢₙ × Cₒᵤₜ = Cᵢₙ × Cₒᵤₜ
```

- **用途1**: 次元削減（チャネル数を減らす → 計算量削減）
- **用途2**: チャネル間の線形結合（Network in Network）
- **用途3**: ボトルネック構造（ResNet）の入り口/出口

### 1.4 転置畳み込み (Transposed Convolution)

```
出力サイズ = (入力サイズ - 1) × S - 2P + K + output_padding
```

- アップサンプリング（解像度を上げる）
- **注意**: 「逆畳み込み (deconvolution)」は誤用（数学的な逆演算ではない）
- チェッカーボードアーティファクト: ストライドとカーネルサイズが合わないと発生
  - 対策: Upsample + 通常Conv が安定

### 1.5 深さ方向分離可能畳み込み (Depthwise Separable Convolution)

```
[通常の畳み込み]
パラメータ: K² × Cᵢₙ × Cₒᵤₜ

[Depthwise Separable]
Step 1 - Depthwise: K² × Cᵢₙ  (各チャネル独立にK×K畳み込み)
Step 2 - Pointwise: 1² × Cᵢₙ × Cₒᵤₜ  (1×1畳み込みでチャネル統合)
合計: K² × Cᵢₙ + Cᵢₙ × Cₒᵤₜ

削減率: ≈ 1/Cₒᵤₜ + 1/K² ≈ 1/K² (K=3で約1/9)
```

- **用途**: MobileNet, EfficientNet（軽量モデル）

### 1.6 代表的アーキテクチャの進化

| モデル | 年 | 層数 | Top-5 (ImageNet) | 主な貢献 |
|--------|-----|------|-------------------|---------|
| LeNet-5 | 1998 | 5 | - | CNN の原型 |
| AlexNet | 2012 | 8 | 16.4% | ReLU, Dropout, GPU学習 |
| VGG-16 | 2014 | 16 | 7.3% | 3×3カーネル統一 |
| GoogLeNet | 2014 | 22 | 6.7% | Inceptionモジュール, 1×1 Conv |
| ResNet-152 | 2015 | 152 | 3.6% | 残差結合 (Skip Connection) |
| DenseNet | 2017 | 121+ | 3.5% | Dense Connection |
| EfficientNet | 2019 | B0-B7 | 2.9% | 複合スケーリング |
| ConvNeXt | 2022 | - | - | ViTの知見をCNNに逆輸入 |

#### VGG の設計思想
- 3×3を2層重ねると5×5と同等の受容野（パラメータは少ない）
  - `3×3×2 = 18` vs `5×5 = 25` パラメータ
  - かつ非線形性が増える（ReLUが2回）

#### GoogLeNet (Inception)
- **Inceptionモジュール**: 1×1, 3×3, 5×5, MaxPool を並列に実行→結合
- 1×1 Conv でボトルネック（次元削減してから大きいカーネル）
- 補助分類器（学習時のみ、勾配消失対策）

#### ResNet の残差結合

```
基本ブロック:     h(x) = F(x) + x          [Identity Shortcut]
ボトルネック:     1×1(256→64) → 3×3(64→64) → 1×1(64→256) + x
次元が異なる場合: h(x) = F(x) + Wₛx        [Projection Shortcut]
```

- **なぜ効くか**:
  1. 勾配のショートカット: `∂h/∂x = ∂F/∂x + I` → 最低でも恒等写像の勾配が流れる
  2. 残差を学習する方が容易（ゼロに近い残差 vs 恒等写像の直接学習）
  3. アンサンブル的解釈（パスの組合せ爆発）

#### DenseNet
```
xₗ = Hₗ([x₀, x₁, ..., xₗ₋₁])   [全先行層の出力を結合]
```
- 特徴量の再利用 → パラメータ効率が高い
- 成長率 (Growth Rate) k: 各層で追加するチャネル数

#### EfficientNet
```
複合スケーリング:
  depth:  d = α^φ
  width:  w = β^φ
  resolution: r = γ^φ
  制約: α·β²·γ² ≈ 2
```
- 深さ/幅/解像度をバランスよくスケーリング
- MBConvブロック（MobileNetV2のInverted Residual + SE）

### 1.7 受容野 (Receptive Field) の計算

```
RFₗ = RFₗ₋₁ + (Kₗ - 1) × Πᵢ₌₁ˡ⁻¹ Sᵢ
```

例: Conv(K=3,S=1) → Conv(K=3,S=1) → Conv(K=3,S=1)
→ RF = 1 + 2 + 2 + 2 = 7

例: Conv(K=3,S=2) → Conv(K=3,S=1)
→ RF = 1 + 2 + 2×2 = 7

- Dilated Conv: `Kₑff = D(K-1) + 1` を使用（受容野を効率的に拡大）

### 1.8 実務活用

- 画像分類: ResNet-50/EfficientNet-B0 から始める
- 特徴量抽出: 事前学習CNNの中間層を利用
- リアルタイム推論: MobileNet/EfficientNet-lite
- 出力サイズ計算は設計時に手で検算する習慣をつける

---

## 2. リカレントニューラルネットワーク (RNN)

### 2.1 基本RNN

```
hₜ = tanh(Wₕₕ hₜ₋₁ + Wₓₕ xₜ + bₕ)
yₜ = Wₕᵧ hₜ + bᵧ
```

- 時刻tの隠れ状態 hₜ は、前の隠れ状態 hₜ₋₁ と現在の入力 xₜ に依存
- **BPTT (Backpropagation Through Time)**: 時間方向に展開して逆伝播

#### BPTT の問題
```
∂L/∂hₜ = Π ∂hₖ₊₁/∂hₖ = Π Wₕₕᵀ · diag(tanh'(zₖ))
```
- T ステップで W を T回掛ける → 勾配消失（|λ|<1）/ 爆発（|λ|>1）
- **Truncated BPTT**: T ステップごとに切断（実用的な妥協）

### 2.2 LSTM (Long Short-Term Memory)

```
忘却ゲート:  fₜ = σ(Wf · [hₜ₋₁, xₜ] + bf)
入力ゲート:  iₜ = σ(Wi · [hₜ₋₁, xₜ] + bi)
候補セル:    C̃ₜ = tanh(Wc · [hₜ₋₁, xₜ] + bc)
セル状態:    Cₜ = fₜ ⊙ Cₜ₋₁ + iₜ ⊙ C̃ₜ
出力ゲート:  oₜ = σ(Wo · [hₜ₋₁, xₜ] + bo)
隠れ状態:    hₜ = oₜ ⊙ tanh(Cₜ)
```

- **⊙**: 要素積 (Hadamard product)
- **セル状態 C**: 勾配のハイウェイ（加算のみで伝播 → 勾配消失を緩和）
- **忘却ゲート f**: 過去の情報をどれだけ保持するか
- **入力ゲート i**: 新しい情報をどれだけ取り込むか
- **出力ゲート o**: セル状態のどの部分を出力するか

パラメータ数:
```
4 × (h² + h×d + h)   [h=隠れ次元, d=入力次元]
= 4h(h + d + 1)       [4ゲート分]
```

### 2.3 GRU (Gated Recurrent Unit)

```
更新ゲート:  zₜ = σ(Wz · [hₜ₋₁, xₜ])
リセットゲート: rₜ = σ(Wr · [hₜ₋₁, xₜ])
候補状態:    h̃ₜ = tanh(W · [rₜ ⊙ hₜ₋₁, xₜ])
隠れ状態:    hₜ = (1 - zₜ) ⊙ hₜ₋₁ + zₜ ⊙ h̃ₜ
```

#### LSTM vs GRU

| 特性 | LSTM | GRU |
|------|------|-----|
| ゲート数 | 3（忘却/入力/出力） | 2（更新/リセット） |
| 状態 | 隠れ状態 h + セル状態 C | 隠れ状態 h のみ |
| パラメータ | 4h(h+d) | 3h(h+d) |
| 性能 | 長い依存関係に強い | 短い系列で同等以上 |
| 計算速度 | やや遅い | やや速い |

### 2.4 双方向RNN (Bidirectional RNN)

```
→hₜ = RNN_forward(xₜ, →hₜ₋₁)
←hₜ = RNN_backward(xₜ, ←hₜ₊₁)
hₜ = [→hₜ ; ←hₜ]   [結合]
```

- 未来の文脈も利用可能
- **制約**: オンライン処理（ストリーミング）では使えない
- **用途**: テキスト分類、NER（系列全体が利用可能な場合）

### 2.5 Seq2Seq (Encoder-Decoder)

```
Encoder: h₁,...,hₜ = RNN(x₁,...,xₜ)    → context = hₜ
Decoder: y₁,...,yₛ = RNN(context, y₁,...,yₛ₋₁)
```

- **問題**: context ベクトルが固定長 → 長い入力で情報が圧縮されすぎる
- **解決**: Attention機構

### 2.6 Attention機構

#### Bahdanau Attention (加算型)
```
eᵢⱼ = vᵀ tanh(Wₛ sⱼ₋₁ + Wₕ hᵢ)
αᵢⱼ = softmax(eᵢⱼ)
cⱼ = Σ αᵢⱼ hᵢ
```
- Encoder全ステップの隠れ状態の加重和
- sⱼ₋₁: Decoderの前ステップ状態

#### Luong Attention (乗算型)
```
score(sⱼ, hᵢ) = sⱼᵀ Wₐ hᵢ     [General]
              = sⱼᵀ hᵢ          [Dot]
              = vᵀ tanh(Wₐ[sⱼ;hᵢ])  [Concat]
```

| 方式 | 計算量 | 特徴 |
|------|--------|------|
| Bahdanau (加算) | O(d) | 隠れ次元が異なっても可 |
| Luong (乗算) | O(1) | 高速、同次元が前提 |

### 2.7 実務活用

- 時系列予測: LSTM/GRU（ただしTransformerが主流に）
- 短い系列: GRU（パラメータ少・高速）
- 長い依存関係: LSTM + Attention
- 現在のトレンド: RNNはTransformerに置き換わりつつあるが、エッジデバイスや低遅延要件では依然有用
- State Space Models (S4, Mamba): RNNの後継として注目

---

## 3. Transformer

### 3.1 Self-Attention

```
Attention(Q, K, V) = softmax(QKᵀ / √dₖ) V
```

- **Q (Query)**: 注目する側
- **K (Key)**: 注目される側（Qとの類似度を計算）
- **V (Value)**: 実際に取り出す情報
- **スケーリング √dₖ**: dot productが大きくなりすぎるのを防ぐ
  - Q,Kの各要素が分散1の独立変数なら `QKᵀ` の分散は dₖ → √dₖ で割って分散を1に

入力X (n×d) からの Q, K, V の生成:
```
Q = X Wq    (n×d) × (d×dₖ) = n×dₖ
K = X Wk    (n×d) × (d×dₖ) = n×dₖ
V = X Wv    (n×d) × (d×dᵥ) = n×dᵥ
```

### 3.2 Multi-Head Attention

```
MultiHead(Q, K, V) = Concat(head₁, ..., headₕ) Wo
headᵢ = Attention(Q Wqᵢ, K Wkᵢ, V Wvᵢ)
```

- **なぜ複数ヘッド**: 異なる部分空間で異なる関係性を捉える
  - あるヘッドは構文関係、別のヘッドは意味関係を学習
- 典型的設定: h=8, dₖ=dᵥ=d/h（総計算量は1ヘッドと同等）

パラメータ数:
```
Wq, Wk, Wv: 3 × d × d = 3d²
Wo:         d × d = d²
合計:       4d²
```

### 3.3 位置エンコーディング

Attentionは順序情報を持たない → 明示的に位置情報を付与。

#### 正弦波位置エンコーディング（元のTransformer）
```
PE(pos, 2i)   = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```
- 学習不要、任意の長さに外挿可能（理論上）
- 相対位置を線形変換で表現可能: PE(pos+k) = f(PE(pos))

#### 学習可能位置エンコーディング
- 各位置に学習パラメータを割り当て（BERT, GPT）
- 最大系列長に制限される

#### RoPE (Rotary Position Embedding)
```
f(xₘ, m) = Rₘ xₘ    [Rₘ: 回転行列]
⟨f(q,m), f(k,n)⟩ = g(q, k, m-n)   [相対位置のみに依存]
```
- 相対位置情報を回転行列で表現
- **用途**: LLaMA, GPT-NeoX, Mistral

#### ALiBi (Attention with Linear Biases)
```
softmax(QKᵀ/√d - m·|i-j|)   [m: ヘッドごとの傾き]
```
- 位置エンコーディングなし、Attention scoreにバイアスを加算
- 学習時より長い系列への外挿が容易

### 3.4 Feed-Forward Network (FFN)

```
FFN(x) = max(0, xW₁ + b₁)W₂ + b₂    [ReLU版]
FFN(x) = GELU(xW₁ + b₁)W₂ + b₂      [GELU版、BERT/GPT]
```

- 拡張率: 通常 d→4d→d（中間層が4倍）
- **GLU (Gated Linear Unit) 変種**:
  ```
  FFN_GLU(x) = (xW₁ ⊙ σ(xWg))W₂   [SwiGLU: LLaMA等で使用]
  ```

パラメータ数:
```
W₁: d × 4d,  W₂: 4d × d  → 8d²
SwiGLU: d×(8d/3)×2 + (8d/3)×d ≈ 8d²（隠れ次元を8d/3に調整）
```

### 3.5 Transformer ブロック全体

#### Encoder ブロック（BERT型）
```
x' = LayerNorm(x + MultiHeadAttention(x, x, x))   [Self-Attention + 残差]
out = LayerNorm(x' + FFN(x'))                       [FFN + 残差]
```

#### Decoder ブロック（GPT型）
```
x'  = LayerNorm(x + MaskedMultiHeadAttention(x, x, x))  [因果マスク付き]
x'' = LayerNorm(x' + CrossAttention(x', enc, enc))       [Encoder出力を参照]
out = LayerNorm(x'' + FFN(x''))
```

#### 因果マスク (Causal Mask)
```
mask[i][j] = -∞  (j > i)    [未来の位置を参照禁止]
           = 0    (j ≤ i)
```
- `softmax(QKᵀ/√d + mask)` → 未来の注意重みが0に

#### Pre-LN vs Post-LN
```
Post-LN: x + LN(SubLayer(x))    [元のTransformer]
Pre-LN:  x + SubLayer(LN(x))    [GPT-2以降]
```
- Pre-LN: 学習が安定（warmupが不要/少なくて済む）
- Post-LN: 理論的には表現力が高い（適切なwarmupが必要）

### 3.6 計算量

```
Self-Attention: O(n² × d)   [n=系列長, d=次元]
FFN:           O(n × d²)

n < d の場合: FFNがボトルネック
n > d の場合: Attentionがボトルネック
```

- メモリ: Attention行列 n×n を保持 → O(n²)

#### 効率化手法

| 手法 | 計算量 | アイデア |
|------|--------|---------|
| Flash Attention | O(n²d) だが定数改善 | タイリング+再計算でHBMアクセス削減 |
| Sparse Attention | O(n√n) | 固定パターンのスパースAttention |
| Linear Attention | O(nd²) | kernel近似で Q(KᵀV) の順で計算 |
| Sliding Window | O(nwd) | ローカルウィンドウ内のみ（Mistral） |
| Multi-Query Attention | O(n²d/h) | K,Vを全ヘッドで共有 |
| Grouped-Query Attention | MQAとMHAの中間 | K,Vをグループ共有（LLaMA 2） |

### 3.7 代表モデル

#### BERT (Bidirectional Encoder Representations from Transformers)
- **構造**: Encoder のみ
- **事前学習タスク**:
  - MLM (Masked Language Model): 15%のトークンをマスクして予測
    - 80% [MASK], 10% ランダム置換, 10% そのまま
  - NSP (Next Sentence Prediction): 2文が連続しているか判定
- **入力**: [CLS] + Sentence A + [SEP] + Sentence B + [SEP]
- **ファインチューニング**: [CLS]トークンの出力を分類ヘッドに接続

#### GPT (Generative Pre-trained Transformer)
- **構造**: Decoder のみ（因果マスク付き Self-Attention）
- **事前学習**: 次トークン予測（自己回帰）
  - `P(xₜ | x₁, ..., xₜ₋₁)`
- **生成時**: トークンを1つずつ生成（KVキャッシュで高速化）
- **スケーリング則**: パラメータ数・データ量・計算量のべき乗則

#### T5 (Text-to-Text Transfer Transformer)
- **構造**: Encoder-Decoder
- **特徴**: 全NLPタスクを「テキスト→テキスト」に統一
  - 分類: "sentiment: positive"
  - 翻訳: "translate English to German: ..."
  - 要約: "summarize: ..."

#### Vision Transformer (ViT)
```
入力画像 (H×W×C) → パッチ分割 (N個の P×P パッチ)
→ 線形射影 (patch embedding) → + 位置エンコーディング
→ [CLS] トークン追加 → Transformer Encoder → 分類ヘッド
```
- パッチ数: N = HW/P²（例: 224×224, P=16 → N=196）
- 大規模データで学習するとCNNを上回る
- **DeiT**: データ拡張+蒸留でImageNetのみで学習可能に

### 3.8 実務活用

- テキスト分類/NER: BERT系のファインチューニング
- テキスト生成: GPT系（自己回帰）
- 画像分類: ViT/DeiT（大規模データ）、CNN（小規模データ）
- Attention mapの可視化でモデルの判断根拠を解釈
- KVキャッシュによる推論の高速化（自己回帰生成時）

---

## 4. 生成モデル

### 4.1 オートエンコーダ (AE)

#### 基本オートエンコーダ
```
Encoder: z = fθ(x)      [x → 低次元潜在表現 z]
Decoder: x̂ = gφ(z)      [z → 再構成 x̂]
損失:    L = ‖x - x̂‖²    [再構成誤差]
```
- ボトルネック: z の次元 < x の次元 → 情報圧縮
- **用途**: 次元削減、特徴量学習、ノイズ除去

#### Denoising AE
```
x̃ = corrupt(x)          [ノイズを付加]
z = fθ(x̃)
x̂ = gφ(z)
L = ‖x - x̂‖²            [元のクリーンなxとの誤差]
```
- ノイズに頑健な表現を学習

### 4.2 変分オートエンコーダ (VAE)

#### ELBO (Evidence Lower Bound)
```
log p(x) ≥ E_q[log p(x|z)] - KL(q(z|x) ‖ p(z)) = ELBO

損失 L = -ELBO = -E_q[log p(x|z)] + KL(q(z|x) ‖ p(z))
       = 再構成誤差 + KL正則化項
```

- **q(z|x)**: Encoderが出力する近似事後分布（N(μ, σ²)）
- **p(z)**: 事前分布（標準正規分布 N(0, I)）
- **KL項**: 潜在空間を正規分布に近づける → 滑らかな潜在空間

#### 再パラメータ化トリック (Reparameterization Trick)

```
[問題] z ~ N(μ, σ²) からのサンプリングは微分不可能

[解決] ε ~ N(0, I)
       z = μ + σ ⊙ ε     [決定的な関数に変換 → 勾配が計算可能]
```

#### KLダイバージェンス（正規分布の場合）
```
KL(N(μ,σ²) ‖ N(0,1)) = (1/2) Σ (μ² + σ² - log σ² - 1)
```

- β-VAE: `L = 再構成誤差 + β·KL` — β>1 で解きほぐし表現 (disentanglement)
- VQ-VAE: 連続潜在空間ではなく離散コードブック（画像生成の基盤）

### 4.3 GAN (Generative Adversarial Network)

#### ミニマックスゲーム
```
min_G max_D  V(D, G) = E_x[log D(x)] + E_z[log(1 - D(G(z)))]
```

- **Generator G**: ノイズ z → 偽データ G(z)（Dを騙したい）
- **Discriminator D**: 本物/偽物を判定（正しく判定したい）
- **Nash均衡**: D(x) = 0.5（本物と偽物を区別できない状態）

#### 学習の不安定性

| 問題 | 原因 | 対策 |
|------|------|------|
| モード崩壊 (Mode Collapse) | Gが多様性を失い同じ出力ばかり | Minibatch Discrimination, Unrolled GAN |
| 勾配消失 | Dが完璧→Gの勾配が0 | ラベルスムージング、Non-saturating loss |
| 学習不均衡 | D/Gの学習速度の不一致 | TTUR (Two Time-scale Update Rule) |
| 振動 | 収束せず振動 | スペクトル正規化 |

#### Non-saturating GAN Loss
```
元:    L_G = log(1 - D(G(z)))       [Dが強いと勾配消失]
改良:  L_G = -log(D(G(z)))           [勾配が安定]
```

#### WGAN (Wasserstein GAN)
```
L = E_x[D(x)] - E_z[D(G(z))]        [Wasserstein距離]
制約: Dは1-Lipschitz連続
```
- JS divergence → Wasserstein距離（分布が重ならなくても有意な勾配）
- **制約の実装**:
  - Weight Clipping（WGAN）
  - Gradient Penalty（WGAN-GP）: `λ E[(‖∇D(x̂)‖₂ - 1)²]`

#### 代表的GANアーキテクチャ

| モデル | 特徴 |
|--------|------|
| DCGAN | CNNベース、学習安定化のガイドライン |
| Conditional GAN | クラスラベルを条件として入力 |
| Pix2Pix | ペア画像変換（U-Net Generator + PatchGAN D） |
| CycleGAN | 非ペア画像変換（Cycle Consistency Loss） |
| StyleGAN | スタイルベース生成（Mapping Network + AdaIN） |
| Progressive GAN | 低解像度から段階的に学習 |

### 4.4 拡散モデル (Diffusion Model)

#### 前向き過程（ノイズ付加）
```
q(xₜ | xₜ₋₁) = N(xₜ; √(1-βₜ) xₜ₋₁, βₜ I)

任意のtに直接ジャンプ（閉形式）:
q(xₜ | x₀) = N(xₜ; √ᾱₜ x₀, (1-ᾱₜ) I)
ᾱₜ = Πₛ₌₁ᵗ (1 - βₛ)

xₜ = √ᾱₜ x₀ + √(1-ᾱₜ) ε    [ε ~ N(0,I)]
```

#### 逆過程（ノイズ除去）— 学習対象
```
pθ(xₜ₋₁ | xₜ) = N(xₜ₋₁; μθ(xₜ, t), Σθ(xₜ, t))
```

#### DDPM (Denoising Diffusion Probabilistic Models)

学習目標（簡易版）:
```
L_simple = E_t,x₀,ε [‖ε - εθ(xₜ, t)‖²]
```
- ネットワーク εθ はノイズ ε を予測する（U-Net構造）
- 生成: xₜ → xₜ₋₁ → ... → x₀ をT回繰り返す

#### スコアマッチング

```
score: s(x) = ∇_x log p(x)

スコアベース生成:
  x_{t+1} = xₜ + (η/2) sθ(xₜ) + √η zₜ    [Langevin Dynamics]
```

- 拡散モデルとスコアベースモデルは等価（Song et al., 2021）
- **SDE/ODE**: 連続時間定式化 → 確定的サンプリング（DDIM）

#### 条件付き生成
- **Classifier Guidance**: 分類器の勾配を加算
- **Classifier-Free Guidance**: 条件付き/無条件の出力を補間
  ```
  ε̃ = εθ(x,∅) + w·(εθ(x,c) - εθ(x,∅))   [w>1 で条件を強調]
  ```

#### Stable Diffusion
```
画像 → VAE Encoder → 潜在空間 → 拡散過程 → U-Net (+ CLIPテキスト条件) → VAE Decoder → 画像
```
- 潜在空間で拡散（計算効率大幅向上）
- テキスト条件: CLIP text encoder

### 4.5 フローベースモデル (Normalizing Flow)

```
x = fθ(z)    [z ~ N(0,I), f は可逆変換]

log p(x) = log p(z) + log |det(∂z/∂x)|
         = log p(z) - log |det(∂x/∂z)|
```

- **可逆変換**: 正確な対数尤度を計算可能（VAEやGANとの違い）
- **ヤコビアン**: 行列式の効率的計算が鍵

#### Coupling Layer（RealNVP）
```
入力を2分割: x = [x₁, x₂]
y₁ = x₁
y₂ = x₂ ⊙ exp(s(x₁)) + t(x₁)    [s, tは任意のNN]

ヤコビアン行列式 = exp(Σ s(x₁))    [三角行列→対角積]
```

#### GLOW
- 1×1可逆畳み込み（Coupling Layerの拡張）
- Actnorm（バッチ正規化の可逆版）

### 4.6 生成モデル比較

| 特性 | VAE | GAN | Flow | Diffusion |
|------|-----|-----|------|-----------|
| 対数尤度 | 下界(ELBO) | なし | 正確 | 下界 |
| 生成品質 | やや低い | 高い | 中程度 | 最高 |
| 多様性 | 高い | モード崩壊リスク | 高い | 高い |
| 学習安定性 | 安定 | 不安定 | 安定 | 安定 |
| 生成速度 | 高速 | 高速 | 高速 | 低速(逐次) |
| 潜在空間 | 連続・滑らか | 不明確 | 連続 | 不明確 |

### 4.7 実務活用

- 画像生成（高品質）: Stable Diffusion / DALL-E
- 画像生成（リアルタイム）: GAN（StyleGAN）
- データ拡張: VAE / GAN
- 異常検知: AE / VAE（再構成誤差が閾値以上 → 異常）
- テキスト→画像: 拡散モデル + CLIP

---

## 5. グラフニューラルネットワーク (GNN)

### 5.1 グラフデータの基本

```
グラフ G = (V, E)
V: ノード集合 (|V| = n)
E: エッジ集合
A: 隣接行列 (n×n)
X: ノード特徴量行列 (n×d)
D: 次数行列 (対角、Dᵢᵢ = Σⱼ Aᵢⱼ)
```

### 5.2 GCN (Graph Convolutional Network)

```
H^(l+1) = σ(D̃^(-1/2) Ã D̃^(-1/2) H^(l) W^(l))

Ã = A + I    [自己ループ追加]
D̃ᵢᵢ = Σⱼ Ãᵢⱼ
```

- 正規化隣接行列による近傍集約
- 層を重ねると受容野が広がる（k層でk-hop近傍）
- **過平滑化 (Over-smoothing)**: 深くするとノード表現が均一化

### 5.3 GAT (Graph Attention Network)

```
eᵢⱼ = LeakyReLU(aᵀ [Whᵢ ‖ Whⱼ])
αᵢⱼ = softmax_j(eᵢⱼ)
h'ᵢ = σ(Σ_j αᵢⱼ Whⱼ)
```

- エッジごとに注意重みを学習（全近傍を等重みでない）
- Multi-Head Attention も使用可能

### 5.4 メッセージパッシング (Message Passing Neural Network)

```
mᵢ^(l+1) = Σ_j∈N(i) Mₗ(hᵢ^l, hⱼ^l, eᵢⱼ)   [メッセージ集約]
hᵢ^(l+1) = Uₗ(hᵢ^l, mᵢ^(l+1))                  [ノード更新]
```

- GCN/GATはメッセージパッシングの特殊ケース
- M: メッセージ関数、U: 更新関数
- 集約: Sum / Mean / Max

### 5.5 グラフレベルのタスク

```
ノード分類: 各ノードの表現 → 分類器
グラフ分類: Readout関数（全ノード集約）→ 分類器
リンク予測: ノードペアの表現 → スコア
```

- Readout: Mean/Sum/Attention Pooling

### 5.6 実務活用

- **分子設計**: 原子=ノード、結合=エッジ → 物性予測
- **推薦システム**: ユーザー・アイテムの二部グラフ
- **ソーシャルネットワーク**: コミュニティ検出、影響力分析
- **交通予測**: 道路ネットワーク上の流量予測
- **知識グラフ**: エンティティ関係の推論

---

## 付録: アーキテクチャの計算問題チートシート

### A. Conv出力サイズ
```
O = floor((I + 2P - K) / S) + 1
```

### B. Transformerのパラメータ数
```
1ブロック:
  Multi-Head Attention: 4d² + 4d (bias)
  FFN: 8d² + 5d (bias, 拡張率4の場合)
  Layer Norm: 4d (2×, γとβ)
  合計: ≈ 12d²

全体 (L層):
  Embedding: V×d + n×d (トークン+位置)
  Blocks: L × 12d²
  Head: d×V
```

### C. CNNのパラメータ数
```
Conv: K² × Cᵢₙ × Cₒᵤₜ + Cₒᵤₜ
FC:   入力ユニット × 出力ユニット + 出力ユニット
BN:   2 × チャネル数 (γ, β)
```
