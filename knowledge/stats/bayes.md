# ベイズ統計 — 統計リファレンス

> 統計検定1級満点レベル。各セクション末尾に実務活用を付記。

---

## 1. ベイズの基本原理

### 1.1 ベイズの定理

$$P(\theta | x) = \frac{P(x | \theta) \, P(\theta)}{P(x)}$$

- **事前分布** $P(\theta)$: データ観測前のパラメータに関する信念
- **尤度** $P(x | \theta)$: パラメータが与えられたときのデータの生成確率
- **事後分布** $P(\theta | x)$: データ観測後のパラメータに関する更新された信念
- **周辺尤度** $P(x) = \int P(x|\theta)P(\theta)d\theta$: 正規化定数（エビデンス）

比例形式（正規化定数を省略）:

$$P(\theta | x) \propto P(x | \theta) \, P(\theta)$$

### 1.2 逐次更新（Sequential Update）

事後分布が次のデータに対する事前分布となる:

$$P(\theta | x_1, x_2) \propto P(x_2 | \theta) \cdot \underbrace{P(\theta | x_1)}_{\text{前回の事後}}$$

データ $x_1, \ldots, x_n$ を1つずつ逐次的に処理しても、一括で処理しても同じ事後分布に到達する。
これはベイズ更新のコヒーレンス（一貫性）と呼ばれる。

### 1.3 頻度論との哲学的違い

| 観点 | 頻度論 | ベイズ論 |
|------|--------|----------|
| 確率の解釈 | 長期的な相対頻度 | 信念の度合い（主観確率） |
| パラメータ | 固定された未知定数 | 確率変数（分布を持つ） |
| 推定結果 | 点推定＋信頼区間 | 事後分布全体 |
| 繰り返しの概念 | 仮想的な反復実験 | 不要 |
| 事前情報 | 使わない | 事前分布として組み込む |
| 停止規則 | 検定結果に影響 | 尤度原理により影響しない |

**尤度原理**: 観測データが同じ尤度関数を与えるなら、推論結果は同じであるべき。
ベイズ推論は尤度原理を自然に満たす。頻度論の p 値は停止規則に依存するため満たさない。

### 1.4 実務活用

- **オンライン学習**: データが逐次到着する環境で事後分布を逐次更新（リアルタイム推薦、異常検知）
- **A/Bテストの逐次分析**: 頻度論ではサンプルサイズ固定が必要だが、ベイズでは途中覗きが理論的に許される
- **不確実性の定量化**: 事後分布全体を保持することで意思決定のリスク評価が可能
- **boatrace実装例**: 各モデルの的中率をベータ分布で逐次更新し、精算ごとに信念を更新

---

## 2. 共役事前分布

### 2.1 共役族の定義

尤度関数 $P(x|\theta)$ に対して、事前分布 $P(\theta)$ が共役であるとは、
事後分布 $P(\theta|x)$ が事前分布と同じ分布族に属することをいう。

**利点**:
- 事後分布が解析的に計算可能（MCMCが不要）
- ハイパーパラメータの更新規則が明示的
- 計算コストが極めて低い

### 2.2 主要な共役ペア一覧

| 尤度 | 事前分布 | 事後分布 | 更新規則 |
|------|----------|----------|----------|
| $\text{Bernoulli}(p)$ | $\text{Beta}(\alpha, \beta)$ | $\text{Beta}(\alpha+s, \beta+n-s)$ | $s$=成功数, $n$=試行数 |
| $\text{Binomial}(n, p)$ | $\text{Beta}(\alpha, \beta)$ | $\text{Beta}(\alpha+x, \beta+n-x)$ | $x$=成功数 |
| $\text{Poisson}(\lambda)$ | $\text{Gamma}(a, b)$ | $\text{Gamma}(a+\sum x_i, b+n)$ | $n$=観測数 |
| $\text{Normal}(\mu, \sigma^2_{\text{known}})$ | $\text{Normal}(\mu_0, \tau^2_0)$ | $\text{Normal}(\mu_n, \tau^2_n)$ | 下記参照 |
| $\text{Normal}(\mu_{\text{known}}, \sigma^2)$ | $\text{InvGamma}(a, b)$ | $\text{InvGamma}(a', b')$ | 下記参照 |
| $\text{Multinomial}(n, \mathbf{p})$ | $\text{Dirichlet}(\boldsymbol{\alpha})$ | $\text{Dirichlet}(\boldsymbol{\alpha}+\mathbf{x})$ | $\mathbf{x}$=カウントベクトル |
| $\text{Exponential}(\lambda)$ | $\text{Gamma}(a, b)$ | $\text{Gamma}(a+n, b+\sum x_i)$ | |
| $\text{Geometric}(p)$ | $\text{Beta}(\alpha, \beta)$ | $\text{Beta}(\alpha+n, \beta+\sum x_i)$ | |

### 2.3 正規モデルの共役更新（詳細）

尤度: $x_1, \ldots, x_n \sim \text{Normal}(\mu, \sigma^2)$（$\sigma^2$ 既知）

事前: $\mu \sim \text{Normal}(\mu_0, \tau_0^2)$

事後:
$$\mu_n = \frac{\frac{1}{\tau_0^2}\mu_0 + \frac{n}{\sigma^2}\bar{x}}{\frac{1}{\tau_0^2} + \frac{n}{\sigma^2}}, \qquad \frac{1}{\tau_n^2} = \frac{1}{\tau_0^2} + \frac{n}{\sigma^2}$$

精度（precision = 分散の逆数）の加法性: 事後精度 = 事前精度 + データ精度

事後平均は事前平均とデータ平均の精度重み付き平均になる。

### 2.4 ハイパーパラメータの解釈

ハイパーパラメータは「仮想サンプルサイズ」として解釈できる:

- $\text{Beta}(\alpha, \beta)$: $\alpha + \beta$ 回の仮想試行（$\alpha$ 回成功、$\beta$ 回失敗）
- $\text{Gamma}(a, b)$: $a$ 個の仮想観測で合計 $b$ を観測
- $\text{Dirichlet}(\alpha_1, \ldots, \alpha_K)$: $\sum \alpha_k$ 個の仮想観測

仮想サンプルサイズが大きいほど事前分布の影響が強い（情報量の多い事前分布）。

### 2.5 実務活用

- **ベータ・二項モデル**: CTR推定、的中率推定に頻用。$\text{Beta}(1,1)$（一様）から開始し逐次更新
- **ポアソン・ガンマモデル**: イベント発生率（障害件数/日、BET回数/日）の推定
- **ディリクレ・多項モデル**: カテゴリ分布の推定（券種別BET比率、艇番別勝率分布）
- **オンラインバンディット**: Thompson Samplingでベータ事後からサンプリングして腕を選択

---

## 3. 無情報事前分布・弱情報事前分布

### 3.1 ジェフリーズ事前分布

フィッシャー情報量 $I(\theta)$ に基づく:

$$\pi_J(\theta) \propto |I(\theta)|^{1/2}$$

**特性**: パラメータ変換に対して不変（$\phi = g(\theta)$ としても整合的な事前が得られる）

主要な例:
- $\text{Bernoulli}(p)$: $\pi_J(p) \propto p^{-1/2}(1-p)^{-1/2} = \text{Beta}(1/2, 1/2)$
- $\text{Normal}(\mu, \sigma^2_{\text{known}})$: $\pi_J(\mu) \propto 1$（一様分布）
- $\text{Normal}(\mu_{\text{known}}, \sigma^2)$: $\pi_J(\sigma^2) \propto 1/\sigma^2$
- $\text{Poisson}(\lambda)$: $\pi_J(\lambda) \propto \lambda^{-1/2}$

### 3.2 一様事前分布の問題点

- パラメータ空間が非有界の場合、非正則事前分布（improper prior）になる
- パラメータ変換に対して不変でない（$p$ に対して一様でも $\log p$ には一様でない）
- 事後分布が正則（proper）にならない場合がある（特に多次元で危険）
- ジェフリーズ事前は多次元で過度に無情報になりうる → 参照事前分布で対処

### 3.3 参照事前分布（Reference Prior）

Bernardo (1979) の参照事前分布:
- 事後分布と事前分布のKLダイバージェンスを最大化
- ジェフリーズ事前の多次元拡張として有用
- パラメータに重要度の順序をつけて逐次的に構成

### 3.4 弱情報事前分布（Weakly Informative Prior）

完全に無情報ではなく、物理的に妥当な範囲に緩やかに制約する:

| 対象 | 推奨事前 | 根拠 |
|------|----------|------|
| 分散パラメータ $\sigma$ | $\text{Half-Cauchy}(0, s)$ | Gelman (2006)。裾が重く大きな値も許容 |
| 回帰係数 $\beta$ | $\text{Normal}(0, s^2)$（$s$は大きめ） | 正則化効果あり |
| 相関行列 | LKJ分布 $\text{LKJ}(\eta)$ | $\eta=1$ で一様、$\eta>1$ で単位行列寄り |
| 分散共分散行列 | $\text{InvWishart}(\nu, \Sigma_0)$ | $\nu$=次元数+1 で弱情報 |
| カウントデータの率 | $\text{Gamma}(0.01, 0.01)$ | 広い範囲をカバー |

### 3.5 実務活用

- **情報が乏しい初期段階**: ジェフリーズまたは弱情報事前で開始し、データ蓄積で事後が支配
- **Stan/PyMCでの推奨**: Half-Cauchy(0, 2.5)を標準偏差の事前に使うのが定番
- **正則化としての事前**: 過学習防止のため弱い事前分布を意図的に入れる

---

## 4. ベイズ推定

### 4.1 点推定と損失関数

| 損失関数 | 最適推定量 | 数式 |
|----------|------------|------|
| 二乗誤差 $L = (\hat\theta - \theta)^2$ | 事後平均 | $\hat\theta = E[\theta|x]$ |
| 絶対誤差 $L = |\hat\theta - \theta|$ | 事後中央値 | $\hat\theta = \text{Med}[\theta|x]$ |
| 0-1損失 | 事後最頻値(MAP) | $\hat\theta = \arg\max P(\theta|x)$ |
| 非対称二次損失 $L = w(\theta)(\hat\theta - \theta)^2$ | 重み付き事後平均 | |
| LINEX損失 $L = e^{a(\hat\theta-\theta)} - a(\hat\theta-\theta) - 1$ | $-\frac{1}{a}\log E[e^{-a\theta}|x]$ | 非対称リスク用 |

### 4.2 MAP推定（Maximum A Posteriori）

$$\hat\theta_{\text{MAP}} = \arg\max_\theta P(\theta | x) = \arg\max_\theta \left[\log P(x|\theta) + \log P(\theta)\right]$$

- 尤度最大化（MLE）に事前分布のペナルティ項を加えた最適化
- 正規事前 → L2正則化（リッジ回帰）、ラプラス事前 → L1正則化（LASSO）
- 高次元では事後分布の最頻値が典型的な値から乖離しうる（concentration of measure）

### 4.3 信用区間（Credible Interval）

**等裾信用区間（Equal-Tailed Interval, ETI）**:
$$P(\theta < a | x) = P(\theta > b | x) = \alpha/2$$

**最高事後密度区間（HPD: Highest Posterior Density）**:
$$C = \{\theta : P(\theta|x) \geq c^*\}, \quad P(\theta \in C | x) = 1-\alpha$$

HPDの特性:
- 最短の信用区間
- 区間内のどの点も区間外のどの点より事後密度が高い
- 非対称分布（ガンマ、ベータ等）では ETI と異なる
- 多峰の場合は非連結な区間になりうる

**頻度論の信頼区間との違い**: 信用区間は「パラメータがこの区間に入る確率が95%」と直接解釈できる。

### 4.4 予測分布（Posterior Predictive Distribution）

新規データ $\tilde{x}$ の予測分布:

$$p(\tilde{x} | x) = \int p(\tilde{x} | \theta) \, p(\theta | x) \, d\theta$$

パラメータの不確実性を積分消去（marginalize out）することで、予測の不確実性を正しく反映。

例: 正規モデルで $\mu, \sigma^2$ 共に未知の場合、予測分布は $t$ 分布になる（正規分布より裾が重い）。

### 4.5 実務活用

- **意思決定**: 損失関数を明示し、最適行動をベイズ決定理論で導出
- **区間推定**: HPD区間でパラメータの不確実性を報告（論文・レポート向け）
- **予測**: 予測分布により「次の観測がどの範囲に来るか」を確率的に予測
- **リスク管理**: LINEX損失で過大評価と過小評価の非対称コストをモデル化

---

## 5. ベイズ検定・モデル選択

### 5.1 ベイズファクター

2つのモデル $M_1, M_2$ の比較:

$$BF_{12} = \frac{P(x | M_1)}{P(x | M_2)} = \frac{\int P(x|\theta_1, M_1)P(\theta_1|M_1)d\theta_1}{\int P(x|\theta_2, M_2)P(\theta_2|M_2)d\theta_2}$$

事後オッズ = ベイズファクター × 事前オッズ:
$$\frac{P(M_1|x)}{P(M_2|x)} = BF_{12} \cdot \frac{P(M_1)}{P(M_2)}$$

解釈の目安（Kass & Raftery 1995）:

| $\log_{10} BF_{12}$ | $BF_{12}$ | 証拠の強さ |
|----------------------|-----------|------------|
| 0 - 0.5 | 1 - 3.2 | 無視できる |
| 0.5 - 1 | 3.2 - 10 | 実質的 |
| 1 - 2 | 10 - 100 | 強い |
| > 2 | > 100 | 決定的 |

### 5.2 周辺尤度（エビデンス）の計算

$$P(x|M) = \int P(x|\theta, M) P(\theta|M) d\theta$$

計算方法:
- **解析的**: 共役モデルでのみ可能
- **ラプラス近似**: $\log P(x|M) \approx \log P(x|\hat\theta) + \log P(\hat\theta) + \frac{d}{2}\log(2\pi) - \frac{1}{2}\log|H|$
- **調和平均推定量**: $1/P(x|M) \approx \frac{1}{T}\sum_{t=1}^T 1/P(x|\theta^{(t)})$（不安定、非推奨）
- **ブリッジサンプリング**: 安定かつ効率的、bridge_sampler パッケージ
- **逐次モンテカルロ (SMC)**: 粒子フィルタベース

### 5.3 リンドレーのパラドックス

サンプルサイズ $n \to \infty$ のとき:
- 頻度論の検定: $H_0$ を棄却（p < 0.05）
- ベイズファクター: $H_0$ を支持（BF → ∞ in favor of $H_0$）

原因: 帰無仮説が点仮説（$\theta = \theta_0$）の場合、事前分布が拡散するほど
周辺尤度が小さくなる（事前質量の希薄化）。

対策: 事前分布の幅を慎重に選ぶ。JZS事前（Jeffreys-Zellner-Siow）が推奨される。

### 5.4 情報量規準

**DIC（Deviance Information Criterion）**:
$$DIC = \overline{D(\theta)} + p_D, \quad p_D = \overline{D(\theta)} - D(\bar\theta)$$
- $p_D$: 有効パラメータ数
- MCMCの出力から容易に計算可能
- 非正規事後や混合モデルで $p_D < 0$ になる問題あり

**WAIC（Widely Applicable Information Criterion）**:
$$WAIC = -2 \sum_{i=1}^n \log \hat{p}(x_i) + 2 p_W$$
- $\hat{p}(x_i) = \frac{1}{S}\sum_s p(x_i|\theta^{(s)})$: 点ごとの対数予測密度
- $p_W$: 有効パラメータ数（事後分散ベース）
- DICより理論的に優れ、特異モデルにも適用可能

**LOO-CV（Leave-One-Out Cross-Validation）**:
$$\text{elpd}_{\text{loo}} = \sum_{i=1}^n \log p(x_i | x_{-i})$$
- Pareto Smoothed Importance Sampling (PSIS) で効率的に近似
- `loo` パッケージ（R）、`arviz` パッケージ（Python）で利用可能
- Pareto $\hat{k}$ 診断値で近似の信頼性を評価（$\hat{k} > 0.7$ は要注意）

### 5.5 ベイズモデル平均化（BMA）

$$P(\tilde{x}|x) = \sum_{k=1}^K P(\tilde{x}|x, M_k) \cdot P(M_k|x)$$

各モデルの予測を事後モデル確率で重み付け平均。
モデル選択の不確実性を予測に反映できる。

### 5.6 実務活用

- **モデル比較**: WAIC/LOO-CVが現在の標準。DICは非推奨になりつつある
- **変数選択**: ベイズファクターで変数の包含/除外を評価
- **アンサンブル**: BMAで複数モデルの予測を統合（気象予測、金融リスク）
- **boatrace実装例**: 3モデル（GPT/Gemini/Opus）の予測をBMAで統合する構想

---

## 6. MCMC（マルコフ連鎖モンテカルロ法）

### 6.1 メトロポリス・ヘイスティングス (MH)

**アルゴリズム**:
1. 初期値 $\theta^{(0)}$ を設定
2. 提案分布 $q(\theta^*|\theta^{(t)})$ から候補 $\theta^*$ を生成
3. 受容確率を計算: $\alpha = \min\left(1, \frac{P(\theta^*|x) \, q(\theta^{(t)}|\theta^*)}{P(\theta^{(t)}|x) \, q(\theta^*|\theta^{(t)})}\right)$
4. 確率 $\alpha$ で $\theta^{(t+1)} = \theta^*$、さもなくば $\theta^{(t+1)} = \theta^{(t)}$
5. 2-4 を繰り返す

**ランダムウォーク MH**: $q(\theta^*|\theta^{(t)}) = \text{Normal}(\theta^{(t)}, \sigma^2_{\text{prop}})$
- $\sigma_{\text{prop}}$ が大きすぎると受容率が低い、小さすぎると混合が遅い
- 最適受容率: 1次元で約0.44、高次元で約0.234（Roberts et al. 1997）

**独立 MH**: $q(\theta^*|\theta^{(t)}) = q(\theta^*)$（現在値に依存しない）
- 提案分布が事後分布を良く近似する場合に有効
- 裾が事後より軽いと受容率が極端に低下するため、裾の重い提案が望ましい

### 6.2 ギブスサンプリング

パラメータベクトル $\theta = (\theta_1, \ldots, \theta_p)$ を成分ごとに更新:

1. $\theta_1^{(t+1)} \sim P(\theta_1 | \theta_2^{(t)}, \ldots, \theta_p^{(t)}, x)$
2. $\theta_2^{(t+1)} \sim P(\theta_2 | \theta_1^{(t+1)}, \theta_3^{(t)}, \ldots, \theta_p^{(t)}, x)$
3. ...
4. $\theta_p^{(t+1)} \sim P(\theta_p | \theta_1^{(t+1)}, \ldots, \theta_{p-1}^{(t+1)}, x)$

**特性**:
- 受容確率は常に1（棄却なし）
- 完全条件付き分布が標準分布なら効率的
- 強い相関がある場合は混合が遅い（ブロック化ギブスで対処）

**データ拡大**: 潜在変数 $z$ を導入して $P(\theta, z | x)$ からギブスサンプリング
- 例: 混合正規分布のEMアルゴリズムのベイズ版

### 6.3 ハミルトニアンモンテカルロ (HMC)

物理系のハミルトン力学を利用した効率的サンプリング:

- **位置** $q = \theta$（パラメータ）
- **運動量** $p \sim \text{Normal}(0, M)$（補助変数）
- **ハミルトニアン** $H(q, p) = -\log P(q|x) + \frac{1}{2}p^T M^{-1} p$

**リープフロッグ積分**:
1. $p \leftarrow p - \frac{\epsilon}{2} \nabla_q U(q)$ （半ステップ運動量更新）
2. $q \leftarrow q + \epsilon M^{-1} p$ （位置更新）
3. $p \leftarrow p - \frac{\epsilon}{2} \nabla_q U(q)$ （半ステップ運動量更新）
4. $L$ 回繰り返す

$U(q) = -\log P(q|x)$（ポテンシャルエネルギー）

MH受容確率: $\alpha = \min(1, \exp(H(q^{(t)}, p^{(t)}) - H(q^*, p^*)))$

**利点**: ランダムウォークを避け、事後分布の等高線に沿って移動。高次元でも効率的。

### 6.4 NUTS（No-U-Turn Sampler）

HMCのステップ数 $L$ とステップサイズ $\epsilon$ を自動調整:
- 軌道が「折り返す」（U-turn）ポイントを検出して停止
- ツリーを再帰的に倍増して最適な軌道長を決定
- Stan の標準サンプラー。チューニングパラメータの手動設定が不要

### 6.5 収束診断

**ゲルマン・ルービンの $\hat{R}$**:
- 複数チェーンの鎖間分散と鎖内分散の比
- $\hat{R} < 1.01$ が収束の目安（旧基準1.1は緩すぎる）
- 改良版 rank-normalized $\hat{R}$（Vehtari et al. 2021）を推奨

**実効サンプルサイズ (ESS)**:
$$ESS = \frac{n}{1 + 2\sum_{k=1}^K \rho_k}$$
- $\rho_k$: ラグ $k$ の自己相関
- Bulk-ESS（分布の中心）と Tail-ESS（裾）を分けて評価
- ESS > 400 が目安（Stan推奨）

**バーンイン（ウォームアップ）**: 初期の非定常部分を除去。全サンプルの25-50%。

**シンニング（間引き）**: 自己相関を減らすために $k$ 個おきに抽出。
現代の実装ではESS が十分なら不要（メモリ制約がある場合のみ）。

**トレースプロット**: チェーンの時系列を目視確認。「毛虫状」なら良好。

### 6.6 実務活用

- **小規模モデル**: 共役モデルが使えない場合でもMCMCで事後分布を数値的に取得
- **Stanの活用**: `rstan`（R）、`cmdstanpy`（Python）でNUTSを利用
- **PyMCの活用**: PyMC v5 でNUTSが標準。変分推論との切り替えも容易
- **診断必須**: $\hat{R}$、ESS、divergent transitionsを必ず確認。divergentがあればモデル再パラメータ化

---

## 7. 階層ベイズモデル

### 7.1 基本構造

$$x_{ij} | \theta_i \sim P(x | \theta_i) \quad \text{(データレベル)}$$
$$\theta_i | \phi \sim P(\theta | \phi) \quad \text{(グループレベル)}$$
$$\phi \sim P(\phi) \quad \text{(ハイパーレベル)}$$

- $i = 1, \ldots, J$: グループ（学校、病院、モデル等）
- $j = 1, \ldots, n_i$: グループ内の観測

### 7.2 収縮推定（Shrinkage / Partial Pooling）

3つのプーリング戦略:

| 戦略 | 推定方法 | 問題 |
|------|----------|------|
| Complete pooling | 全データで1つの $\theta$ | グループ差を無視 |
| No pooling | グループ別に独立推定 | 小サンプルで不安定 |
| **Partial pooling** | 階層モデル | 全体平均に向かって収縮 |

収縮の度合い:
$$\hat\theta_i^{\text{Bayes}} \approx (1 - B_i) \bar{x}_i + B_i \, \mu$$

$$B_i = \frac{\sigma^2 / n_i}{\sigma^2 / n_i + \tau^2}$$

- $B_i$: 収縮係数（0に近いほど個別推定、1に近いほど全体平均）
- サンプルサイズ $n_i$ が小さいグループほど全体平均に引き寄せられる
- James-Stein 推定量との関連

### 7.3 ランダム効果モデルとの関係

線形混合モデル: $y_{ij} = \beta_0 + u_i + \epsilon_{ij}$, $u_i \sim N(0, \tau^2)$

ベイズ的解釈: $u_i$ はランダム効果 = グループレベルのパラメータ。
$\tau^2$ は $u_i$ の分散 = ハイパーパラメータ。
頻度論のREMLとベイズ的推定は $\tau^2$ の扱いで異なる。

### 7.4 実務活用

- **メタ分析**: 複数研究の効果サイズを統合（研究間異質性 $\tau^2$ を推定）
- **小地域推定**: 市区町村別の疾病率を、全国データで安定化（疫学）
- **推薦システム**: ユーザー×アイテムの評価を階層ベイズで推定（協調フィルタリング）
- **スポーツ分析**: チーム/選手のパフォーマンスを階層的にモデル化
- **boatrace実装例**: 会場別×モデル別の的中率を階層ベイズで推定（少BETの会場は全体に収縮）

---

## 8. ベイズ的正則化

### 8.1 事前分布と正則化の対応

MAP推定の最適化問題:

$$\hat\beta_{\text{MAP}} = \arg\min_\beta \left[-\sum_i \log P(y_i|x_i, \beta) - \log P(\beta)\right]$$

| 事前分布 | 正則化 | ペナルティ項 |
|----------|--------|-------------|
| $\beta_j \sim N(0, \sigma^2_\beta)$ | リッジ (L2) | $\lambda \sum \beta_j^2$ |
| $\beta_j \sim \text{Laplace}(0, b)$ | LASSO (L1) | $\lambda \sum |\beta_j|$ |
| $\beta_j \sim \text{Cauchy}(0, s)$ | — | 裾が重い正則化 |
| Horseshoe | — | スパースかつ大きなシグナルを保持 |

$\lambda = \sigma^2/(2\sigma^2_\beta)$ の関係でベイズと頻度論の正則化が対応。

### 8.2 Horseshoe Prior

$$\beta_j | \lambda_j, \tau \sim N(0, \lambda_j^2 \tau^2)$$
$$\lambda_j \sim \text{Half-Cauchy}(0, 1)$$
$$\tau \sim \text{Half-Cauchy}(0, \tau_0)$$

- $\lambda_j$: 局所収縮パラメータ（変数ごと）
- $\tau$: 全体収縮パラメータ
- ゼロ近傍に強い質量を持ちながら、裾が重いため大きなシグナルを潰さない
- $\tau_0 \approx p_0/(p - p_0) \cdot \sigma/\sqrt{n}$（$p_0$: 期待される非ゼロ係数の数）

### 8.3 スパイク＆スラブ事前

$$\beta_j | \gamma_j \sim \gamma_j \cdot N(0, \sigma^2_{\text{slab}}) + (1-\gamma_j) \cdot \delta_0$$
$$\gamma_j \sim \text{Bernoulli}(\pi)$$

- $\gamma_j = 0$: 変数 $j$ は除外（スパイク = 点質量）
- $\gamma_j = 1$: 変数 $j$ は包含（スラブ = 広い分布）
- 変数選択の事後確率 $P(\gamma_j = 1 | x)$ を直接計算可能
- 計算コストが高い（$2^p$ のモデル空間）→ SSVS (Stochastic Search Variable Selection) で対処

### 8.4 実務活用

- **高次元回帰**: $p \gg n$ の状況（ゲノム、テキスト特徴量）でHorseshoeが有効
- **変数重要度**: スパイク＆スラブで包含確率を算出し、重要変数をランキング
- **正則化強度の自動決定**: ベイズでは $\lambda$ がハイパーパラメータとして自動推定（CVが不要）

---

## 9. 変分推論（Variational Inference）

### 9.1 基本概念

事後分布 $p(\theta|x)$ を近似分布 $q(\theta)$ で近似する最適化問題:

$$q^*(\theta) = \arg\min_{q \in \mathcal{Q}} \text{KL}(q(\theta) \| p(\theta|x))$$

直接最小化は $p(\theta|x)$ の正規化定数が不明なため困難 → ELBO を最大化。

### 9.2 ELBO（Evidence Lower BOund）

$$\log p(x) = \text{ELBO}(q) + \text{KL}(q \| p(\theta|x))$$

$$\text{ELBO}(q) = E_q[\log p(x, \theta)] - E_q[\log q(\theta)]$$
$$= E_q[\log p(x|\theta)] - \text{KL}(q(\theta) \| p(\theta))$$

$\text{KL} \geq 0$ より $\text{ELBO} \leq \log p(x)$（対数エビデンスの下界）。
ELBOを最大化することで $q$ を $p(\theta|x)$ に近づける。

### 9.3 平均場近似（Mean-Field Approximation）

近似分布族を独立成分の積に制限:

$$q(\theta) = \prod_{j=1}^p q_j(\theta_j)$$

各 $q_j$ の最適解:
$$\log q_j^*(\theta_j) = E_{-j}[\log p(x, \theta)] + \text{const}$$

$E_{-j}$: $\theta_j$ 以外の成分に関する $q$ での期待値。

**限界**: パラメータ間の事後相関を捉えられない。多峰事後を近似できない。

### 9.4 確率的変分推論（SVI: Stochastic Variational Inference）

大規模データ向け:
1. ミニバッチ $x_B$ をサンプリング
2. ELBOの勾配をミニバッチで推定: $\nabla_\phi \text{ELBO} \approx \frac{n}{|B|}\sum_{i \in B} \nabla_\phi \log p(x_i|\theta)$
3. 自然勾配法で更新（共役モデルでは特に効率的）

**再パラメータ化トリック（Reparameterization Trick）**:
$q_\phi(\theta) = \text{Normal}(\mu, \sigma^2)$ のとき $\theta = \mu + \sigma \epsilon$, $\epsilon \sim N(0,1)$
として勾配を $\epsilon$ の期待値に変換 → 分散の小さい勾配推定が可能。

### 9.5 MCMCとの比較

| 観点 | MCMC | 変分推論 |
|------|------|----------|
| 精度 | 漸近的に正確 | 近似（平均場ではバイアスあり） |
| 計算速度 | 遅い（数時間〜数日） | 速い（数分〜数時間） |
| スケーラビリティ | $n > 10^5$ で困難 | SGDベースで大規模対応 |
| 収束診断 | $\hat{R}$, ESS等が整備 | ELBOの収束のみ（不十分な場合あり） |
| 不確実性 | 正確な事後分布 | 過小評価されがち |
| 多峰分布 | エルゴード性で全モード探索 | 1つのモードに収束しがち |

### 9.6 実務活用

- **大規模ベイズ**: 100万件以上のデータには変分推論が現実的な選択
- **ベイズニューラルネットワーク**: Bayes by Backprop、Variational Dropout
- **トピックモデル**: LDA（潜在ディリクレ配分）の標準推論手法
- **VAE（変分オートエンコーダ）**: 深層生成モデルの基盤技術
- **探索的分析**: まず変分推論で概観 → 関心のあるサブモデルでMCMC精密推定

---

## 10. ノンパラメトリックベイズ

### 10.1 ディリクレ過程（Dirichlet Process: DP）

$$G \sim \text{DP}(\alpha, G_0)$$

- $G$: ランダム確率測度
- $\alpha > 0$: 集中パラメータ（大きいほど $G_0$ に近い）
- $G_0$: 基底測度（事前の「形」）

DPからの実現値は離散分布（確率1で離散）。

**性質**: 任意の可測分割 $A_1, \ldots, A_K$ に対して
$$(G(A_1), \ldots, G(A_K)) \sim \text{Dirichlet}(\alpha G_0(A_1), \ldots, \alpha G_0(A_K))$$

### 10.2 中華レストラン過程（CRP: Chinese Restaurant Process）

$n$ 番目の客がテーブル $k$ に座る確率:

$$P(\text{テーブル } k) = \frac{n_k}{\alpha + n - 1}, \quad P(\text{新しいテーブル}) = \frac{\alpha}{\alpha + n - 1}$$

- $n_k$: テーブル $k$ の既存客数
- 「富める者がさらに富む」（preferential attachment）
- テーブル数の期待値: $E[K] \approx \alpha \log(n/\alpha)$（対数的に増加）

### 10.3 スティック・ブレイキング構成

$$G = \sum_{k=1}^\infty \pi_k \delta_{\theta_k}, \quad \theta_k \sim G_0$$

$$V_k \sim \text{Beta}(1, \alpha), \quad \pi_k = V_k \prod_{l=1}^{k-1}(1-V_l)$$

棒を順に折っていくイメージ:
- $\pi_1 = V_1$
- $\pi_2 = (1-V_1)V_2$
- $\pi_3 = (1-V_1)(1-V_2)V_3$
- ...

$\sum_{k=1}^\infty \pi_k = 1$（確率1で）。
実装では有限の $K$ で打ち切り（truncated stick-breaking）。

### 10.4 DP混合モデル（DPMM）

$$x_i | z_i, \theta \sim F(\theta_{z_i}), \quad z_i | \pi \sim \text{Cat}(\pi), \quad \pi \sim \text{GEM}(\alpha), \quad \theta_k \sim G_0$$

- クラスタ数を事前に指定する必要がない（データから自動決定）
- $\alpha$ が大きいとクラスタ数が増える、小さいと少ない
- 推論: ギブスサンプリング（Neal Algorithm 3/8）、変分推論（truncated DP）

**ガウス混合の場合**:
$$x_i | z_i \sim N(\mu_{z_i}, \Sigma_{z_i}), \quad (\mu_k, \Sigma_k) \sim \text{NIW}(\mu_0, \kappa_0, \nu_0, \Lambda_0)$$

### 10.5 ガウス過程（GP: Gaussian Process）

関数空間上の事前分布:

$$f \sim \text{GP}(m(x), k(x, x'))$$

- $m(x)$: 平均関数（通常 $m(x) = 0$）
- $k(x, x')$: カーネル関数（共分散関数）

任意の有限点 $(x_1, \ldots, x_n)$ での値が多変量正規分布に従う:
$$(f(x_1), \ldots, f(x_n)) \sim N(\mathbf{m}, K)$$

**主要カーネル**:

| カーネル | 数式 | 特性 |
|----------|------|------|
| RBF (SE) | $k(x,x') = \sigma^2 \exp(-\|x-x'\|^2/(2l^2))$ | 滑らか、無限微分可能 |
| Matern-5/2 | $\sigma^2(1+\frac{\sqrt{5}r}{l}+\frac{5r^2}{3l^2})\exp(-\frac{\sqrt{5}r}{l})$ | 2回微分可能 |
| Matern-3/2 | $\sigma^2(1+\frac{\sqrt{3}r}{l})\exp(-\frac{\sqrt{3}r}{l})$ | 1回微分可能 |
| 周期 | $\sigma^2 \exp(-\frac{2\sin^2(\pi|x-x'|/p)}{l^2})$ | 周期的パターン |
| 線形 | $\sigma^2_b + \sigma^2_v(x-c)(x'-c)$ | 線形回帰のベイズ版 |

**事後過程（回帰）**:
$$f_* | x_*, X, y \sim N(\bar{f}_*, \text{cov}(f_*))$$
$$\bar{f}_* = K(x_*, X)[K(X,X) + \sigma^2_n I]^{-1}y$$
$$\text{cov}(f_*) = K(x_*, x_*) - K(x_*, X)[K(X,X) + \sigma^2_n I]^{-1}K(X, x_*)$$

計算量: $O(n^3)$（逆行列計算）→ スパースGP、インデューシングポイントで近似

### 10.6 その他のノンパラメトリックベイズモデル

- **ピットマン・ヨル過程（PYP）**: DPの一般化。パラメータ $(\alpha, d)$。ベキ則的なクラスタサイズ
- **インディアンビュッフェ過程（IBP）**: 二値特徴行列の事前。各データ点が複数の特徴を持つ
- **階層DP (HDP)**: グループ間でクラスタを共有。トピックモデル（HDP-LDA）に利用
- **ベータ過程**: IBPの連続版。辞書学習に利用

### 10.7 実務活用

- **クラスタリング**: DPMM でクラスタ数を自動推定（顧客セグメンテーション、異常検知）
- **回帰・補間**: ガウス過程で不確実性付きの関数推定（ベイズ最適化の代理モデル）
- **ベイズ最適化**: GP + 獲得関数（EI, UCB）でブラックボックス最適化（ハイパーパラメータチューニング）
- **時系列**: GP + 周期カーネル + トレンドカーネルの加法モデル（Facebook Prophet の理論基盤）
- **自然言語処理**: HDP-LDAでトピック数を自動決定

---

## 付録A: ベイズ計算の実装ガイド

### ツール選択フローチャート

```
共役モデルが使える？
  ├─ Yes → 解析解（最速・最正確）
  └─ No → データサイズは？
       ├─ n < 10^5 → MCMC（Stan/PyMC）
       │     ├─ 連続パラメータ → NUTS
       │     └─ 離散パラメータ → ギブス
       └─ n > 10^5 → 変分推論（SVI/ADVI）
             └─ 精度が必要 → サブサンプルMCMC
```

### 主要ライブラリ

| ライブラリ | 言語 | 推論手法 | 特徴 |
|------------|------|----------|------|
| Stan | R/Python/Julia | NUTS, VI | 最も信頼性が高い。診断が充実 |
| PyMC | Python | NUTS, ADVI, SMC | Pythonエコシステムと統合 |
| NumPyro | Python (JAX) | NUTS, SVI | GPU対応、高速 |
| Turing.jl | Julia | HMC, NUTS, VI | Julia生態系 |
| JAGS | R | ギブス | 教育向け、レガシー |
| Edward2/TFP | Python (TF) | VI, HMC | 深層学習統合 |
| brms | R | Stan backend | lme4風の記法でStan |

### 実務上の注意事項

1. **事前分布感度分析**: 異なる事前で結果が大きく変わらないか確認
2. **事後予測チェック**: 事後分布からデータを生成し、実データと比較
3. **計算再現性**: シード固定、チェーン数・イテレーション数を記録
4. **報告**: 事後要約（平均、SD、95%CI）+ 収束診断（$\hat{R}$, ESS）+ ELBOまたはWAIC

---

## 付録B: 重要な数理的結果

### バーンスタイン・フォンミーゼス定理（Bayesian CLT）

正則条件下で $n \to \infty$ のとき:

$$P(\theta | x_1, \ldots, x_n) \xrightarrow{d} N\left(\hat\theta_{\text{MLE}}, \frac{1}{n}I(\theta_0)^{-1}\right)$$

- 事後分布は漸近的にMLEを中心とする正規分布に収束
- 事前分布の影響は消失（データが支配）
- 誤指定されたモデルでは収束先がKL最小化点

### ベイズの許容性

- 固有事前分布に基づくベイズ推定量は許容的（admissible）
- 許容性: どのパラメータ値でも他の推定量に支配されない
- 完備類定理: 許容的推定量はベイズ推定量またはその極限

### ド・フィネッティの定理

交換可能な確率変数の無限列 $x_1, x_2, \ldots$ に対して:

$$P(x_1, \ldots, x_n) = \int \prod_{i=1}^n f(x_i | \theta) \, dP(\theta)$$

ある混合分布（事前分布）$P(\theta)$ が存在する。
交換可能性を仮定すれば、ベイズモデルが自然に導出される（ベイズの哲学的正当化）。

### ミニマックスとベイズ

- ベイズリスクを最大化する最悪事前（least favorable prior）に対するベイズ推定量はミニマックス
- ジェームズ・スタイン推定量: $p \geq 3$ の正規平均の同時推定で、MLEはミニマックスだが許容的でない
- 収縮推定量（階層ベイズ）が支配する
