# 統計的機械学習 — 統計リファレンス

> 統計検定1級・満点レベル。各節末に実務活用を付記。

---

## 1. 学習理論の基礎

### 1.1 経験リスク最小化 (ERM)

真のリスク（期待損失）:

$$R(f) = \mathbb{E}_{(x,y)\sim P}[\ell(f(x), y)]$$

経験リスク（訓練データ上の損失）:

$$\hat{R}_n(f) = \frac{1}{n}\sum_{i=1}^{n}\ell(f(x_i), y_i)$$

ERM原理: $\hat{f}_n = \arg\min_{f \in \mathcal{F}} \hat{R}_n(f)$

- 仮説集合 $\mathcal{F}$ が有限なら、大数の法則により $\hat{R}_n(f) \to R(f)$
- 無限の場合は一様収束（uniform convergence）が必要 → VC理論へ

### 1.2 バイアス-バリアンス分解

二乗損失に対する分解:

$$\mathbb{E}[(y - \hat{f}(x))^2] = \text{Bias}[\hat{f}(x)]^2 + \text{Var}[\hat{f}(x)] + \sigma^2$$

- **Bias²**: モデルの表現力不足（過少適合）
- **Variance**: 訓練データへの過敏性（過適合）
- **σ²（ノイズ）**: 削減不可能な誤差（ベイズ誤差）

トレードオフ: モデル複雑度↑ → Bias↓ Variance↑

- 0-1損失（分類）ではこの分解は成立しない（Friedman の分解が別途ある）

### 1.3 VC次元（Vapnik-Chervonenkis dimension）

定義: 仮説集合 $\mathcal{F}$ が**散らす (shatter)** ことのできる最大の点集合サイズ

- 散らす = $n$ 点のあらゆる $2^n$ 通りのラベル付けを実現可能
- d次元線形分類器の VC次元 = $d + 1$
- 有限仮説集合 $|\mathcal{F}|$ のVC次元 ≤ $\log_2 |\mathcal{F}|$
- RBFカーネルSVM の VC次元 = ∞（パラメータ依存で実効的には有限）

VC上界（分類の場合）:

$$R(f) \leq \hat{R}_n(f) + \sqrt{\frac{d_{VC}(\log(2n/d_{VC}) + 1) + \log(4/\delta)}{n}}$$

確率 $1-\delta$ 以上で成立。

### 1.4 PAC学習（Probably Approximately Correct）

定義: アルゴリズム $\mathcal{A}$ が以下を満たすとき PAC学習可能:
- 任意の $\epsilon > 0, \delta > 0$ に対して
- $m \geq m_0(\epsilon, \delta)$ のサンプルで
- 確率 $1-\delta$ 以上で $R(\hat{f}) - R(f^*) \leq \epsilon$

有限仮説集合のサンプル複雑度: $m \geq \frac{1}{\epsilon}(\log|\mathcal{F}| + \log\frac{1}{\delta})$

効率的 PAC 学習: 多項式時間で PAC 学習可能な概念クラス。

### 1.5 ラデマッハ複雑度

経験ラデマッハ複雑度:

$$\hat{\mathfrak{R}}_n(\mathcal{F}) = \mathbb{E}_{\sigma}\left[\sup_{f \in \mathcal{F}} \frac{1}{n}\sum_{i=1}^{n} \sigma_i f(x_i)\right]$$

$\sigma_i \in \{-1, +1\}$ は独立ラデマッハ確率変数（等確率）。

汎化上界: $R(f) \leq \hat{R}_n(f) + 2\mathfrak{R}_n(\mathcal{F}) + \sqrt{\frac{\log(1/\delta)}{2n}}$

VC次元との関係: $\mathfrak{R}_n(\mathcal{F}) \leq \sqrt{\frac{2d_{VC}\log(en/d_{VC})}{n}}$

- ラデマッハ複雑度はデータ依存 → VC上界より通常タイト

### 1.6 汎化誤差の上界

主要な汎化バウンド（歴史順）:

| 手法 | バウンド | 特徴 |
|---|---|---|
| VC理論 | $O(\sqrt{d_{VC}\log n / n})$ | データ非依存 |
| ラデマッハ | $O(\mathfrak{R}_n(\mathcal{F}))$ | データ依存、よりタイト |
| PAC-Bayes | $\text{KL}(q \| p)$ ベース | 事後分布ベース、NN向き |
| アルゴリズム安定性 | $O(1/n)$（一様安定） | 正則化手法に有効 |

### 1.7 正則化の理論的根拠（構造的リスク最小化: SRM）

最小化目標:

$$\hat{f} = \arg\min_{f \in \mathcal{F}} \left[\hat{R}_n(f) + \lambda \Omega(f)\right]$$

- $\Omega(f)$: 正則化項（モデル複雑度ペナルティ）
- L2正則化 ($\|w\|_2^2$): ティホノフ正則化。バリアンス抑制、解は常に一意
- L1正則化 ($\|w\|_1$): スパース解を誘導（§7で詳述）

SRM原理: 仮説集合を $\mathcal{F}_1 \subset \mathcal{F}_2 \subset \cdots$ と入れ子にし、
経験リスク + 複雑度ペナルティが最小の階層を選択。

**実務活用**: モデル複雑度の選択基準
- 学習曲線（訓練/検証誤差 vs サンプル数）でバイアス-バリアンスを診断
- Bias支配 → 特徴量追加・モデル複雑化。Variance支配 → 正則化強化・データ増加
- VC次元は理論的目安。実務では交差検証（§2）を併用

---

## 2. 交差検証・モデル選択

### 2.1 k-fold 交差検証

データを $k$ 分割し、$k-1$ 個で学習・1個で評価を $k$ 回繰り返す。

$$\text{CV}(k) = \frac{1}{k}\sum_{j=1}^{k} \hat{R}_{n_j}^{(-j)}(\hat{f}^{(-j)})$$

| k | バイアス | バリアンス | 計算コスト |
|---|---|---|---|
| 5 | やや高 | 低 | 低 |
| 10 | バランス良 | 中 | 中 |
| LOO ($k=n$) | ほぼ不偏 | 高 | 高（カーネル法は例外: O(n²)で計算可能） |

- 10-fold が一般的推奨（Breiman & Spector 1992, Kohavi 1995）
- LOO のバリアンスが高い理由: 各訓練セットが $n-1$ 点で高度に重複 → 推定値間の相関大

### 2.2 層化交差検証

各foldでクラス比率を維持。不均衡データで必須。

- `StratifiedKFold` (sklearn) で実装
- 回帰では目的変数のビン分割で層化可能

### 2.3 ブートストラップ法

復元抽出でサイズ $n$ のブートストラップ標本を $B$ 回生成。

- 各標本に含まれない確率: $(1-1/n)^n \to 1/e \approx 0.368$
- OOB (Out-of-Bag) 推定: ランダムフォレストで自動的に利用可能

**.632+ 推定量**:

$$\hat{R}^{.632+} = (1-w)\hat{R}_{\text{train}} + w\hat{R}_{\text{OOB}}$$

$w = 0.632 / (1 - 0.368 \times r)$、$r$ は相対過適合率。

- .632推定量は過適合時にバイアス大 → .632+ で補正

### 2.4 情報量規準の統一的理解

| 規準 | 定義 | 特徴 |
|---|---|---|
| AIC | $-2\log L + 2k$ | 予測誤差最小化（LOOの漸近近似） |
| BIC | $-2\log L + k\log n$ | 真のモデル選択（事後確率最大化） |
| WAIC | $-2(\text{lppd} - p_{\text{WAIC}})$ | 完全ベイズ、事後分布利用 |

- AIC: $n \to \infty$ で LOO-CV と漸近等価（Stone 1977）
- BIC: ペナルティが $\log n$ → サンプル大で簡素なモデル選好（一致性あり）
- WAIC: ベイジアンモデルの標準。事後予測分布の点ごと対数尤度を使用
- DIC: WAICの近似。正規性仮定が必要で現在は非推奨

AIC vs BIC の使い分け:
- 予測精度重視 → AIC（過少適合リスクを嫌う）
- 真のモデル同定 → BIC（過適合リスクを嫌う）

**実務活用**: ハイパーパラメータ最適化
- グリッドサーチ + CV: 確実だが計算量 $O(|G|^d \times k \times T)$
- ランダムサーチ: Bergstra & Bengio (2012) で有効性実証。高次元で効率的
- ベイズ最適化（TPE, GP-UCB）: 試行回数が限られるとき最適
- AIC/BIC は尤度ベースモデルでCV代替として高速（線形回帰、GLM等）

---

## 3. 分類手法

### 3.1 線形分類

#### ロジスティック回帰

$$P(y=1|x) = \sigma(w^T x + b) = \frac{1}{1+e^{-(w^T x + b)}}$$

損失関数（負の対数尤度 = 交差エントロピー）:

$$\mathcal{L} = -\sum_{i=1}^{n}[y_i \log p_i + (1-y_i)\log(1-p_i)]$$

- 凸最適化 → 大域的最適解が保証される
- 多クラス拡張: softmax回帰 $P(y=k|x) = \frac{\exp(w_k^T x)}{\sum_j \exp(w_j^T x)}$
- 出力は確率（キャリブレーション良好）→ 閾値調整で precision/recall トレードオフ制御可

#### 線形判別分析 (LDA)

各クラスの条件付き分布を正規分布と仮定: $P(x|y=k) = \mathcal{N}(\mu_k, \Sigma)$

共分散 $\Sigma$ が全クラス共通 → 判別境界は線形。

フィッシャーの判別基準: $w = \Sigma^{-1}(\mu_1 - \mu_2)$（クラス間分散/クラス内分散を最大化）

- QDA（二次判別分析）: クラス毎に $\Sigma_k$ → 判別境界は二次曲面
- LDA は次元削減にも利用可（$K-1$ 次元へ射影）

#### サポートベクターマシン（SVM）

**ハードマージンSVM**（線形分離可能な場合）:

$$\min_{w,b} \frac{1}{2}\|w\|^2 \quad \text{s.t.} \quad y_i(w^T x_i + b) \geq 1, \forall i$$

**ソフトマージンSVM**（線形分離不可能な場合）:

$$\min_{w,b,\xi} \frac{1}{2}\|w\|^2 + C\sum_{i=1}^{n}\xi_i \quad \text{s.t.} \quad y_i(w^T x_i + b) \geq 1-\xi_i, \xi_i \geq 0$$

- $C$: 正則化パラメータ。大 → ハードマージンに近い。小 → マージン違反を許容
- ヒンジ損失: $\ell(y, f(x)) = \max(0, 1-yf(x))$ と等価

#### 双対問題

$$\max_{\alpha} \sum_{i}\alpha_i - \frac{1}{2}\sum_{i,j}\alpha_i\alpha_j y_i y_j x_i^T x_j$$
$$\text{s.t.} \quad 0 \leq \alpha_i \leq C, \quad \sum_i \alpha_i y_i = 0$$

- $\alpha_i > 0$ のデータ点がサポートベクター（全体の一部 → スパース）
- 内積 $x_i^T x_j$ をカーネル $K(x_i, x_j)$ に置換 → カーネルSVM

#### カーネルSVM

$$f(x) = \sum_{i \in SV} \alpha_i y_i K(x_i, x) + b$$

主要カーネル:
- **線形**: $K(x,z) = x^T z$
- **多項式**: $K(x,z) = (\gamma x^T z + r)^d$
- **RBF（ガウス）**: $K(x,z) = \exp(-\gamma\|x-z\|^2)$ — 最も汎用的
- **マテルン**: 滑らかさパラメータ $\nu$ で制御。GP回帰で頻用

RBFの $\gamma$ の意味: 大 → 近傍のみ影響（複雑な境界）、小 → 遠方も影響（滑らかな境界）

**実務活用**: テキスト分類、画像認識
- テキスト: TF-IDF + 線形SVM が高次元スパースデータで依然強力
- 画像: 特徴抽出済みベクトル + RBF-SVM（CNN以前の定番）
- 確率出力が必要な場合: Platt Scaling でロジスティック変換

### 3.2 決定木・アンサンブル

#### 不純度指標

ノード $t$ のクラス $k$ 比率を $p_k$ として:

| 指標 | 定義 | 特徴 |
|---|---|---|
| ジニ不純度 | $\sum_k p_k(1-p_k)$ | CART標準。計算が速い |
| エントロピー | $-\sum_k p_k \log p_k$ | 情報利得。やや遅い |
| 誤分類率 | $1 - \max_k p_k$ | 剪定の評価に使用。分割基準には不向き |

情報利得 = 親ノードの不純度 - 子ノードの加重平均不純度

#### 剪定

- **事前剪定**: 最大深さ、最小サンプル数、最小不純度改善量で成長を制限
- **事後剪定（コスト複雑度剪定）**: $\min_T [\hat{R}(T) + \alpha|T|]$。$\alpha$ は CV で選択

#### バギング（Bootstrap AGGregatING）

1. ブートストラップ標本 $B$ 個を生成
2. 各標本で独立にモデル学習
3. 予測を平均（回帰）or 多数決（分類）

分散削減: $\text{Var}[\bar{f}] = \frac{\rho\sigma^2 + (1-\rho)\sigma^2/B}{1}$ → $B$ 増で $\sigma^2/B$ 項は減るが $\rho\sigma^2$ は残る

#### ランダムフォレスト

バギング + 各分割で $m$ 個の特徴量をランダムに選択（$m \approx \sqrt{p}$ for 分類、$m \approx p/3$ for 回帰）

- 木間の相関 $\rho$ を低減 → バギングより分散がさらに減少
- OOB推定で追加のCV不要
- 超並列化容易

#### ブースティング

**AdaBoost**: 誤分類サンプルの重みを増加させて逐次学習

$$F_T(x) = \sum_{t=1}^{T} \alpha_t h_t(x), \quad \alpha_t = \frac{1}{2}\log\frac{1-\epsilon_t}{\epsilon_t}$$

指数損失 $e^{-yF(x)}$ の逐次最小化と等価。

**勾配ブースティング**: 一般の損失関数に対して、負の勾配（擬似残差）にフィット

$$h_t = \arg\min_h \sum_i \left[-\frac{\partial \ell(y_i, F_{t-1}(x_i))}{\partial F_{t-1}(x_i)} - h(x_i)\right]^2$$

$$F_t(x) = F_{t-1}(x) + \eta h_t(x)$$

$\eta$（学習率/収縮率）: 小さいほど汎化性能↑ だが $T$ を増やす必要

#### XGBoost / LightGBM

**XGBoost**:
- 損失の2次テイラー展開: $\ell(y, \hat{y}+\delta) \approx \ell + g\delta + \frac{1}{2}h\delta^2$
- 最適葉重み: $w^* = -\frac{\sum g_i}{\sum h_i + \lambda}$
- 分割利得: $\text{Gain} = \frac{1}{2}\left[\frac{G_L^2}{H_L+\lambda} + \frac{G_R^2}{H_R+\lambda} - \frac{(G_L+G_R)^2}{H_L+H_R+\lambda}\right] - \gamma$

**LightGBM**:
- GOSS (Gradient-based One-Side Sampling): 勾配大のサンプルを優先
- EFB (Exclusive Feature Bundling): 相互排他的特徴をバンドル
- ヒストグラムベース分割: 連続値をビンに離散化 → $O(n \cdot p)$ → $O(n_{\text{bin}} \cdot p)$
- leaf-wise成長（depth-wiseより高速だが過適合注意）

#### 変数重要度

- **不純度減少 (MDI)**: 各特徴量で分割した際の不純度減少の合計。高カーディナリティ変数にバイアス
- **順列重要度 (MPI)**: OOBデータで特徴量の値をシャッフルした際の精度低下。バイアスなし
- **SHAP (SHapley Additive exPlanations)**: ゲーム理論ベース。各予測に対する各特徴量の貢献度

$$\phi_j = \sum_{S \subseteq N \setminus \{j\}} \frac{|S|!(p-|S|-1)!}{p!}[f(S \cup \{j\}) - f(S)]$$

TreeSHAP: 木構造を利用して $O(TLD^2)$ で厳密計算。

**実務活用**: 特徴量重要度分析、予測モデル
- テーブルデータの分類/回帰: LightGBM がデファクトスタンダード
- 解釈性: SHAP値で個別予測の説明（規制対応・顧客説明）
- 特徴量選択: 順列重要度 + 再帰的特徴量除去 (RFE)

### 3.3 ニューラルネットワーク

#### 普遍近似定理 (Universal Approximation Theorem)

1層の十分広い隠れ層（活性化関数が非定数・有界・連続）で、任意の連続関数を任意の精度で近似可能。

- ただし必要なユニット数は指数的に増大し得る → 深さの利点
- 深いネットワーク: $O(\text{poly}(d))$ ユニットで表現可能な関数クラスが広い

#### 誤差逆伝播法

連鎖律による勾配の効率的計算:

$$\frac{\partial \mathcal{L}}{\partial w_{ij}^{(l)}} = \frac{\partial \mathcal{L}}{\partial z_j^{(l)}} \cdot a_i^{(l-1)}$$

計算量: 順伝播と同じ $O(W)$（$W$は総パラメータ数）。数値微分 $O(W^2)$ より圧倒的に効率的。

#### 正則化手法

| 手法 | 機構 | 効果 |
|---|---|---|
| ドロップアウト | 各ユニットを確率 $p$ で無効化 | アンサンブル近似。共適応防止 |
| 重み減衰 (L2) | $\mathcal{L} + \frac{\lambda}{2}\|w\|^2$ | 重みの大きさを抑制 |
| バッチ正規化 | 各層の入力を正規化 | 内部共変量シフト軽減。学習率↑可 |
| 早期打ち切り | 検証誤差が増加し始めたら停止 | 暗黙の正則化（L2と等価な場合あり） |
| データ拡張 | 訓練データを変換で増殖 | 不変性の注入 |

#### 最適化アルゴリズム

**SGD + モメンタム**:

$$v_t = \beta v_{t-1} + \nabla\mathcal{L}(\theta_t), \quad \theta_{t+1} = \theta_t - \eta v_t$$

**Adam** (Adaptive Moment Estimation):

$$m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t, \quad v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2$$
$$\hat{m}_t = \frac{m_t}{1-\beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1-\beta_2^t}$$
$$\theta_{t+1} = \theta_t - \frac{\eta\hat{m}_t}{\sqrt{\hat{v}_t}+\epsilon}$$

デフォルト: $\beta_1=0.9, \beta_2=0.999, \epsilon=10^{-8}$

- AdamW: 重み減衰を損失に加えるのではなく更新式で直接適用（デカップル正則化）
- 学習率スケジューリング: コサインアニーリング、ウォームアップ+線形減衰が定番

**実務活用**: 複雑な非線形関係のモデリング
- 画像: CNN (ResNet, EfficientNet)。転移学習で少量データでも有効
- テキスト/言語: Transformer (BERT, GPT)。事前学習+ファインチューニング
- 表形式データ: 多くの場合 GBDT > NN（ただし TabNet, FT-Transformer が進展中）

---

## 4. 教師なし学習

### 4.1 クラスタリング

#### k-means

**ロイド法**:
1. 各点を最近傍の中心に割当: $c_i = \arg\min_k \|x_i - \mu_k\|^2$
2. 中心を更新: $\mu_k = \frac{1}{|C_k|}\sum_{i \in C_k} x_i$
3. 収束まで繰り返し

目的関数（WCSS）: $J = \sum_{k=1}^{K}\sum_{i \in C_k}\|x_i - \mu_k\|^2$

- 計算量: $O(nKdT)$（$T$: 反復回数）
- 局所最適解に収束（大域最適の保証なし）

**k-means++ 初期化**: 最初の中心をランダム選択、以降は既存中心からの距離に比例する確率で選択。

$$P(x_i) = \frac{D(x_i)^2}{\sum_j D(x_j)^2}$$

$O(\log K)$ 近似率を保証。

k の選択: エルボー法、シルエット分析、Gap統計量

#### 混合ガウスモデル (GMM) + EMアルゴリズム

$$p(x) = \sum_{k=1}^{K}\pi_k \mathcal{N}(x|\mu_k, \Sigma_k)$$

$\pi_k$: 混合比率（$\sum_k \pi_k = 1$）

**Eステップ**: 負担率の計算

$$\gamma_{ik} = \frac{\pi_k \mathcal{N}(x_i|\mu_k, \Sigma_k)}{\sum_j \pi_j \mathcal{N}(x_i|\mu_j, \Sigma_j)}$$

**Mステップ**: パラメータの更新

$$N_k = \sum_i \gamma_{ik}, \quad \mu_k = \frac{1}{N_k}\sum_i \gamma_{ik} x_i$$
$$\Sigma_k = \frac{1}{N_k}\sum_i \gamma_{ik}(x_i-\mu_k)(x_i-\mu_k)^T, \quad \pi_k = \frac{N_k}{n}$$

- k-meansは GMM の特殊ケース（$\Sigma_k = \epsilon I, \epsilon \to 0$）
- 共分散の形状: full / diagonal / spherical / tied で計算量-表現力トレードオフ

#### DBSCAN

パラメータ: $\epsilon$（近傍半径）、MinPts（コアポイント閾値）

- コアポイント: $\epsilon$ 近傍に MinPts 以上の点
- 境界ポイント: コアポイントの $\epsilon$ 近傍だが自身はコア条件未達
- ノイズポイント: いずれにも属さない

利点: クラスタ数の事前指定不要、任意形状のクラスタ検出、外れ値をノイズとして分離
欠点: 密度が不均一なデータに弱い → HDBSCAN で改善

#### スペクトラルクラスタリング

1. 類似度行列 $W$ を構築（RBFカーネル等）
2. グラフラプラシアン $L = D - W$（$D$: 次数行列）
3. $L$ の固有値分解で最小 $K$ 個の固有ベクトルを取得
4. 固有ベクトル空間で k-means

正規化ラプラシアン: $L_{\text{sym}} = D^{-1/2}LD^{-1/2}$ または $L_{\text{rw}} = D^{-1}L$

- 非凸クラスタの検出に強い（二重の月、同心円等）
- グラフカットの緩和問題と等価（Ncut, RatioCut）

**実務活用**: 顧客セグメンテーション、異常検知
- セグメンテーション: GMM で「各クラスタに属する確率」を出力 → ソフトクラスタリング
- 異常検知: k-means の距離、GMM の対数尤度、DBSCAN のノイズラベルを異常スコアに活用
- Isolation Forest: アンサンブルベースの異常検知（木の平均パス長が短い = 異常）

### 4.2 次元削減

#### PCA（主成分分析）

二重の解釈:
1. **分散最大化**: $w_1 = \arg\max_{\|w\|=1} w^T \Sigma w$ → 共分散行列の最大固有値に対応する固有ベクトル
2. **再構成誤差最小化**: $\min \sum_i \|x_i - \hat{x}_i\|^2$ → 同じ解

寄与率: $\frac{\lambda_k}{\sum_j \lambda_j}$、累積寄与率 80-95% でカットオフを決定

- 確率的PCA (PPCA): $x = Wz + \mu + \epsilon$、潜在変数モデルとして定式化
- カーネルPCA: 非線形次元削減（§6で詳述）

#### t-SNE（t-distributed Stochastic Neighbor Embedding）

高次元での類似度（ガウス）:

$$p_{j|i} = \frac{\exp(-\|x_i-x_j\|^2/2\sigma_i^2)}{\sum_{k\neq i}\exp(-\|x_i-x_k\|^2/2\sigma_i^2)}$$

低次元での類似度（t分布、自由度1）:

$$q_{ij} = \frac{(1+\|y_i-y_j\|^2)^{-1}}{\sum_{k\neq l}(1+\|y_k-y_l\|^2)^{-1}}$$

KLダイバージェンスの最小化: $\text{KL}(P\|Q) = \sum_{ij} p_{ij}\log\frac{p_{ij}}{q_{ij}}$

- t分布を使う理由: 裾が重い → crowding問題を軽減
- perplexity: 実効的な近傍数（5-50が一般的）
- 大域構造は保存されない（距離・クラスタ間の配置は無意味）

#### UMAP（Uniform Manifold Approximation and Projection）

理論的基盤: リーマン幾何学 + ファジィ単体集合

- t-SNE より高速（近似最近傍探索 + SGD最適化）
- 大域構造をより保存
- $n\_neighbors$（局所性）と $min\_dist$（密集度）がハイパーパラメータ

**実務活用**: 高次元データの可視化
- PCA: 線形構造の理解、前処理としての次元削減。説明可能性が高い
- t-SNE/UMAP: 非線形構造の可視化。クラスタの存在確認に有用だが、定量的解釈は困難

---

## 5. EMアルゴリズム

### 5.1 一般定式化

観測データ $X$、潜在変数 $Z$、パラメータ $\theta$

**Eステップ**:

$$Q(\theta|\theta^{(t)}) = \mathbb{E}_{Z|X,\theta^{(t)}}[\log p(X,Z|\theta)]$$

**Mステップ**:

$$\theta^{(t+1)} = \arg\max_\theta Q(\theta|\theta^{(t)})$$

### 5.2 不完全データの尤度

$$\log p(X|\theta) = \log \sum_Z p(X,Z|\theta)$$

直接最大化が困難 → 下界の反復最大化:

$$\log p(X|\theta) \geq \mathbb{E}_q[\log p(X,Z|\theta)] - \mathbb{E}_q[\log q(Z)] = \text{ELBO}$$

EMは $q(Z) = p(Z|X,\theta^{(t)})$ としたELBO最大化と等価。

### 5.3 収束性の証明

$$\log p(X|\theta^{(t+1)}) \geq Q(\theta^{(t+1)}|\theta^{(t)}) + H(Z|X,\theta^{(t)}) \geq Q(\theta^{(t)}|\theta^{(t)}) + H(Z|X,\theta^{(t)}) = \log p(X|\theta^{(t)})$$

- 対数尤度は各反復で単調非減少（等号は収束時のみ）
- 局所最適解への収束は保証。大域最適の保証はない → 複数初期値で実行

### 5.4 変分EM

$p(Z|X,\theta)$ が解析的に計算不可能な場合、$q(Z)$ をパラメトリック族で近似:

$$q(Z) = \prod_j q_j(Z_j) \quad \text{（平均場近似）}$$

各 $q_j$ の最適解: $\log q_j^*(Z_j) = \mathbb{E}_{-j}[\log p(X,Z|\theta)] + \text{const}$

- 変分推論 (VI): 完全ベイズ版。$\theta$ も潜在変数として扱う
- 確率的変分推論 (SVI): ミニバッチ + 自然勾配で大規模データに対応

**実務活用**: 欠測データ処理、混合モデル推定
- 欠測データ: EMで欠測値を潜在変数として扱い周辺化
- トピックモデル (LDA): 変分EMで文書のトピック分布を推定
- 隠れマルコフモデル (HMM): Baum-Welch = EM の特殊ケース

---

## 6. カーネル法

### 6.1 正定値カーネル

定義: 任意の $n$ 点 $\{x_1,...,x_n\}$ に対して、グラム行列 $K_{ij} = K(x_i, x_j)$ が半正定値

**マーサーの定理**: 連続な正定値カーネルは特徴写像 $\phi$ が存在して:

$$K(x,z) = \langle\phi(x), \phi(z)\rangle_{\mathcal{H}}$$

カーネルトリック: 高次元（場合によっては無限次元）の内積を、元の入力空間での関数評価で計算。

RBFカーネルの特徴空間は**無限次元**（テイラー展開で確認可能）。

### 6.2 再生核ヒルベルト空間 (RKHS)

カーネル $K$ に対応する関数空間 $\mathcal{H}_K$:

- 再生性: $f(x) = \langle f, K(x, \cdot)\rangle_{\mathcal{H}_K}$
- RKHS ノルム $\|f\|_{\mathcal{H}_K}$ が関数の「滑らかさ」を測る

### 6.3 表現定理 (Representer Theorem)

正則化問題 $\min_{f \in \mathcal{H}_K} \left[\frac{1}{n}\sum_i \ell(y_i, f(x_i)) + \lambda\|f\|_{\mathcal{H}_K}^2\right]$ の解は:

$$f^*(x) = \sum_{i=1}^{n} \alpha_i K(x_i, x)$$

- 無限次元空間での最適化が $n$ 個の係数 $\alpha$ の最適化に帰着
- 多くのカーネル法の理論的基盤

### 6.4 カーネルリッジ回帰

$$\hat{\alpha} = (K + \lambda I)^{-1}y$$

- 計算量: $O(n^3)$（行列の逆算。大規模データでは近似が必要）
- Nystr\"om近似: $m \ll n$ 個のランドマーク点でカーネル行列を低ランク近似

### 6.5 主要カーネル一覧

| カーネル | $K(x,z)$ | 特徴空間次元 | パラメータ |
|---|---|---|---|
| 線形 | $x^T z$ | $d$ | なし |
| 多項式 | $(\gamma x^T z + r)^d$ | $\binom{d+p}{p}$ | $\gamma, r, d$ |
| RBF（ガウス） | $\exp(-\gamma\|x-z\|^2)$ | $\infty$ | $\gamma$ |
| マテルン | $\frac{2^{1-\nu}}{\Gamma(\nu)}(\sqrt{2\nu}\frac{r}{l})^\nu K_\nu(\sqrt{2\nu}\frac{r}{l})$ | $\infty$ | $\nu, l$ |

マテルンの特殊ケース: $\nu=1/2$ → 指数カーネル、$\nu \to \infty$ → RBF

**実務活用**: 非線形パターン認識
- ガウス過程回帰: カーネルの選択が prior の指定に対応。マテルンカーネルが実務的に汎用性高い
- MMD (Maximum Mean Discrepancy): 二標本検定。カーネルを使った分布間距離

---

## 7. スパース学習

### 7.1 LASSO（L1正則化）

$$\hat{\beta} = \arg\min_\beta \frac{1}{2n}\|y - X\beta\|^2 + \lambda\|\beta\|_1$$

**スパース性の幾何学的説明**: L1ペナルティの等高面は菱形 → 最適解が座標軸上（= 一部の係数が厳密に0）に落ちやすい。L2は円 → 軸上に落ちにくい。

**サブ勾配条件**: $\hat{\beta}_j \neq 0 \Leftrightarrow |X_j^T(y-X\hat{\beta})/n| = \lambda$

解法: 座標降下法（Coordinate Descent）が効率的。LARS も使用可能。

### 7.2 圧縮センシング

$s$-スパースな信号 $\beta$ を $m \ll p$ の観測から復元:

$$y = A\beta, \quad \|\beta\|_0 \leq s$$

**RIP条件 (Restricted Isometry Property)**:

$$(1-\delta_s)\|\beta\|^2 \leq \|A\beta\|^2 \leq (1+\delta_s)\|\beta\|^2, \quad \forall s\text{-sparse } \beta$$

$\delta_{2s} < \sqrt{2}-1$ ならば L1最小化で厳密復元が保証される。

ランダム行列（ガウス、ベルヌーイ）は高確率で RIP を満たす: $m = O(s \log(p/s))$

### 7.3 グループLASSO

$$\min_\beta \frac{1}{2n}\|y - X\beta\|^2 + \lambda\sum_{g=1}^{G}\sqrt{p_g}\|\beta_g\|_2$$

- グループ単位でスパース化（グループ内は全て0 or 全て非0）
- 応用: カテゴリ変数（ダミー変数群の一括選択）、多チャンネル信号

### 7.4 弾性ネット

$$\min_\beta \frac{1}{2n}\|y - X\beta\|^2 + \lambda_1\|\beta\|_1 + \lambda_2\|\beta\|_2^2$$

- L1 + L2 の組み合わせ
- LASSO の問題点を解消: (1) $p > n$ で最大 $n$ 個しか選択できない (2) 相関の高い変数からランダムに1つだけ選ぶ → 弾性ネットはグループごと選択
- $\alpha = \lambda_1/(\lambda_1+\lambda_2)$: L1比率。$\alpha=1$ → LASSO、$\alpha=0$ → リッジ

**実務活用**: 遺伝子発現データ、高次元回帰
- $p \gg n$ の高次元データ: LASSO or 弾性ネットが標準
- 安定した変数選択: Stability Selection（ランダムサブサンプリング + LASSO を反復）
- 解のパス: $\lambda$ を変化させた解パスを可視化 → 重要変数の特定

---

## 8. グラフィカルモデル

### 8.1 ベイジアンネットワーク（有向グラフ）

同時分布の分解:

$$p(x_1,...,x_p) = \prod_{i=1}^{p} p(x_i | \text{pa}(x_i))$$

$\text{pa}(x_i)$: ノード $x_i$ の親ノード集合。DAG構造で因果関係を表現。

### 8.2 マルコフ確率場（無向グラフ）

$$p(x) = \frac{1}{Z}\prod_{C \in \mathcal{C}} \psi_C(x_C)$$

$Z$: 分配関数（正規化定数）。$\psi_C$: クリークポテンシャル。

- ハンマーズリー-クリフォードの定理: 正の分布は無向グラフのクリーク分解と条件付き独立性が等価

### 8.3 d分離

有向グラフでの条件付き独立性判定規則:

| パス構造 | $Z$ が観測されていない | $Z$ が観測されている |
|---|---|---|
| 連鎖: $A \to Z \to B$ | 依存 | 独立（ブロック） |
| 分岐: $A \leftarrow Z \to B$ | 依存 | 独立（ブロック） |
| 合流: $A \to Z \leftarrow B$ | 独立 | 依存（開通: explaining away） |

$X$ と $Y$ が $Z$ でd分離 $\Rightarrow$ $X \perp\!\!\!\perp Y | Z$

### 8.4 推論アルゴリズム

**変数消去**: 不要な変数を和（または積分）で周辺化。計算量は消去順序に依存。

**信念伝播 (Belief Propagation)**:
- 木構造: メッセージパッシングで厳密推論（Sum-Product アルゴリズム）
- ループあり: Loopy BP は近似推論（収束保証なし、実用的には有効）

メッセージ更新: $m_{f\to x}(x) = \sum_{\sim x} f(x_1,...,x_k)\prod_{j\neq i} m_{x_j\to f}(x_j)$

### 8.5 構造学習

| 手法 | 原理 | 代表的アルゴリズム |
|---|---|---|
| 制約ベース | 条件付き独立性検定 | PC, FCI |
| スコアベース | モデルスコア最適化 | GES, BIC + 探索 |
| ハイブリッド | 制約+スコア | MMHC |
| 連続最適化 | DAG制約の連続緩和 | NOTEARS |

NOTEARS: DAG条件 $\text{tr}(e^{W \circ W}) - d = 0$ を連続制約として扱い、増大ラグランジュ法で解く。

**実務活用**: 因果探索、確率的推論
- 因果推論: 介入 $do(X=x)$ の効果推定（バックドア基準、フロントドア基準）
- 異常原因分析: ベイジアンネットワークで異常の根本原因を推定
- 医療: 疾患-症状の因果ネットワーク

---

## 9. 半教師あり学習

### 9.1 自己学習（Self-Training）

1. ラベル付きデータで初期モデル学習
2. ラベルなしデータに予測ラベル付与
3. 高信頼度の予測をラベル付きデータに追加
4. 繰り返し

- 確認バイアス（confirmation bias）のリスク: 初期モデルの誤りが増幅
- 対策: 信頼度閾値を徐々に下げる（カリキュラム学習的アプローチ）

### 9.2 ラベル伝播

グラフ上でラベルを伝播:

$$F^{(t+1)} = \alpha S F^{(t)} + (1-\alpha)Y$$

$S = D^{-1/2}WD^{-1/2}$: 正規化類似度行列。$Y$: 初期ラベル行列。$\alpha$: 伝播率。

- 調和関数法: ラベル付きノードを固定、ラベルなしノードの調和平均
- 閉形式解: $F_U = (I - \alpha S_{UU})^{-1}\alpha S_{UL}Y_L$

### 9.3 三つの仮定

| 仮定 | 内容 | 活用する手法 |
|---|---|---|
| 滑らかさ仮定 | 近い点は同じラベル | ラベル伝播、グラフベース |
| 低密度分離仮定 | 決定境界はデータ密度の低い領域を通る | 半教師ありSVM (TSVM)、エントロピー正則化 |
| 多様体仮定 | データは低次元多様体上に存在 | 多様体正則化、Laplacian SVM |

**実務活用**: ラベルが少ない場合のモデリング
- 自然言語処理: 大量の未ラベルテキスト + 少量のラベル付き → 事前学習 (BERT) + ファインチューニング
- 画像: FixMatch（弱い拡張でラベル予測、強い拡張で一貫性学習）
- 能動学習との併用: 最も情報量の多いサンプルにラベルを付与 → コスト効率的

---

## 10. 強化学習の統計的基礎

### 10.1 マルコフ決定過程 (MDP)

5つ組 $(S, A, P, R, \gamma)$:
- $S$: 状態空間
- $A$: 行動空間
- $P(s'|s,a)$: 遷移確率
- $R(s,a)$: 報酬関数
- $\gamma \in [0,1)$: 割引率

マルコフ性: $P(s_{t+1}|s_1,...,s_t,a_1,...,a_t) = P(s_{t+1}|s_t,a_t)$

### 10.2 価値関数

**状態価値関数**: $V^\pi(s) = \mathbb{E}_\pi\left[\sum_{t=0}^{\infty}\gamma^t R(s_t,a_t) | s_0=s\right]$

**行動価値関数**: $Q^\pi(s,a) = \mathbb{E}_\pi\left[\sum_{t=0}^{\infty}\gamma^t R(s_t,a_t) | s_0=s, a_0=a\right]$

最適価値関数: $V^*(s) = \max_\pi V^\pi(s)$, $Q^*(s,a) = \max_\pi Q^\pi(s,a)$

### 10.3 ベルマン方程式

**ベルマン期待方程式**:

$$V^\pi(s) = \sum_a \pi(a|s)\left[R(s,a) + \gamma\sum_{s'} P(s'|s,a)V^\pi(s')\right]$$

**ベルマン最適方程式**:

$$V^*(s) = \max_a\left[R(s,a) + \gamma\sum_{s'} P(s'|s,a)V^*(s')\right]$$

$$Q^*(s,a) = R(s,a) + \gamma\sum_{s'} P(s'|s,a)\max_{a'} Q^*(s',a')$$

- 価値反復: ベルマン最適方程式を反復適用 → $\gamma < 1$ で収束
- 方策反復: 方策評価 + 方策改善を交互実行 → 有限ステップで収束

### 10.4 方策勾配法

方策を $\pi_\theta(a|s)$ でパラメータ化。目的関数:

$$J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta}\left[\sum_{t=0}^{T} \gamma^t R(s_t, a_t)\right]$$

**方策勾配定理**:

$$\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}\left[\nabla_\theta \log\pi_\theta(a|s) \cdot Q^{\pi_\theta}(s,a)\right]$$

- REINFORCE: $Q$ をモンテカルロリターンで推定。分散大
- Actor-Critic: 価値関数 $V_\phi(s)$ を同時学習。$A(s,a) = Q(s,a) - V(s)$（アドバンテージ）で分散低減
- PPO (Proximal Policy Optimization): クリッピングで方策の急激な変化を防止

### 10.5 探索と利用のトレードオフ

**多腕バンディット問題**: $K$ 本の腕、各腕の報酬分布は未知。累積報酬を最大化。

リグレット: $R_T = T\mu^* - \sum_{t=1}^{T}\mu_{a_t}$（最適腕との累積差）

| 手法 | 原理 | リグレット |
|---|---|---|
| $\epsilon$-greedy | 確率 $\epsilon$ でランダム探索 | $O(\epsilon T + K/\epsilon)$ |
| UCB1 | $a_t = \arg\max_a [\hat{\mu}_a + \sqrt{\frac{2\log t}{n_a}}]$ | $O(\sqrt{KT\log T})$ |
| トンプソンサンプリング | 事後分布からサンプルして最大のものを選択 | $O(\sqrt{KT\log T})$ — 実用的に最良 |

**UCB (Upper Confidence Bound)**:

$$a_t = \arg\max_a \left[\hat{\mu}_a + c\sqrt{\frac{\log t}{n_a}}\right]$$

- 楽観的探索: 不確実性の高い腕を積極的に試す
- Hoeffding の不等式に基づく信頼上界

**トンプソンサンプリング**:
1. 各腕の報酬分布の事後を維持（例: ベルヌーイ報酬 → $\text{Beta}(\alpha, \beta)$）
2. 各事後からサンプル $\tilde{\mu}_a \sim p(\mu_a | \text{data})$
3. $a_t = \arg\max_a \tilde{\mu}_a$

- ベイズ最適に漸近。実装が簡潔で実務的に最も強力
- 文脈付きバンディット: 特徴量 $x_t$ に依存 → LinUCB, Neural Thompson Sampling

**実務活用**: バンディット問題、推薦システム、A/Bテストの適応的設計
- A/Bテスト: トンプソンサンプリングで勝者を早期に特定（リグレット最小化）
- 推薦: 文脈付きバンディットでユーザー特徴量に基づくパーソナライズ
- 価格最適化: 需要の不確実性下でUCB方策を適用
- 投資ポートフォリオ: Kelly基準 × バンディット探索で動的配分

---

## 付録: 手法選択ガイド

| データ特性 | 推奨手法 | 理由 |
|---|---|---|
| $n$ 大, $p$ 小, テーブルデータ | GBDT (LightGBM) | 精度・速度・解釈性のバランス |
| $n$ 小, $p$ 大 ($p \gg n$) | LASSO / 弾性ネット / SVM | スパース性・正則化が必須 |
| 画像・音声・テキスト | NN (CNN / Transformer) | 構造的帰納バイアスが有効 |
| ラベルなし・構造探索 | GMM / スペクトラルクラスタリング | 確率モデルまたはグラフベース |
| 因果関係の推定 | グラフィカルモデル + PC/GES | d分離・介入の形式化 |
| ラベル少量 + 大量未ラベル | 半教師あり / 自己学習 | ラベルコスト削減 |
| 逐次的意思決定 | バンディット / RL | 探索-利用トレードオフの形式化 |

## 付録: 数学的基盤の早見表

| 概念 | 使用場面 | 要点 |
|---|---|---|
| 凸最適化 | ロジスティック回帰, SVM, LASSO | 大域最適が保証される |
| ラグランジュ双対 | SVM双対, カーネル法 | KKT条件でスパース解 |
| 固有値分解 | PCA, スペクトラルクラスタリング | 共分散/ラプラシアンの構造抽出 |
| 情報理論 | 決定木, VAE, 変分推論 | KLダイバージェンス, 相互情報量 |
| 測度論 | 確率的収束, 汎化理論 | 確率不等式（Hoeffding, McDiarmid） |
| 関数解析 | カーネル法, RKHS | 再生性, 表現定理 |
