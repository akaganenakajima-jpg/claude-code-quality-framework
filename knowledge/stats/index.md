# 統計検定1級 知識ベース — インデックス

## ファイル一覧

| # | ファイル | 分野 | 主な内容 |
|---|---|---|---|
| 1 | `prob.md` | 確率論・確率分布 | 測度論的確率・離散/連続分布・多変量分布・特性関数・極限定理・不等式 |
| 2 | `inference.md` | 統計的推測 | MLE・十分統計量・UMVUE・信頼区間・仮説検定・漸近理論・検出力分析 |
| 3 | `multivariate.md` | 多変量解析 | PCA・因子分析・判別分析・正準相関・クラスター分析・MANOVA・SEM |
| 4 | `ts.md` | 時系列解析 | ARIMA・単位根検定・スペクトル解析・状態空間モデル・GARCH・VAR |
| 5 | `bayes.md` | ベイズ統計 | 共役事前・MCMC・階層ベイズ・変分推論・ノンパラメトリックベイズ |
| 6 | `regression.md` | 回帰分析・GLM | 線形回帰・GLM・ロジスティック・正則化・混合効果・GAM・生存時間解析 |
| 7 | `doe.md` | 実験計画法・ノンパラメトリック | 要因計画・応答曲面法・順位検定・ブートストラップ・ロバスト統計 |
| 8 | `stochastic.md` | 確率過程・決定理論 | マルコフ連鎖・ポアソン過程・ブラウン運動・マルチンゲール・待ち行列・因果推論 |
| 9 | `ml.md` | 統計的機械学習 | 学習理論・SVM・アンサンブル・EM・カーネル法・グラフィカルモデル・強化学習 |

## 分野横断マップ — どの業務でどのファイルを参照するか

| 業務シーン | 主参照 | 補助参照 |
|---|---|---|
| A/Bテスト設計・サンプルサイズ計算 | `inference.md` | `doe.md`, `bayes.md` |
| 予測モデル構築・機械学習 | `ml.md` | `regression.md`, `multivariate.md` |
| 時系列予測・異常検知 | `ts.md` | `stochastic.md`, `bayes.md` |
| ベイズ推定・不確実性定量化 | `bayes.md` | `inference.md`, `prob.md` |
| 回帰分析・因果推論 | `regression.md` | `stochastic.md`, `doe.md` |
| 確率モデリング・シミュレーション | `prob.md` | `stochastic.md`, `bayes.md` |
| 次元削減・クラスタリング | `multivariate.md` | `ml.md` |
| 実験設計・多重比較 | `doe.md` | `inference.md` |
| 待ち行列・性能設計 | `stochastic.md` | `prob.md` |
| 外れ値対策・ロバスト分析 | `doe.md` | `regression.md`, `prob.md` |

## 横断テーマ別索引

| テーマ | 関連ファイル |
|---|---|
| 最尤推定・情報量 | `inference.md`(MLE/フィッシャー情報量), `bayes.md`(BIC), `regression.md`(GLM) |
| 正則化 | `regression.md`(Ridge/LASSO), `ml.md`(SRM), `bayes.md`(ベイズ的正則化) |
| モデル選択 | `inference.md`(AIC/BIC), `bayes.md`(WAIC/LOO-CV), `ml.md`(交差検証) |
| 分布理論 | `prob.md`(分布族), `inference.md`(標本分布), `ts.md`(スペクトル) |
| マルコフ性 | `stochastic.md`(マルコフ連鎖), `ts.md`(ARIMA), `bayes.md`(MCMC) |
| 因果推論 | `stochastic.md`(DAG/DID/RDD), `doe.md`(実験計画), `regression.md`(傾向スコア) |
