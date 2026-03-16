# 時系列解析 — 統計リファレンス

> 統計検定1級・満点レベル。各節末に実務活用を付記。

---

## 1. 基本概念

### 1.1 時系列データの定義

時系列 $\{X_t\}_{t \in T}$ は、時間インデックス $t$ に対応する確率変数の族。
離散時間（$T = \mathbb{Z}$）と連続時間（$T = \mathbb{R}$）があるが、実務では離散が主。

### 1.2 定常過程

**弱定常（広義定常）**: 以下の3条件を満たす過程:
1. $E[X_t] = \mu$（一定）
2. $\text{Var}(X_t) = \sigma^2 < \infty$（一定・有限）
3. $\text{Cov}(X_t, X_{t+h}) = \gamma(h)$（時点 $t$ に依存せず、ラグ $h$ のみの関数）

**強定常（狭義定常）**: $(X_{t_1}, \ldots, X_{t_k})$ の同時分布が時間シフトに対して不変。
正規過程では弱定常 ⟺ 強定常。

### 1.3 自己共分散関数・自己相関関数

**自己共分散関数 (ACVF)**:
$$\gamma(h) = \text{Cov}(X_t, X_{t+h}) = E[(X_t - \mu)(X_{t+h} - \mu)]$$

性質:
- $\gamma(0) = \text{Var}(X_t) \geq 0$
- $\gamma(h) = \gamma(-h)$（対称性）
- $|\gamma(h)| \leq \gamma(0)$
- $\gamma(h)$ は非負定値関数（任意の線形結合の分散が非負）

**自己相関関数 (ACF)**:
$$\rho(h) = \frac{\gamma(h)}{\gamma(0)}$$

$\rho(0) = 1$, $|\rho(h)| \leq 1$

**標本ACF**: $\hat{\rho}(h) = \hat{\gamma}(h) / \hat{\gamma}(0)$ で推定。
大標本での漸近分布: $\sqrt{n}\hat{\rho}(h) \xrightarrow{d} N(0, 1)$（ホワイトノイズの場合）。
$\pm 1.96/\sqrt{n}$ が95%信頼限界（コレログラムの青い帯）。

### 1.4 偏自己相関関数 (PACF)

$X_{t+1}, \ldots, X_{t+h-1}$ の影響を除去した $X_t$ と $X_{t+h}$ の相関:
$$\alpha(h) = \text{Corr}(X_t - \hat{X}_t, X_{t+h} - \hat{X}_{t+h})$$

ここで $\hat{X}_t, \hat{X}_{t+h}$ は中間変数への線形射影。

AR(p) 過程では $\alpha(h) = 0$（$h > p$）→ AR次数の同定に利用。

レビンソン・ダービン再帰で効率的に計算:
$$\alpha(h) = \frac{\gamma(h) - \sum_{j=1}^{h-1} \phi_{h-1,j}\gamma(h-j)}{\gamma(0) - \sum_{j=1}^{h-1} \phi_{h-1,j}\gamma(j)}$$

### 1.5 エルゴード性

時間平均と集合平均が一致する性質。

**平均のエルゴード性**: $\frac{1}{n}\sum_{t=1}^{n} X_t \xrightarrow{p} \mu$ が成立する条件:
$$\frac{1}{n}\sum_{h=-n}^{n}\gamma(h) \to 0 \quad (n \to \infty)$$

$\sum_{h=-\infty}^{\infty} |\gamma(h)| < \infty$（絶対和可能）が十分条件。
弱定常＋ACVFが減衰 → エルゴード的（標本平均で母平均を一致推定可能）。

### 1.6 ホワイトノイズ

$\{W_t\} \sim \text{WN}(0, \sigma^2)$: $E[W_t] = 0$, $\gamma(h) = \sigma^2 \cdot \mathbf{1}_{h=0}$

**強ホワイトノイズ（iid ノイズ）**: $W_t$ が独立同一分布。
**弱ホワイトノイズ**: 無相関だが独立とは限らない（GARCH残差はこの例）。

**実務活用**: 残差がホワイトノイズか否かの検定（Ljung-Box検定 $Q = n(n+2)\sum_{h=1}^{m}\hat{\rho}(h)^2/(n-h) \sim \chi^2_{m-p-q}$）でモデルの妥当性を診断する。

---

## 2. ARIMA モデル

### 2.1 AR(p) モデル

$$X_t = \phi_1 X_{t-1} + \phi_2 X_{t-2} + \cdots + \phi_p X_{t-p} + W_t$$

**後退シフト演算子**: $B X_t = X_{t-1}$ を用いて $\phi(B)X_t = W_t$, $\phi(z) = 1 - \phi_1 z - \cdots - \phi_p z^p$

**定常条件**: $\phi(z) = 0$ の全ての根が $|z| > 1$（単位円の外側）。
- AR(1): $|\phi_1| < 1$
- AR(2): $\phi_1 + \phi_2 < 1$, $\phi_2 - \phi_1 < 1$, $|\phi_2| < 1$（三角形領域）

**ユール・ウォーカー方程式**:
$$\gamma(h) = \phi_1 \gamma(h-1) + \cdots + \phi_p \gamma(h-p), \quad h \geq 1$$

行列形式: $\Gamma_p \boldsymbol{\phi} = \boldsymbol{\gamma}_p$ で $\boldsymbol{\phi} = \Gamma_p^{-1}\boldsymbol{\gamma}_p$, $\sigma^2 = \gamma(0) - \boldsymbol{\phi}^T \boldsymbol{\gamma}_p$

ACF: 指数減衰（AR(1)）または減衰振動（AR(2) で複素根を持つ場合）。
PACF: ラグ $p$ で切断（$\alpha(h) = 0, h > p$）。

### 2.2 MA(q) モデル

$$X_t = W_t + \theta_1 W_{t-1} + \cdots + \theta_q W_{t-q} = \theta(B)W_t$$

常に弱定常（有限個のWNの線形結合）。

ACF: ラグ $q$ で切断（$\rho(h) = 0, h > q$）。
PACF: 指数減衰。

**反転可能条件**: $\theta(z) = 0$ の全根が $|z| > 1$。
反転可能なら MA を無限次 AR で表現できる: $\theta^{-1}(B)X_t = W_t$

$$\gamma(h) = \begin{cases} \sigma^2 \sum_{j=0}^{q-|h|} \theta_j \theta_{j+|h|} & |h| \leq q \\ 0 & |h| > q \end{cases}$$

### 2.3 ARMA(p,q) モデル

$$\phi(B)X_t = \theta(B)W_t$$

定常条件: $\phi(z) = 0$ の全根が $|z| > 1$
反転可能条件: $\theta(z) = 0$ の全根が $|z| > 1$
$\phi(z)$ と $\theta(z)$ に共通根がないこと（共通因子キャンセル回避）

ACF: 指数減衰＋減衰振動の混合（ラグ $q-p$ 以降）
PACF: 指数減衰（ラグ $p-q$ 以降）

### 2.4 差分と ARIMA(p,d,q)

$d$ 階差分: $\nabla^d X_t = (1-B)^d X_t$

$\{X_t\}$ が ARIMA(p,d,q) ⟺ $\nabla^d X_t$ が ARMA(p,q)

$$\phi(B)(1-B)^d X_t = \theta(B)W_t$$

実務では $d = 1$ か $d = 2$ がほとんど。$d \geq 3$ は過剰差分の疑い。

### 2.5 季節性 ARIMA (SARIMA)

$$\phi(B)\Phi(B^s)(1-B)^d(1-B^s)^D X_t = \theta(B)\Theta(B^s)W_t$$

記法: $\text{ARIMA}(p,d,q) \times (P,D,Q)_s$

- $s$: 季節周期（月次データなら $s=12$、四半期なら $s=4$）
- $(P,D,Q)$: 季節性成分の AR 次数・差分次数・MA 次数

### 2.6 モデル同定（Box-Jenkins法）

| モデル | ACF パターン | PACF パターン |
|--------|-------------|--------------|
| AR(p)  | 指数減衰/減衰振動 | ラグ $p$ で切断 |
| MA(q)  | ラグ $q$ で切断 | 指数減衰/減衰振動 |
| ARMA(p,q) | 指数減衰（ラグ $q-p$ 後） | 指数減衰（ラグ $p-q$ 後） |

手順: ① 定常化（差分・対数変換）→ ② ACF/PACF 確認 → ③ 候補モデル選定 → ④ パラメータ推定 → ⑤ 残差診断

### 2.7 パラメータ推定

**条件付き最尤法**: 初期値を条件として対数尤度を最大化。正規分布仮定の下:
$$\ell(\boldsymbol{\phi}, \boldsymbol{\theta}, \sigma^2) = -\frac{n}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_{t=1}^{n}(X_t - \hat{X}_t)^2$$

**完全最尤法**: カルマンフィルターによるイノベーション分解で尤度を正確に計算（§5参照）。

### 2.8 モデル選択

**AIC**: $-2\ell + 2k$（$k$: パラメータ数）
**BIC (SIC)**: $-2\ell + k\log n$（$n$: 標本サイズ）

BIC は AIC より大標本でペナルティが強く、よりパーシモニアスなモデルを選ぶ。
AIC は予測精度重視、BIC は一致性（真のモデル次数を確率1で同定）重視。

**AICc**: 小標本補正版 $\text{AIC} + 2k(k+1)/(n-k-1)$

### 2.9 予測

**最小平均二乗誤差 (MMSE) 予測**: $\hat{X}_{n+h} = E[X_{n+h} | X_1, \ldots, X_n]$

ARMA の場合、イノベーション・アルゴリズムまたは Durbin-Levinson 再帰で計算。

予測誤差分散: $\text{Var}(X_{n+h} - \hat{X}_{n+h}) = \sigma^2 \sum_{j=0}^{h-1} \psi_j^2$
（$\psi_j$ は MA($\infty$) 表現の係数、$h \to \infty$ で定常分散に収束）

**実務活用**: 需要予測（小売・物流）、電力需要予測、財務計画。SARIMA は月次売上・気温等の季節パターン予測に標準的。auto.arima（R）や pmdarima（Python）で自動モデル選択。

---

## 3. 単位根検定・共和分

### 3.1 単位根過程

**ランダムウォーク**: $X_t = X_{t-1} + W_t$（ARIMA(0,1,0)）
- $\text{Var}(X_t) = t\sigma^2$（分散が線形増大）→ 非定常
- ACF: $\rho(h) = \sqrt{t/(t+h)} \to 1$（減衰しない）

**ドリフト付きランダムウォーク**: $X_t = \delta + X_{t-1} + W_t$
$E[X_t] = X_0 + \delta t$（確率的トレンド＋確定的トレンド）

### 3.2 ADF 検定（拡張ディッキー・フラー検定）

帰無仮説 $H_0$: 単位根あり（$\rho = 1$）
対立仮説 $H_1$: 定常（$|\rho| < 1$）

回帰モデル:
$$\Delta X_t = \alpha + \beta t + \gamma X_{t-1} + \sum_{j=1}^{k} \delta_j \Delta X_{t-j} + \varepsilon_t$$

$\gamma = \rho - 1$ の $t$ 統計量を DF 分布（非標準）と比較。
ラグ項 $\Delta X_{t-j}$ は系列相関除去のため（拡張の意味）。
ラグ次数 $k$ は AIC/BIC で選択。

3つのバリエーション:
1. 定数項なし・トレンドなし: $\Delta X_t = \gamma X_{t-1} + \cdots$
2. 定数項あり: $\Delta X_t = \alpha + \gamma X_{t-1} + \cdots$
3. 定数項＋線形トレンド: $\Delta X_t = \alpha + \beta t + \gamma X_{t-1} + \cdots$

棄却域: 左片側（統計量が臨界値より小さければ棄却）。

### 3.3 KPSS 検定

帰無仮説 $H_0$: 定常（トレンド定常）
対立仮説 $H_1$: 単位根あり

$X_t = \xi t + r_t + \varepsilon_t$, $r_t = r_{t-1} + u_t$（$u_t \sim (0, \sigma_u^2)$）
$H_0: \sigma_u^2 = 0$（ランダムウォーク成分が消える＝定常）

検定統計量: $\eta = \frac{1}{n^2 \hat{\sigma}_\varepsilon^2}\sum_{t=1}^{n}S_t^2$, $S_t = \sum_{i=1}^{t}\hat{\varepsilon}_i$

ADF と KPSS を併用し、両方の結果が整合的か確認するのが良い実務慣行:
| ADF | KPSS | 解釈 |
|-----|------|------|
| 棄却 | 棄却しない | 定常 |
| 棄却しない | 棄却 | 単位根 |
| 棄却 | 棄却 | 判断困難（構造変化の疑い）|
| 棄却しない | 棄却しない | 判断困難（検出力不足）|

### 3.4 共和分

$I(d)$: $d$ 回差分で定常になる過程。

$\{X_t\}, \{Y_t\}$ が共に $I(1)$ で、$\exists \beta$ s.t. $Y_t - \beta X_t \sim I(0)$ なら共和分。
$[1, -\beta]$ を共和分ベクトルと呼ぶ。

**エングル・グレンジャー2段階法**:
1. $Y_t = \alpha + \beta X_t + e_t$ を OLS 推定
2. $\hat{e}_t$ に ADF 検定を適用（EG 臨界値を使用）

**ヨハンセン検定**: VAR に基づく尤度比検定。複数の共和分関係を同時に検定可能。
- トレース統計量: $\lambda_{\text{trace}}(r) = -n\sum_{i=r+1}^{k}\ln(1-\hat{\lambda}_i)$
- 最大固有値統計量: $\lambda_{\max}(r, r+1) = -n\ln(1-\hat{\lambda}_{r+1})$

### 3.5 見せかけの回帰

2つの独立なランダムウォーク $X_t, Y_t$ を回帰すると、$R^2$ が高く $t$ 統計量が有意になることがある（Granger & Newbold, 1974）。DW 統計量が極端に低い（残差に強い自己相関）場合は見せかけの回帰を疑う。

対処: 差分回帰、共和分検定、誤差修正モデル (ECM)。

**実務活用**: 為替・株価・GDP 等の経済時系列は大半が $I(1)$。水準回帰の前に必ず単位根検定→共和分検定を実施。共和分関係が見つかれば ECM: $\Delta Y_t = \alpha(\hat{e}_{t-1}) + \sum \beta_i \Delta X_{t-i} + \varepsilon_t$（$\alpha < 0$ が均衡回帰速度）。ペアトレード戦略の根拠にもなる。

---

## 4. スペクトル解析

### 4.1 パワースペクトル密度関数

定常過程の自己共分散 $\gamma(h)$ が絶対和可能なとき:
$$f(\omega) = \frac{1}{2\pi}\sum_{h=-\infty}^{\infty}\gamma(h)e^{-i\omega h}, \quad \omega \in [-\pi, \pi]$$

逆変換: $\gamma(h) = \int_{-\pi}^{\pi} f(\omega)e^{i\omega h} d\omega$

$f(\omega) \geq 0$（非負）、$\gamma(0) = \text{Var}(X_t) = \int_{-\pi}^{\pi}f(\omega)d\omega$

### 4.2 ウィーナー・ヒンチンの定理

弱定常過程において、ACVFとパワースペクトル密度はフーリエ変換対をなす。
$$f(\omega) = \mathcal{F}\{\gamma(h)\}, \quad \gamma(h) = \mathcal{F}^{-1}\{f(\omega)\}$$

周波数領域と時間領域の等価性を保証する基本定理。

代表的スペクトル:
- ホワイトノイズ: $f(\omega) = \sigma^2 / (2\pi)$（全周波数で一定）
- AR(1) $\phi > 0$: 低周波にピーク（トレンド成分が強い）
- AR(1) $\phi < 0$: 高周波にピーク（交互変動が強い）
- MA(1): $f(\omega) = \frac{\sigma^2}{2\pi}(1 + \theta^2 + 2\theta\cos\omega)$

### 4.3 ピリオドグラムと平滑化

**ピリオドグラム**: スペクトル密度の素朴な推定量
$$I(\omega_j) = \frac{1}{2\pi n}\left|\sum_{t=1}^{n}X_t e^{-i\omega_j t}\right|^2, \quad \omega_j = 2\pi j/n$$

問題: ピリオドグラムは一致推定量でない（分散が減少しない）。

**平滑化ピリオドグラム**: 窓関数 $W_m$ で平滑化
$$\hat{f}(\omega) = \sum_{|h| \leq m} w(h/m)\hat{\gamma}(h)e^{-i\omega h}$$

代表的窓関数:
- Bartlett窓: $w(u) = 1 - |u|$
- Parzen窓: 3次スプライン
- Daniell窓: 矩形（移動平均）

帯域幅 $m$ はバイアス-分散トレードオフ。$m$ 大→低バイアス/高分散、$m$ 小→高バイアス/低分散。

### 4.4 クロススペクトルとコヒーレンス

2変量定常過程 $(X_t, Y_t)$ のクロススペクトル:
$$f_{XY}(\omega) = \frac{1}{2\pi}\sum_{h=-\infty}^{\infty}\gamma_{XY}(h)e^{-i\omega h}$$

**コヒーレンス**: 周波数 $\omega$ における2系列の線形相関の強さ
$$C_{XY}(\omega) = \frac{|f_{XY}(\omega)|^2}{f_X(\omega)f_Y(\omega)} \in [0, 1]$$

**実務活用**: 振動解析（機械工学）、脳波解析（EEG）、潮汐予測。金融では週次・月次サイクルの検出。コヒーレンスは2市場間の周波数別連動性の分析に使う。

---

## 5. 状態空間モデル

### 5.1 線形ガウス状態空間モデル

**状態方程式**: $\boldsymbol{\alpha}_{t+1} = T_t \boldsymbol{\alpha}_t + R_t \boldsymbol{\eta}_t, \quad \boldsymbol{\eta}_t \sim N(0, Q_t)$
**観測方程式**: $Y_t = Z_t \boldsymbol{\alpha}_t + \varepsilon_t, \quad \varepsilon_t \sim N(0, H_t)$

$\boldsymbol{\alpha}_t$: 状態ベクトル（観測不能）、$Y_t$: 観測値。

### 5.2 カルマンフィルター

**予測ステップ**:
$$\boldsymbol{a}_{t|t-1} = T_t \boldsymbol{a}_{t-1|t-1}$$
$$P_{t|t-1} = T_t P_{t-1|t-1} T_t^T + R_t Q_t R_t^T$$

**更新ステップ**:
$$v_t = Y_t - Z_t \boldsymbol{a}_{t|t-1} \quad \text{（イノベーション）}$$
$$F_t = Z_t P_{t|t-1} Z_t^T + H_t \quad \text{（イノベーション分散）}$$
$$K_t = P_{t|t-1} Z_t^T F_t^{-1} \quad \text{（カルマンゲイン）}$$
$$\boldsymbol{a}_{t|t} = \boldsymbol{a}_{t|t-1} + K_t v_t$$
$$P_{t|t} = (I - K_t Z_t) P_{t|t-1}$$

カルマンゲイン $K_t$ は観測の信頼度と状態の不確実性のバランスを動的に調整する。

### 5.3 固定区間平滑化

全観測 $Y_1, \ldots, Y_n$ を用いた状態推定（後方再帰）:
$$\boldsymbol{a}_{t|n} = \boldsymbol{a}_{t|t} + P_{t|t}T_{t+1}^T P_{t+1|t}^{-1}(\boldsymbol{a}_{t+1|n} - \boldsymbol{a}_{t+1|t})$$

フィルタリング（逐次）より平滑化（全データ）の方が推定精度が高い。

### 5.4 尤度関数の計算（イノベーション分解）

$$\log L = -\frac{n}{2}\log(2\pi) - \frac{1}{2}\sum_{t=1}^{n}\left[\log|F_t| + v_t^T F_t^{-1} v_t\right]$$

カルマンフィルターの副産物 $(v_t, F_t)$ から直接計算可能。
ARIMA を状態空間表現に変換すれば、完全最尤推定が可能。

### 5.5 EM アルゴリズムによるパラメータ推定

E ステップ: 現在のパラメータで固定区間平滑化 → 状態の期待値・共分散を計算
M ステップ: 完全データ対数尤度の期待値を最大化 → パラメータ更新

収束は遅いが数値的に安定。多変量・欠測値ありの場合に有利。

### 5.6 ARIMA の状態空間表現

ARIMA(1,1,1) の例: $Y_t = \alpha_t + \varepsilon_t$ として
- $\alpha_t = \alpha_{t-1} + \phi(\alpha_{t-1} - \alpha_{t-2}) + \theta \eta_{t-1} + \eta_t$

一般に ARIMA(p,d,q) は $(p+d) \times (p+d)$ の状態空間に変換可能。

**実務活用**: 欠測値を含む不規則サンプリングデータの分析（カルマンフィルターは欠測時に更新ステップをスキップするだけ）。GPS 測位（位置・速度の同時推定）。経済指標のリアルタイム推定（GDP ナウキャスティング）。制御工学（ロボット姿勢推定）。

---

## 6. GARCH モデル

### 6.1 ARCH(q) モデル

Engle (1982)。条件付き分散が過去の二乗残差に依存:

$$X_t = \sigma_t W_t, \quad W_t \sim \text{iid}(0, 1)$$
$$\sigma_t^2 = \alpha_0 + \alpha_1 X_{t-1}^2 + \cdots + \alpha_q X_{t-q}^2$$

条件: $\alpha_0 > 0$, $\alpha_i \geq 0$, $\sum \alpha_i < 1$（弱定常のため）

$X_t$ は無相関だが独立でない（弱ホワイトノイズ）。$X_t^2$ に自己相関が存在。

### 6.2 GARCH(p,q) モデル

Bollerslev (1986)。過去の条件付き分散も組み込む:

$$\sigma_t^2 = \alpha_0 + \sum_{i=1}^{q}\alpha_i X_{t-i}^2 + \sum_{j=1}^{p}\beta_j \sigma_{t-j}^2$$

GARCH(1,1) が実務で最も頻用:
$$\sigma_t^2 = \alpha_0 + \alpha_1 X_{t-1}^2 + \beta_1 \sigma_{t-1}^2$$

弱定常条件: $\alpha_1 + \beta_1 < 1$
非条件分散: $\text{Var}(X_t) = \alpha_0 / (1 - \alpha_1 - \beta_1)$

$\alpha_1 + \beta_1$ が1に近いほど「ボラティリティの持続性」が高い（IGARCH: $= 1$）。

**ボラティリティ・クラスタリング**: 大きな変動の後には大きな変動が続く傾向。金融収益率の典型的特徴。GARCH はこの現象を自然にモデル化する。

### 6.3 EGARCH（指数 GARCH）

Nelson (1991)。非対称効果（レバレッジ効果）を捕捉:

$$\ln\sigma_t^2 = \omega + \sum_{i=1}^{q}\left[\alpha_i |Z_{t-i}| + \gamma_i Z_{t-i}\right] + \sum_{j=1}^{p}\beta_j \ln\sigma_{t-j}^2$$

$\gamma_i < 0$: 負のショック（下落）が正のショックより大きくボラティリティを増大。
対数をとるため $\sigma_t^2 > 0$ の制約が自動的に保証される。

### 6.4 GJR-GARCH

Glosten, Jagannathan, Runkle (1993):

$$\sigma_t^2 = \alpha_0 + (\alpha_1 + \gamma_1 \cdot \mathbf{1}_{X_{t-1}<0})X_{t-1}^2 + \beta_1 \sigma_{t-1}^2$$

$\gamma_1 > 0$: 負のリターン時に条件付き分散が追加的に増大（レバレッジ効果）。

### 6.5 条件付き分散の推定と応用

最尤法（正規分布仮定、または $t$ 分布・GED で裾の厚さを考慮）。
擬似最尤推定 (QMLE): 正規尤度で推定しても分布仮定が誤っていてもパラメータは一致推定（正則条件下）。

**実務活用**: **VaR（Value at Risk）**: $\text{VaR}_\alpha = \mu_{t+1} + z_\alpha \hat{\sigma}_{t+1}$。リスク管理の基礎ツール。ボラティリティ予測はオプション・プライシング、ポートフォリオ最適化、リスク・パリティ戦略の入力。収益率の肥尾（fat tail）と非対称性をモデル化する上で標準手法。

---

## 7. VAR モデル

### 7.1 VAR(p) の定義と推定

$k$ 変量 VAR(p):
$$\boldsymbol{Y}_t = \boldsymbol{c} + A_1 \boldsymbol{Y}_{t-1} + \cdots + A_p \boldsymbol{Y}_{t-p} + \boldsymbol{u}_t, \quad \boldsymbol{u}_t \sim N(\boldsymbol{0}, \Sigma)$$

$A_i$: $k \times k$ 係数行列、パラメータ数は $k^2 p + k$（次元の呪い）。

推定: 各方程式を OLS で個別推定（SUR と同値。誤差共分散が方程式間で同じ説明変数のため）。
次数選択: AIC/BIC/HQ。

定常条件: $\det(I_k - A_1 z - \cdots - A_p z^p) = 0$ の全根が $|z| > 1$。

### 7.2 グレンジャー因果性検定

$\{X_t\}$ が $\{Y_t\}$ の「グレンジャー原因」:
$$H_0: X \text{ の過去値は } Y \text{ の予測に寄与しない}$$

VAR 内で $Y$ 方程式中の $X$ のラグ係数が全てゼロか否かの $F$ 検定（Wald 検定）。
双方向の因果・フィードバック関係も検定可能。

注意: 統計的「予測改善」であり、真の因果関係ではない。

### 7.3 インパルス応答関数 (IRF)

VAR(p) の MA($\infty$) 表現: $\boldsymbol{Y}_t = \boldsymbol{\mu} + \sum_{i=0}^{\infty}\Psi_i \boldsymbol{u}_{t-i}$

$\Psi_i$ の $(j,k)$ 要素 = $k$ 番目の変数への単位ショックが $i$ 期後に $j$ 番目の変数に与える影響。

直交化IRF: $\boldsymbol{u}_t = P\boldsymbol{\varepsilon}_t$（$P$: $\Sigma$ のコレスキー分解、$\varepsilon_t$ は無相関）。
変数の順序に依存する（コレスキー順序の問題）。

### 7.4 分散分解 (FEVD)

$h$ 期先予測誤差の分散を各変数のショックに帰属:
$$\text{FEVD}_{j \leftarrow k}(h) = \frac{\sum_{i=0}^{h-1}(\Psi_i P)_{jk}^2}{\sum_{i=0}^{h-1}\sum_{m=1}^{K}(\Psi_i P)_{jm}^2}$$

各変数の予測誤差のうち何%が各ショックに起因するかを示す。

### 7.5 構造 VAR (SVAR)

同時点の構造的関係を識別:
$$A_0 \boldsymbol{Y}_t = \boldsymbol{c}^* + A_1^* \boldsymbol{Y}_{t-1} + \cdots + \boldsymbol{\varepsilon}_t$$

$A_0$ は非対角要素に制約を課して識別（短期制約・長期制約・符号制約）。
$k(k-1)/2$ 個の制約が最低限必要（ジャスト識別）。

**実務活用**: マクロ経済政策分析（金融政策ショックの波及効果）。複数の経済指標（GDP/金利/インフレ率/失業率）の相互依存関係のモデル化。多変量予測と要因分解。

---

## 8. 非線形時系列モデル

### 8.1 閾値 AR モデル (TAR)

Tong (1978)。状態変数 $Z_t$ の値に応じてAR係数が切り替わる:

$$X_t = \begin{cases} \phi_1^{(1)} X_{t-1} + \cdots + \phi_{p_1}^{(1)} X_{t-p_1} + \varepsilon_t^{(1)} & Z_t \leq r \\ \phi_1^{(2)} X_{t-1} + \cdots + \phi_{p_2}^{(2)} X_{t-p_2} + \varepsilon_t^{(2)} & Z_t > r \end{cases}$$

$r$: 閾値パラメータ、$Z_t$: 閾値変数。

**SETAR**: $Z_t = X_{t-d}$（自己遷移、$d$: 遅延パラメータ）。

閾値 $r$ の推定はグリッドサーチ + 条件付き OLS。漸近理論は非標準（Davies の問題: 帰無仮説下で $r$ が識別不能）。

### 8.2 マルコフ切替モデル (MS-AR)

Hamilton (1989)。隠れマルコフ連鎖 $S_t \in \{1, \ldots, M\}$ がレジームを支配:

$$X_t = \mu_{S_t} + \phi_1^{(S_t)} X_{t-1} + \cdots + \sigma_{S_t} \varepsilon_t$$

遷移確率: $P(S_t = j | S_{t-1} = i) = p_{ij}$

EM アルゴリズム（Hamilton フィルター + 平滑化）でパラメータ推定。
フィルタリング確率 $P(S_t = j | Y_1, \ldots, Y_t)$ はリアルタイムのレジーム推定。

**実務活用**: 景気循環の拡張・後退レジーム判定（NBER準拠）。金融市場のブル/ベア相場検出。為替レートのレジーム変化。ボラティリティの構造変化検出（平穏期/動乱期）。

---

## 9. 長期記憶過程

### 9.1 ARFIMA モデル

$$\phi(B)(1-B)^d X_t = \theta(B)W_t, \quad d \in (-0.5, 0.5)$$

$d$ が非整数（fractional）。

- $0 < d < 0.5$: 長期記憶（long memory）。ACF はべき減衰 $\rho(h) \sim C h^{2d-1}$（指数減衰より遅い）。
- $-0.5 < d < 0$: 反持続（anti-persistent）。ACF が急速に減衰。
- $d = 0$: ARMA（短期記憶）。

スペクトル: $f(\omega) \sim C \omega^{-2d}$（$\omega \to 0$）。$d > 0$ なら原点でスペクトルが発散（低周波パワーが卓越）。

推定法:
- **GPH 推定量**: ピリオドグラムの低周波領域の対数回帰 $\log I(\omega_j) = c - d \cdot 2\log|1-e^{-i\omega_j}|$
- **Whittle 推定量**: 周波数領域の近似最尤推定
- **完全最尤推定**: 状態空間表現 + カルマンフィルター

### 9.2 ハースト指数

$H = d + 0.5 \in (0, 1)$

- $H = 0.5$: 短期記憶（ランダムウォークの増分）
- $0.5 < H < 1$: 長期正相関（トレンド持続性）
- $0 < H < 0.5$: 長期負相関（平均回帰傾向）

R/S 解析: $R(n)/S(n) \sim C n^H$ から $H$ を推定（$R$: レンジ、$S$: 標準偏差）。

**実務活用**: ネットワークトラフィックの自己相似性（Ethernet の LRD）、水文学（ナイル川の水位: Hurst の原論文）、金融収益率のボラティリティ（ボラティリティ系列は $H \approx 0.7$-$0.9$ の長期記憶を持つことが知られている）。

---

## 10. 時系列の分解

### 10.1 古典的分解

**加法モデル**: $X_t = T_t + S_t + R_t$（トレンド + 季節 + 残差）
**乗法モデル**: $X_t = T_t \cdot S_t \cdot R_t$（対数変換で加法に帰着）

手順:
1. 移動平均でトレンド $\hat{T}_t$ を推定（$2 \times m$ 移動平均で季節除去: $m$ が偶数の場合）
2. $X_t - \hat{T}_t$ から季節成分 $\hat{S}_t$ を推定（同じ月/曜日の平均）
3. 残差 $\hat{R}_t = X_t - \hat{T}_t - \hat{S}_t$

### 10.2 移動平均フィルター

$m$ 次対称移動平均: $\hat{T}_t = \sum_{j=-k}^{k} a_j X_{t+j}$（$m = 2k+1$）

偶数周期 $s$ の場合: $2 \times s$ 移動平均（端点の重み $1/(2s)$、他は $1/s$）

移動平均はローパスフィルター（高周波成分を除去）。
Henderson 移動平均: 3次トレンドに最適化された滑らかな重み。

### 10.3 STL 分解

Seasonal and Trend decomposition using Loess (Cleveland et al., 1990)。

アルゴリズム概要:
1. **内側ループ**: 季節成分の抽出（サブシリーズの Loess 平滑化）→ トレンドの抽出（残差の Loess 平滑化）を反復
2. **外側ループ**: ロバスト重み付け（外れ値の影響を低減）

パラメータ:
- `n.p`: 季節周期
- `n.s`: 季節平滑化の窓幅（奇数、大きいほど安定した季節パターン）
- `n.t`: トレンド平滑化の窓幅
- `n.l`: 低域フィルタの窓幅（通常 `n.p` と同じ）
- `n.i`: 内側ループ反復数（通常2で十分）
- `n.o`: 外側ループ反復数（外れ値がなければ0、あれば5-10）

特徴:
- 季節成分が時間変化することを許容
- Loess（局所重み付き回帰）によるロバスト性
- 乗法モデルには対数変換後に適用

### 10.4 HP フィルター

Hodrick-Prescott フィルター。トレンド $\tau_t$ を以下の最小化で抽出:

$$\min_{\{\tau_t\}} \left[\sum_{t=1}^{n}(X_t - \tau_t)^2 + \lambda\sum_{t=2}^{n-1}(\tau_{t+1} - 2\tau_t + \tau_{t-1})^2\right]$$

第1項: データへの当てはまり、第2項: トレンドの滑らかさ（2階差分のペナルティ）。

$\lambda$: 平滑化パラメータ
- $\lambda = 0$: $\tau_t = X_t$（ペナルティなし、データそのもの）
- $\lambda \to \infty$: 線形トレンド
- 慣例: 四半期データ $\lambda = 1600$、月次 $\lambda = 14400$、年次 $\lambda = 6.25$

解は閉形式: $\boldsymbol{\tau} = (I + \lambda K^T K)^{-1}\boldsymbol{X}$（$K$: 2階差分行列）

批判点（Hamilton 2018）: 端点問題（直近値の推定が不安定）、スプリアスな周期成分の生成。代替として Hamilton 回帰フィルター（$X_{t+h} = \beta_0 + \beta_1 X_t + \cdots + \varepsilon_{t+h}$）が提案されている。

**実務活用**: マクロ経済分析で最も広く使われるトレンド抽出法（GDP ギャップ推定）。STL は小売売上・コールセンター着信量等の実務予測で標準的。Prophet（Facebook/Meta）は STL の拡張で、祝日効果・変化点を組み込む。

---

## 付録: 重要な定理・公式一覧

| 定理・公式 | 内容 |
|-----------|------|
| ウォルド分解定理 | 任意の弱定常過程 = 決定論的成分 + MA($\infty$) |
| ウィーナー・ヒンチン | ACVF ⟷ パワースペクトル密度（フーリエ変換対）|
| ユール・ウォーカー方程式 | AR(p) のACVF再帰関係 |
| イノベーション分解 | 尤度 = $\prod_t p(v_t | F_t)$（カルマンフィルター副産物）|
| Beveridge-Nelson 分解 | $I(1)$ 過程 = ランダムウォーク + 定常成分 |
| グレンジャー表現定理 | 共和分 ⟹ ECM 表現が存在（逆も成立）|
| 連続写像定理 | 単位根漸近理論の基礎（関数的中心極限定理）|
