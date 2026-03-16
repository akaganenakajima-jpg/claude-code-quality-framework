# データサイエンス数学ストラテジスト上級 — 知識ベースインデックス

> 満点レベルリファレンス。DS数学ストラテジスト上級試験の全出題範囲を網羅。

## ファイル一覧

| # | ファイル | 分野 | 主要トピック |
|---|---------|------|-------------|
| 1 | `linear-algebra.md` | 線形代数 | ベクトル空間・行列・固有値・SVD・正定値行列・行列微分・テンソル |
| 2 | `calculus-optimization.md` | 微積分・最適化 | 多変数微分・積分・勾配降下・制約付き最適化・変分法・情報幾何 |
| 3 | `probability-stats.md` | 確率・統計（DS数学視点） | 確率空間・確率不等式・情報理論・ランダム行列理論 |
| 4 | `applied-math.md` | 応用数学・アルゴリズム | グラフ理論・数値計算・フーリエ解析・確率的アルゴリズム・微分方程式 |

## 横断マップ — トピック別参照先

### 機械学習の数学的基礎
| トピック | 主参照 | 副参照 |
|---------|--------|--------|
| 線形回帰の最小二乗法 | `linear-algebra.md` §3 | `calculus-optimization.md` §3 |
| ロジスティック回帰 | `calculus-optimization.md` §3 | `probability-stats.md` §3 |
| SVM（サポートベクターマシン） | `calculus-optimization.md` §4 | `linear-algebra.md` §5 |
| PCA（主成分分析） | `linear-algebra.md` §4 (SVD) | `probability-stats.md` §1 |
| ニューラルネットワーク最適化 | `calculus-optimization.md` §3 | `linear-algebra.md` §6 |
| 決定木・ランダムフォレスト | `probability-stats.md` §3 | — |
| クラスタリング | `linear-algebra.md` §4 | `applied-math.md` §1 |
| 推薦システム | `linear-algebra.md` §4 (SVD) | `applied-math.md` §1 |
| ベイズ推論 | `probability-stats.md` §1 | `applied-math.md` §4 |
| 時系列解析 | `applied-math.md` §3 | `probability-stats.md` §1 |

### データサイエンス実務での数学
| 実務課題 | 参照先 |
|---------|--------|
| 特徴量の次元削減 | `linear-algebra.md` §4 (SVD/PCA) |
| 損失関数の設計 | `probability-stats.md` §3, `calculus-optimization.md` §3 |
| ハイパーパラメータ最適化 | `calculus-optimization.md` §3-4 |
| A/Bテストの統計的有意性 | `probability-stats.md` §2 |
| グラフベース分析 | `applied-math.md` §1 |
| 数値安定性の確保 | `applied-math.md` §2 |
| 高次元データの取り扱い | `probability-stats.md` §4 |
| シミュレーション | `applied-math.md` §4-5 |
| ポートフォリオ最適化 | `calculus-optimization.md` §4 |
| 信号・画像処理 | `applied-math.md` §3 |

## 試験対策の重点ポイント

### 頻出計算パターン
1. **固有値計算**: 2x2, 3x3の特性多項式 → `linear-algebra.md` §4
2. **勾配計算**: 行列微分の公式適用 → `linear-algebra.md` §6
3. **ラグランジュ乗数法**: 等式制約下の極値 → `calculus-optimization.md` §4
4. **確率計算**: ベイズの定理の適用 → `probability-stats.md` §1
5. **情報量計算**: エントロピー・KLダイバージェンス → `probability-stats.md` §3

### 証明・導出の頻出テーマ
1. SVDの存在と一意性 → `linear-algebra.md` §4
2. 凸関数の大域最適性 → `calculus-optimization.md` §4
3. 最尤推定量の一致性 → `probability-stats.md` §1
4. PageRankの収束性 → `applied-math.md` §1

## 記法の凡例

| 記号 | 意味 |
|------|------|
| x, y, a, b | ベクトル（太字省略、小文字） |
| A, B, X | 行列（大文字） |
| x' または x^T | 転置 |
| A^{-1} | 逆行列 |
| \|x\| | ノルム（文脈でL2） |
| ∇f | 勾配ベクトル |
| H(f) | ヘッセ行列 |
| E[X] | 期待値 |
| Var(X) | 分散 |
| det(A) | 行列式 |
| tr(A) | トレース |
| rank(A) | ランク |
| ker(A) | カーネル（零空間） |
| Im(A) | 像空間 |
