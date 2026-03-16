# 統計検定 データサイエンス発展 — 知識ベース インデックス

## ファイル一覧

| # | ファイル | 分野 | 主な内容 |
|---|---|---|---|
| 1 | `data-engineering.md` | データエンジニアリング | ETL/ELT・前処理・SQL高度技法・分散処理・データ品質管理 |
| 2 | `analytics.md` | データ分析・可視化 | EDA・可視化原則・A/Bテスト・時系列分析・テキスト分析 |
| 3 | `modeling.md` | モデリング・予測 | 教師あり/なし学習・モデル評価・解釈性・MLOps |
| 4 | `ethics.md` | データ倫理・法規 | 個人情報保護法/GDPR・AI公平性・データガバナンス |

## 分野横断マップ — どの業務でどのファイルを参照するか

| 業務シーン | 主参照 | 補助参照 |
|---|---|---|
| データ収集・前処理パイプライン構築 | `data-engineering.md` | `analytics.md` |
| 分析用SQL・Window関数・集計最適化 | `data-engineering.md` | `analytics.md` |
| 探索的データ分析・レポート作成 | `analytics.md` | `data-engineering.md` |
| ダッシュボード・可視化設計 | `analytics.md` | `ethics.md` |
| A/Bテスト設計・効果検証 | `analytics.md` | `modeling.md` |
| 予測モデル構築・評価 | `modeling.md` | `data-engineering.md`, `analytics.md` |
| 不均衡データ・異常検知 | `modeling.md` | `analytics.md` |
| モデル解釈・説明責任 | `modeling.md` | `ethics.md` |
| MLOps・モデル運用・監視 | `modeling.md` | `data-engineering.md` |
| 個人情報保護・匿名化設計 | `ethics.md` | `data-engineering.md` |
| AI倫理・公平性監査 | `ethics.md` | `modeling.md` |
| データガバナンス・品質管理 | `ethics.md` | `data-engineering.md` |
| 大規模データ基盤設計 | `data-engineering.md` | `modeling.md` |
| 時系列予測・需要予測 | `analytics.md` | `modeling.md` |
| テキストマイニング・自然言語処理 | `analytics.md` | `modeling.md` |

## 横断テーマ別索引

| テーマ | 関連ファイル |
|---|---|
| 特徴量エンジニアリング | `data-engineering.md`(前処理・エンコーディング), `modeling.md`(特徴量選択・重要度) |
| 統計的仮説検定 | `analytics.md`(A/Bテスト・検出力), `modeling.md`(モデル比較) |
| 評価指標 | `modeling.md`(RMSE/AUC/F1), `analytics.md`(KPI設計) |
| バイアス・公平性 | `ethics.md`(公平性指標), `modeling.md`(不均衡対策・SHAP) |
| データパイプライン | `data-engineering.md`(ETL/ELT), `modeling.md`(MLOps) |
| プライバシー保護 | `ethics.md`(k-匿名性・差分プライバシー), `data-engineering.md`(データ品質) |
| 可視化・報告 | `analytics.md`(グラフ選択・ダッシュボード), `modeling.md`(PDP・SHAP可視化) |

## IPA知識ベースとの連携

| DS発展テーマ | IPA参照ファイル |
|---|---|
| SQL最適化・インデックス設計 | `ipa/db.md` |
| 分散処理アーキテクチャ | `ipa/sa.md` |
| ネットワーク・API設計 | `ipa/nw.md` |
| プロジェクト管理（CRISP-DM） | `ipa/pm.md` |
| セキュリティ・暗号化 | `ipa/nw.md`, `ipa/au.md` |
| コスト・投資判断 | `ipa/st.md` |
