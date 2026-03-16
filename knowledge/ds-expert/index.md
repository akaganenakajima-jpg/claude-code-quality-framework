# 統計検定データサイエンスエキスパート — 知識ベースインデックス

> 満点レベル対応。各ファイルはセクション番号（§）で相互参照可能。

## ファイル一覧

| # | ファイル | 内容 | 主要トピック数 |
|---|---------|------|---------------|
| 1 | `advanced-modeling.md` | 高度モデリング | 6セクション |
| 2 | `deep-analytics.md` | 高度分析手法 | 6セクション |
| 3 | `system-design.md` | データサイエンスシステム設計 | 4セクション |
| 4 | `business.md` | ビジネス課題解決 | 3セクション |

## 横断マップ — キーワードから参照先を特定

| トリガー（キーワード） | 一次参照 | 二次参照 |
|---|---|---|
| 回帰・分類・GAM・混合効果・生存時間 | `advanced-modeling.md` §1 | — |
| ベイズ推定・Stan・MCMC・階層ベイズ | `advanced-modeling.md` §2 | `business.md` §1 |
| 因果推論・傾向スコア・DID・RDD・IV | `advanced-modeling.md` §3 | `business.md` §2 |
| 強化学習・MDP・バンディット・Q-learning | `advanced-modeling.md` §4 | `business.md` §2 |
| 深層学習・CNN・RNN・Transformer・GAN | `advanced-modeling.md` §5 | `deep-analytics.md` §4,§5 |
| 最適化・SGD・Adam・ベイズ最適化 | `advanced-modeling.md` §6 | `system-design.md` §4 |
| 時系列・状態空間・変化点・VAR | `deep-analytics.md` §1 | `advanced-modeling.md` §2 |
| 空間統計・クリギング・GWR | `deep-analytics.md` §2 | — |
| ネットワーク・グラフ・中心性・GNN | `deep-analytics.md` §3 | — |
| NLP・BERT・GPT・RAG・ファインチューニング | `deep-analytics.md` §4 | `advanced-modeling.md` §5 |
| 画像解析・物体検出・セグメンテーション | `deep-analytics.md` §5 | `advanced-modeling.md` §5 |
| 推薦・協調フィルタリング・行列分解 | `deep-analytics.md` §6 | `advanced-modeling.md` §4 |
| MLアーキテクチャ・Feature Store・サービング | `system-design.md` §1 | — |
| MLOps・CI/CD・実験管理・ドリフト検出 | `system-design.md` §2 | `business.md` §1 |
| データパイプライン・Airflow・品質チェック | `system-design.md` §3 | — |
| スケーラビリティ・分散学習・GPU | `system-design.md` §4 | — |
| KPI・ROI・費用対効果・意思決定 | `business.md` §1 | `advanced-modeling.md` §3 |
| A/Bテスト・実験設計・逐次テスト | `business.md` §2 | `advanced-modeling.md` §4 |
| ダッシュボード・可視化・不確実性伝達 | `business.md` §3 | — |

## 出題傾向と学習優先度

| 優先度 | 分野 | 出題頻度 | 備考 |
|--------|------|----------|------|
| S | 因果推論 | 毎回複数問 | DID・傾向スコアは必出 |
| S | ベイズモデリング | 毎回出題 | 階層ベイズ・MCMC診断 |
| S | MLOps/システム設計 | 毎回出題 | ドリフト検出・Feature Store |
| A | 深層学習アーキテクチャ | 高頻度 | Transformer構造の理解 |
| A | 時系列（高度） | 高頻度 | 状態空間・変化点検出 |
| A | 実験設計 | 高頻度 | A/Bテスト設計の実践力 |
| B | 強化学習 | 中頻度 | バンディットは頻出 |
| B | NLP/画像解析 | 中頻度 | アーキテクチャ選択判断 |
| B | ネットワーク分析 | 中頻度 | 中心性指標の使い分け |
| C | 空間統計 | 低頻度 | 基本概念のみ押さえる |

## IPA知識ベースとの連携

DSエキスパートはIPA資格と以下の点で知識が重複・補完する:

| DSエキスパート分野 | IPA参照先 | 補完関係 |
|---|---|---|
| システム設計 | `~/.claude/knowledge/ipa/sa.md` | アーキテクチャ設計の基盤 |
| データパイプライン | `~/.claude/knowledge/ipa/db.md` | DB設計・SQL最適化 |
| ネットワーク分析 | `~/.claude/knowledge/ipa/nw.md` | ネットワーク基盤知識 |
| プロジェクト管理 | `~/.claude/knowledge/ipa/pm.md` | ML PJ管理の基盤 |
| セキュリティ | `~/.claude/knowledge/ipa/ap.md` | データセキュリティ |
