# 高度モデリング — DSエキスパートリファレンス

> 統計検定データサイエンスエキスパート 満点レベル対応
> セクション番号（§）は `index.md` の横断マップから参照される

---

## §1. 高度な回帰・分類

### 1.1 一般化加法モデル (GAM)

**定義**: 応答変数と説明変数の関係を滑らかな関数の和で表現するモデル。

```
g(E[Y]) = β₀ + f₁(x₁) + f₂(x₂) + ... + fₚ(xₚ)
```

- `g()`: リンク関数（GLMと同様）
- `fⱼ()`: 平滑化関数（スプライン、局所回帰等）

**スプラインの種類**:
- **薄板スプライン (thin plate)**: ノット配置不要、計算コスト高
- **3次回帰スプライン (cubic regression)**: ノット数で柔軟性制御
- **P-スプライン**: B-スプライン基底 + 差分ペナルティ
- **テンソル積スプライン**: 交互作用項のモデリング

**平滑化パラメータ選択**:
- GCV (Generalized Cross-Validation)
- REML (Restricted Maximum Likelihood) — 推奨
- AIC/BIC

**GAM vs GLM の判断基準**:
| 条件 | 推奨モデル |
|------|-----------|
| 線形関係が理論的に期待される | GLM |
| 非線形関係の探索段階 | GAM |
| 解釈性が最優先 | GLM |
| 予測精度重視・変数間の非線形パターン | GAM |

**Pythonでの実装**:
```python
from pygam import LinearGAM, s, f, te
gam = LinearGAM(s(0) + s(1) + te(2, 3) + f(4))
gam.gridsearch(X_train, y_train)
```

### 1.2 混合効果モデル（マルチレベルモデル）

**定義**: 固定効果と変量効果を同時にモデリングし、データの階層構造を考慮。

```
Yᵢⱼ = (β₀ + u₀ⱼ) + (β₁ + u₁ⱼ)xᵢⱼ + εᵢⱼ
u₀ⱼ ~ N(0, σ²ᵤ₀), u₁ⱼ ~ N(0, σ²ᵤ₁), εᵢⱼ ~ N(0, σ²)
```

**用語**:
- **固定効果 (fixed effects)**: 母集団全体に共通するパラメータ
- **変量効果 (random effects)**: グループ単位の偏差
- **ICC (級内相関係数)**: `σ²ᵤ₀ / (σ²ᵤ₀ + σ²)` — グループ内類似度

**推定法**:
- **ML (Maximum Likelihood)**: 固定効果の推定にバイアス
- **REML (Restricted ML)**: 分散成分の推定が不偏 — 推奨

**モデル選択**:
- 変量効果の検定: LRT (尤度比検定)。ただし境界問題あり（χ²の混合分布）
- 固定効果の比較: AIC/BIC（ML推定で比較）
- 分散成分の比較: AIC/BIC（REML推定で比較）

**交差分類 vs 入れ子構造**:
- 入れ子: 生徒 ⊂ クラス ⊂ 学校
- 交差分類: 患者 × 病院 × 医師（完全な入れ子でない）

### 1.3 ゼロ過剰モデル（ZIP/ZINB）

**問題**: カウントデータで理論分布よりゼロが多い場合（医療費請求、希少事象）。

**ZIP (Zero-Inflated Poisson)**:
```
P(Y=0) = π + (1-π)e^(-λ)
P(Y=k) = (1-π) × (λᵏe^(-λ)/k!)  (k≥1)
```

**ZINB (Zero-Inflated Negative Binomial)**: 過分散もある場合。

**ハードルモデルとの違い**:
| 特性 | ゼロ過剰モデル | ハードルモデル |
|------|---------------|--------------|
| ゼロの由来 | 2つのプロセス（構造的+カウント） | 1つのプロセス（参加/非参加） |
| 正のカウントからのゼロ | あり | なし |
| 適用場面 | 「真のゼロ」と「偶然のゼロ」の区別 | 参加判断後のカウント |

**モデル選択**: Vuong検定で標準Poisson vs ZIP を比較。

### 1.4 生存時間解析

**カプラン・マイヤー推定量**:
```
Ŝ(t) = Π_{tᵢ≤t} (1 - dᵢ/nᵢ)
```
- `dᵢ`: 時点tᵢでのイベント数
- `nᵢ`: 時点tᵢでのリスク集合サイズ
- 打ち切り（censoring）: 観察期間終了・脱落 → 正確なイベント時間不明

**Cox比例ハザードモデル**:
```
h(t|X) = h₀(t) × exp(β₁x₁ + β₂x₂ + ... + βₚxₚ)
```
- `h₀(t)`: ベースラインハザード（ノンパラメトリック）
- **比例ハザード仮定**: ハザード比が時間に依存しない
- **検証方法**: Schoenfeld残差プロット、log-log生存曲線

**比例ハザード仮定の違反への対処**:
1. 時間依存共変量の導入: `β(t) = β₁ + β₂×g(t)`
2. 層別Cox: 層ごとに別のベースラインハザード
3. パラメトリックモデル（Weibull、対数正規等）

**C-index (Harrell's concordance index)**:
- 判別能の指標。0.5 = ランダム、1.0 = 完全一致
- 打ち切りデータに対応した AUC の一般化

### 1.5 競合リスクモデル

**問題**: 複数の種類のイベントが競合する場合（死因別分析、離職理由別分析）。

**原因別ハザード (Cause-Specific Hazard)**:
```
hₖ(t) = lim_{Δt→0} P(t ≤ T < t+Δt, D=k | T ≥ t) / Δt
```

**Fine-Grayモデル（部分分布ハザード）**:
- 累積発生関数 (CIF) を直接モデリング
- 共変量が CIF に与える効果を推定
- 解釈: 「特定の原因によるイベント発生確率への影響」

**原因別ハザード vs Fine-Gray**:
| 目的 | 推奨モデル |
|------|-----------|
| 病因メカニズムの理解 | 原因別ハザード |
| 臨床的予測（ある原因でのイベント確率） | Fine-Gray |

### 1.6 実務活用: 医療・金融での高度分析

**医療分野**:
- 臨床試験: Cox回帰で治療効果推定（HR = 0.7 → リスク30%低減）
- 再入院予測: 混合効果モデル（病院=ランダム効果）
- 医療費予測: ZINB（大半が低額、一部が高額）

**金融分野**:
- 信用リスク: 生存時間分析でデフォルトまでの時間モデリング
- 保険料算定: GAMで年齢・地域の非線形効果を捕捉
- 不正検知: 混合効果モデルで個人の行動パターン + 全体傾向

---

## §2. ベイズモデリング実践

### 2.1 ベイズ推定の枠組み

**ベイズの定理**:
```
p(θ|D) ∝ p(D|θ) × p(θ)
事後分布 ∝ 尤度 × 事前分布
```

**事前分布の選択指針**:
| 種類 | 特徴 | 使用場面 |
|------|------|---------|
| 無情報事前分布 | データに任せる | 情報が乏しい場合 |
| 弱情報事前分布 | パラメータの合理的範囲を制約 | 推奨デフォルト |
| 情報事前分布 | 先行研究・専門知識を反映 | メタ分析・経験蓄積 |
| 正則化事前分布 | Laplace(L1)/Normal(L2)に対応 | 高次元・過学習防止 |

**共役事前分布**:
| 尤度 | 共役事前 | 事後 |
|------|---------|------|
| 正規(μ既知σ²) | 正規 | 正規 |
| 正規(σ²既知μ) | 逆ガンマ | 逆ガンマ |
| 二項 | ベータ | ベータ |
| ポアソン | ガンマ | ガンマ |
| 多項 | ディリクレ | ディリクレ |

### 2.2 Stan/PyMCによる実装

**Stanモデルの構造**:
```stan
data {
  int<lower=0> N;
  vector[N] x;
  vector[N] y;
}
parameters {
  real alpha;
  real beta;
  real<lower=0> sigma;
}
model {
  alpha ~ normal(0, 10);
  beta ~ normal(0, 5);
  sigma ~ half_cauchy(0, 5);
  y ~ normal(alpha + beta * x, sigma);
}
```

**PyMC実装**:
```python
import pymc as pm
with pm.Model() as model:
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=5)
    sigma = pm.HalfCauchy('sigma', beta=5)
    mu = alpha + beta * x
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
    trace = pm.sample(2000, tune=1000, chains=4)
```

### 2.3 階層ベイズモデル

**構造**: グループレベルのパラメータに共通の超パラメータを設定。

```
yᵢⱼ ~ Normal(μⱼ, σ²)
μⱼ ~ Normal(μ₀, τ²)
μ₀ ~ Normal(0, 100)
τ ~ HalfCauchy(0, 5)
```

**縮約 (Shrinkage)**:
- サンプルサイズの小さいグループは全体平均に引き寄せられる
- 情報の借用 (borrowing strength) により安定した推定

**Non-Centered Parameterization（発散対策）**:
```stan
parameters {
  real mu0;
  real<lower=0> tau;
  vector[J] z;  // 標準正規
}
transformed parameters {
  vector[J] mu = mu0 + tau * z;  // 非中心化
}
```

### 2.4 ベイズ構造時系列モデル (BSTS)

**構成要素**:
- ローカルレベル/ローカルトレンド
- 季節成分
- 回帰成分（スパイク・アンド・スラブ事前分布で変数選択）

**CausalImpact**: BSTSベースの因果推論
- 介入前のデータで反実仮想を予測
- 介入後の実測値との差分が因果効果

```python
from causalimpact import CausalImpact
ci = CausalImpact(data, pre_period, post_period)
ci.summary()  # 期待効果量、信用区間、p値
```

### 2.5 MCMCの収束診断

**R̂ (Rhat, Potential Scale Reduction Factor)**:
- チェーン間変動 / チェーン内変動
- **基準: R̂ < 1.01**（旧基準1.1は不十分）

**ESS (Effective Sample Size)**:
- 自己相関を考慮した実効サンプルサイズ
- **基準: ESS > 400**（bulk-ESS, tail-ESS 両方）

**トレースプロット**:
- 「毛虫のような」混合が良好
- トレンド・停滞・周期 → 収束不良

**発散 (Divergent Transitions)**:
- HMCシミュレーターが曲率の急な領域で不正確になる
- **対処**: `adapt_delta` 引き上げ（0.95→0.99）、非中心化パラメータ化

### 2.6 実務活用: 不確実性を含む意思決定

- **予測区間の提示**: 点推定でなく事後分布の90%信用区間を意思決定者に提示
- **損失関数ベースの意思決定**: 非対称コストを反映した最適行動選択
- **段階的意思決定**: 事前分布→データ収集→事後分布の更新ループ
- **感度分析**: 事前分布の選択が結論に与える影響を定量化

---

## §3. 因果推論の実践

### 3.1 因果推論のフレームワーク

**Rubinの因果モデル（潜在結果枠組み）**:
- 個体因果効果: `τᵢ = Y¹ᵢ - Y⁰ᵢ`（観測不能 — 因果推論の根本問題）
- ATE (Average Treatment Effect): `E[Y¹ - Y⁰]`
- ATT (Average Treatment effect on the Treated): `E[Y¹ - Y⁰ | D=1]`
- CATE (Conditional ATE): `E[Y¹ - Y⁰ | X=x]`

**識別のための仮定**:
1. **SUTVA**: 安定な単位処置値の仮定（干渉なし、処置バージョン一意）
2. **無視可能性 (Ignorability)**: `(Y⁰, Y¹) ⊥ D | X`
3. **正値性 (Positivity)**: `0 < P(D=1|X) < 1`

### 3.2 傾向スコアマッチング・IPTW

**傾向スコア**: `e(X) = P(D=1 | X)`

**マッチング**:
- 最近傍マッチング（キャリパー付き）
- カーネルマッチング
- **バランス確認**: 標準化差分 < 0.1

**IPTW (Inverse Probability of Treatment Weighting)**:
```
ATE の推定量 = (1/N) Σ [Dᵢ Yᵢ/e(Xᵢ) - (1-Dᵢ)Yᵢ/(1-e(Xᵢ))]
```

**安定化重み**: `sw = P(D) / e(X)` for treated, `(1-P(D)) / (1-e(X))` for control
- 極端な重みによる分散増大を緩和

**二重にロバストな推定量 (Doubly Robust)**:
- 傾向スコアモデルと結果モデルのどちらかが正しければ一致推定量
- AIPW (Augmented IPW) が代表的

### 3.3 差分の差分法 (DID)

**基本モデル**:
```
Yᵢₜ = β₀ + β₁Dᵢ + β₂Postₜ + β₃(Dᵢ × Postₜ) + εᵢₜ
```
- `β₃` が因果効果

**平行トレンド仮定**:
- 処置がなければ、処置群と対照群のアウトカムは並行に推移したはず
- **検証**: 処置前の期間でプラセボテスト（イベントスタディプロット）

**拡張DID**:
- **Staggered DID**: 処置タイミングが異なる場合 → Callaway-Sant'Anna推定量
- **処置強度の連続的変化**: 連続DID
- **三重差分 (DDD)**: 追加の対照次元で仮定を緩和

### 3.4 回帰不連続デザイン (RDD)

**Sharp RDD**: 閾値で処置が決定的に切り替わる
```
τ_RDD = lim_{x↓c} E[Y|X=x] - lim_{x↑c} E[Y|X=x]
```

**Fuzzy RDD**: 閾値で処置確率がジャンプ（完全でない）→ IV的解釈

**実装上の注意**:
- **バンド幅選択**: MSE最適バンド幅（Imbens-Kalyanaraman）
- **カーネル**: 三角カーネル（推奨）
- **多項式次数**: 局所線形（1次）が推奨。高次は過適合リスク
- **McCrary検定**: 閾値での密度不連続テスト（操作の検出）

### 3.5 操作変数法 (IV)

**条件**:
1. **関連性 (Relevance)**: Z → D（弱い操作変数問題に注意）
2. **外生性 (Exogeneity)**: Z ⊥ ε
3. **排除制約 (Exclusion Restriction)**: Z → Y は D を通じてのみ

**2段階最小二乗法 (2SLS)**:
```
Stage 1: D = α₀ + α₁Z + v      → D̂ を取得
Stage 2: Y = β₀ + β₁D̂ + ε      → β₁ が因果効果（LATE）
```

**弱操作変数の診断**: 第1段階のF統計量 > 10（Stock-Yogo基準）

**LATE (Local Average Treatment Effect)**: 操作変数に反応する「遵守者」のみの因果効果

### 3.6 合成統制法

**目的**: 処置を受けた1つの単位に対し、複数の対照単位の加重平均で反実仮想を構築。

```
Ŷ⁰₁ₜ = Σⱼ wⱼ Yⱼₜ  (wⱼ ≥ 0, Σwⱼ = 1)
```

**重みの決定**: 処置前の期間で処置群のアウトカムを最もよく再現するよう最適化。

**プラセボテスト**: 各対照単位を「偽の処置群」として同じ手法を適用し、処置群の効果が外れ値かを確認。

### 3.7 DAGによる因果構造の可視化

**DAG (Directed Acyclic Graph)** のルール:
- **d分離**: パスがブロックされる条件
- **バックドア基準**: 交絡パスをブロックする最小の調整変数集合
- **フロントドア基準**: 媒介変数を通じた因果効果の識別

**落とし穴**:
- **合流点バイアス（衝突因子）**: 共通の結果で条件付けると偽の相関が発生
- **中間変数の調整**: 過剰調整（over-adjustment）で効果を過小推定
- **M-bias**: 一見必要な調整がむしろバイアスを生む

### 3.8 DoWhy/EconMLの活用

```python
import dowhy
model = dowhy.CausalModel(
    data=df,
    treatment='treatment',
    outcome='outcome',
    graph="digraph {treatment -> outcome; confounder -> treatment; confounder -> outcome;}"
)
identified = model.identify_effect(proceed_when_unidentifiable=True)
estimate = model.estimate_effect(identified, method_name="backdoor.propensity_score_matching")
refutation = model.refute_estimate(identified, estimate, method_name="random_common_cause")
```

**EconML（異質的処置効果）**:
```python
from econml.dml import CausalForestDML
est = CausalForestDML(model_y=LGBMRegressor(), model_t=LGBMClassifier())
est.fit(Y, T, X=X, W=W)
cate = est.effect(X_test)  # 個人レベルの因果効果
```

### 3.9 実務活用: マーケティング施策の因果効果測定

- **広告効果**: DID（広告開始前後 × 対象/非対象エリア）
- **クーポン施策**: 傾向スコアマッチング（クーポン利用者 vs 非利用者、属性調整）
- **価格弾力性**: IV法（コスト変動を操作変数に価格→需要の因果効果）
- **政策評価**: RDD（助成金の閾値スコアでの効果）
- **Uplift Modeling**: CATEを推定し、施策効果の高いセグメントにターゲティング

---

## §4. 強化学習

### 4.1 マルコフ決定過程 (MDP)

**定義**: `(S, A, P, R, γ)`
- S: 状態空間、A: 行動空間
- P(s'|s,a): 遷移確率、R(s,a): 報酬関数
- γ: 割引率 (0 ≤ γ < 1)

**価値関数**:
```
V^π(s) = E_π[Σ_{t=0}^∞ γᵗ R(sₜ, aₜ) | s₀ = s]
Q^π(s,a) = E_π[Σ_{t=0}^∞ γᵗ R(sₜ, aₜ) | s₀ = s, a₀ = a]
```

**ベルマン方程式**:
```
V*(s) = max_a [R(s,a) + γ Σ_{s'} P(s'|s,a) V*(s')]
Q*(s,a) = R(s,a) + γ Σ_{s'} P(s'|s,a) max_{a'} Q*(s',a')
```

### 4.2 Q-learning、SARSA

**Q-learning（Off-policy）**:
```
Q(s,a) ← Q(s,a) + α [r + γ max_{a'} Q(s',a') - Q(s,a)]
```

**SARSA（On-policy）**:
```
Q(s,a) ← Q(s,a) + α [r + γ Q(s',a') - Q(s,a)]
```

**差異**: Q-learningは最適方策のQ値を学習（探索中でも）。SARSAは現在の方策のQ値を学習。

**ε-greedy**: 確率εでランダム行動、1-εで貪欲行動。εを漸減するのが一般的。

**Deep Q-Network (DQN)**:
- Q関数をニューラルネットで近似
- Experience Replay: 過去の経験を再利用（i.i.d.化）
- Target Network: 学習安定化のためQ値の目標を遅延更新

### 4.3 方策勾配法

**REINFORCE**:
```
∇J(θ) = E_π [Σₜ ∇log π_θ(aₜ|sₜ) × Gₜ]
Gₜ = Σ_{k=t}^T γ^(k-t) rₖ  (累積報酬)
```

**ベースライン**: 分散低減のため `Gₜ - b(sₜ)` を使用。b(s)=V(s)が典型的。

**Actor-Critic**:
- Actor: 方策 π_θ(a|s) をパラメータ化
- Critic: 価値関数 V_w(s) をパラメータ化
- Advantage: `A(s,a) = Q(s,a) - V(s)` → 分散低減

**PPO (Proximal Policy Optimization)**:
- クリッピングで方策の更新幅を制限
- 安定した学習を実現、実装が比較的容易
- 現在最も広く使われる方策勾配法

### 4.4 バンディット問題

**多腕バンディット**: 探索と活用のトレードオフ。

**UCB (Upper Confidence Bound)**:
```
a* = argmax_a [Q̂(a) + c√(ln t / N(a))]
```
- 不確実性の高い腕を優先的に探索

**トンプソンサンプリング**:
- 各腕の報酬分布の事後分布からサンプリング
- サンプル値が最大の腕を選択
- ベイズ的に最適な探索-活用バランス
- ベータ-二項モデルが基本（二値報酬の場合）

**文脈付きバンディット**: 状態（文脈）に応じて最適な腕を選択。
- LinUCB: 線形報酬モデル
- Neural UCB: ニューラルネット + UCB

### 4.5 オフライン強化学習

**問題**: 過去のログデータのみから方策を学習（新たな探索不可）。

**分布シフト問題**: 学習データの方策と新方策の行動分布が乖離 → Q値の過大推定。

**手法**:
- **BCQ (Batch-Constrained Q-learning)**: 行動をデータ分布内に制約
- **CQL (Conservative Q-Learning)**: Q値を保守的に推定
- **OPE (Off-Policy Evaluation)**: 新方策の性能をオフラインで評価
  - IS (Importance Sampling)
  - Doubly Robust
  - FQE (Fitted Q Evaluation)

### 4.6 実務活用: 推薦システム、動的価格設定

- **推薦**: バンディットで新コンテンツの探索 + 既知の人気コンテンツの活用
- **動的価格設定**: MDPで需要状態→価格行動→利益報酬をモデル化
- **広告入札**: 文脈付きバンディットでCTR最大化の入札戦略
- **在庫管理**: 強化学習で補充タイミング・量を最適化
- **対話システム**: Actor-Criticで対話方策を最適化

---

## §5. 深層学習アーキテクチャ

### 5.1 CNN（畳み込みニューラルネットワーク）

**畳み込み層**:
```
出力サイズ = (入力サイズ - カーネルサイズ + 2×パディング) / ストライド + 1
```

**主要アーキテクチャの進化**:
| モデル | 年 | 特徴 |
|--------|-----|------|
| AlexNet | 2012 | ReLU、Dropout、GPU学習 |
| VGG | 2014 | 3×3カーネルの積層 |
| GoogLeNet | 2014 | Inceptionモジュール（並列カーネル） |
| ResNet | 2015 | 残差結合（スキップ接続）→ 深層化 |
| EfficientNet | 2019 | 幅/深さ/解像度の複合スケーリング |

**特徴量抽出としてのCNN**:
- 事前学習モデルの中間層出力を特徴量として利用
- 浅い層: エッジ・テクスチャ、深い層: 意味的特徴

### 5.2 RNN/LSTM/GRU

**Vanilla RNN の問題**: 勾配消失/爆発 → 長期依存関係を学習できない。

**LSTM (Long Short-Term Memory)**:
- 忘却ゲート: `fₜ = σ(Wf[hₜ₋₁, xₜ] + bf)`
- 入力ゲート: `iₜ = σ(Wi[hₜ₋₁, xₜ] + bi)`
- 出力ゲート: `oₜ = σ(Wo[hₜ₋₁, xₜ] + bo)`
- セル状態: `Cₜ = fₜ⊙Cₜ₋₁ + iₜ⊙tanh(Wc[hₜ₋₁, xₜ] + bc)`

**GRU (Gated Recurrent Unit)**:
- LSTMの簡略版。リセットゲート + 更新ゲート
- パラメータ数が少なく、小規模データで有利

### 5.3 Transformer

**Self-Attention**:
```
Attention(Q,K,V) = softmax(QKᵀ / √dₖ) V
```

**Multi-Head Attention**:
```
MultiHead(Q,K,V) = Concat(head₁,...,headₕ) Wᴼ
headᵢ = Attention(QWᵢᵠ, KWᵢᴷ, VWᵢⱽ)
```

**位置エンコーディング**:
```
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

**RNNとの比較**:
| 特性 | RNN | Transformer |
|------|-----|-------------|
| 並列化 | 不可（逐次処理） | 可能 |
| 長距離依存 | 勾配消失で困難 | Self-Attentionで直接参照 |
| 計算量 | O(n) | O(n²)（系列長のAttention） |
| 位置情報 | 暗黙的（順序処理） | 明示的（位置エンコーディング） |

### 5.4 オートエンコーダ

**構造**: エンコーダ → 潜在表現z → デコーダ → 再構成

**VAE (Variational Autoencoder)**:
- 潜在空間を確率分布（通常は正規分布）として学習
- 損失 = 再構成誤差 + KLダイバージェンス
- `L = E_q[log p(x|z)] - KL(q(z|x) || p(z))`
- 生成モデルとして使用可能（潜在空間からサンプリング）

**Reparameterization Trick**: `z = μ + σ⊙ε (ε ~ N(0,I))` → 勾配逆伝播可能に

### 5.5 GAN (Generative Adversarial Network)

**min-max ゲーム**:
```
min_G max_D V(D,G) = E_x[log D(x)] + E_z[log(1 - D(G(z)))]
```

**学習の不安定性への対策**:
- WGAN: Wasserstein距離ベース → 安定した勾配
- Spectral Normalization: 判別器のリプシッツ制約
- Progressive Growing: 低解像度→段階的に高解像度へ

**モード崩壊**: 生成器が多様性を失い同じ出力ばかり生成する現象。

### 5.6 転移学習

**戦略**:
| データ量 | ドメイン距離 | 戦略 |
|----------|-------------|------|
| 少 | 近い | 最終層のみファインチューニング |
| 少 | 遠い | 中間層の特徴量を利用、全層は凍結 |
| 多 | 近い | 全層ファインチューニング |
| 多 | 遠い | 全層ファインチューニング（低学習率） |

**学習率スケジュール**: 層ごとに異なる学習率（discriminative fine-tuning）。
- 浅い層: 低学習率（汎用特徴を保持）
- 深い層: 高学習率（タスク固有に適応）

### 5.7 実務活用: 画像・テキスト・時系列の深層学習

- **製造業**: CNN + 転移学習で外観検査（少量の不良品データでも高精度）
- **顧客対応**: Transformerベースのチャットボット
- **予知保全**: LSTM/Transformerで設備センサー時系列から故障予兆を検出
- **異常検知**: VAE/AutoEncoderで正常パターンを学習、再構成誤差で異常スコアリング
- **文書処理**: BERTファインチューニングで契約書の条項分類

---

## §6. 最適化理論

### 6.1 凸最適化

**凸関数の性質**:
- `f(λx + (1-λ)y) ≤ λf(x) + (1-λ)f(y)` (0 ≤ λ ≤ 1)
- 局所最適解 = 大域最適解（凸問題の根本的利点）
- ヘッセ行列が半正定値 ⟺ 凸関数

**KKT条件（Karush-Kuhn-Tucker）**:
```
最適化: min f(x) s.t. gᵢ(x) ≤ 0, hⱼ(x) = 0

1. 定常性: ∇f(x*) + Σ μᵢ∇gᵢ(x*) + Σ λⱼ∇hⱼ(x*) = 0
2. 主実行可能性: gᵢ(x*) ≤ 0, hⱼ(x*) = 0
3. 双対実行可能性: μᵢ ≥ 0
4. 相補性スラック: μᵢgᵢ(x*) = 0
```

**双対問題**: 強双対性が成立する場合（Slaterの制約想定）、主問題と双対問題の最適値が一致。

### 6.2 勾配降下法の変種

**SGD (Stochastic Gradient Descent)**:
```
θ ← θ - η ∇L_i(θ)  (ミニバッチ)
```

**モメンタム**:
```
v ← βv + ∇L(θ)
θ ← θ - ηv
```

**Adam (Adaptive Moment Estimation)**:
```
m ← β₁m + (1-β₁)∇L      (1次モーメント)
v ← β₂v + (1-β₂)(∇L)²    (2次モーメント)
m̂ = m/(1-β₁ᵗ), v̂ = v/(1-β₂ᵗ)  (バイアス補正)
θ ← θ - η × m̂/(√v̂ + ε)
```

**オプティマイザ選択指針**:
| 手法 | 特徴 | 適用場面 |
|------|------|---------|
| SGD+Momentum | 汎化性能が高い傾向 | CNN、大規模画像タスク |
| Adam | 収束が速い、チューニング容易 | NLP、Transformer |
| AdamW | Adamにデカップル重み減衰 | Transformer標準 |
| LAMB | 大バッチ学習用 | 分散学習 |

### 6.3 学習率スケジュール

- **Step Decay**: 一定エポックごとに学習率を減衰
- **Cosine Annealing**: コサイン関数に従い減衰 + ウォームリスタート
- **Warm-up**: 初期の数ステップで学習率を漸増（Transformer標準）
- **OneCycleLR**: 学習率を上昇→下降の1サイクル（Super-Convergence）

### 6.4 ベイズ最適化

**目的**: 評価コストの高いブラックボックス関数の最適化（ハイパーパラメータチューニング）。

**構成要素**:
1. **代理モデル (Surrogate)**: ガウス過程 (GP) で目的関数を近似
2. **獲得関数 (Acquisition Function)**: 次の評価点を決定
   - **EI (Expected Improvement)**: 現在の最良値からの改善期待値
   - **UCB**: 平均 + κ×標準偏差
   - **PI (Probability of Improvement)**: 改善する確率

**vs ランダムサーチ/グリッドサーチ**:
| 手法 | 評価回数 | 高次元 | 初期コスト |
|------|---------|--------|-----------|
| グリッドサーチ | O(kᵈ) | 不可 | なし |
| ランダムサーチ | ユーザ指定 | 可 | なし |
| ベイズ最適化 | 少なくて済む | △（~20次元まで） | GP学習コスト |

**ツール**: Optuna、Hyperopt、BoTorch

### 6.5 実務活用: ハイパーパラメータ最適化

- **モデル選択**: ベイズ最適化でXGBoostの `max_depth`, `learning_rate`, `n_estimators` を最適化
- **ニューラルネットの構造探索 (NAS)**: 強化学習/進化計算でアーキテクチャ自体を最適化
- **早期停止**: Asynchronous successive halving (ASHA) で不良な設定を早期に打ち切り
- **マルチフィデリティ**: 少データで粗く評価→有望な候補のみ全データで評価

---

## 試験対策チェックリスト

- [ ] GAMのスプライン種類とペナルティパラメータ選択を説明できる
- [ ] 混合効果モデルのICC、ML vs REMLの違いを説明できる
- [ ] ZIP/ZINBとハードルモデルの使い分けを判断できる
- [ ] Cox回帰の比例ハザード仮定の検証方法と違反時の対処を述べられる
- [ ] ベイズ推定のMCMC収束診断（R̂/ESS/発散）を実施できる
- [ ] 階層ベイズの縮約効果と非中心化パラメータ化を説明できる
- [ ] 傾向スコア・DID・RDD・IV・合成統制法の仮定と使い分けを判断できる
- [ ] DAGのバックドア基準・合流点バイアスを説明できる
- [ ] Q-learning vs SARSA の差異、DQNの工夫を説明できる
- [ ] バンディット問題のUCB/トンプソンサンプリングの仕組みを述べられる
- [ ] Transformer のSelf-Attention計算を手で追える
- [ ] VAEの損失関数（再構成+KL）とReparameterization Trickを説明できる
- [ ] 凸最適化のKKT条件を書ける
- [ ] Adam/SGDの使い分け判断ができる
- [ ] ベイズ最適化のGP+獲得関数の仕組みを説明できる
